"""
Memory consolidation - Determining what becomes long-term memory

This module decides which interactions should be stored as long-term memories
and what type of memory they should become.

Following the design specification:
- Significance threshold: 6.0+ becomes long-term memory
- Different memory types for different experiences
- Pattern detection for semantic and procedural memory formation
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import logging

from memory.memory_types import (
    Memory, MemoryType, EmotionType,
    EpisodicMemory, SemanticMemory, EmotionalMemory, ProceduralMemory
)
from memory.vector_store import VectorMemoryStore

logger = logging.getLogger(__name__)


class MemoryConsolidator:
    """
    Determines what interactions become long-term memories.

    Analyzes interactions for:
    - Emotional significance
    - Novel experiences (first time events)
    - Strong emotions (joy, fear, gratitude)
    - Relationship building moments
    - Pattern formation (repeated behaviors -> procedural memories)
    """

    def __init__(
        self,
        vector_store: VectorMemoryStore,
        config: Dict[str, Any]
    ):
        """
        Initialize memory consolidator.

        Args:
            vector_store: Vector memory store
            config: Configuration dict
        """
        self.vector_store = vector_store
        self.significance_threshold = config.get('memory_significance_threshold', 6.0)

        # Pattern tracking for procedural memory formation
        self.behavior_patterns: Dict[str, List[datetime]] = {}  # behavior -> timestamps

    def process_interaction(
        self,
        user_input: str,
        eevee_response: str,
        context: Dict[str, Any],
        council_decision: Optional[Any] = None
    ) -> Optional[List[Memory]]:
        """
        Process an interaction and determine if memories should be formed.

        Args:
            user_input: What the user said
            eevee_response: How Eevee responded
            context: Full context dict (state, location, emotion, etc.)
            council_decision: Brain council decision (if available)

        Returns:
            List of Memory objects to store, or None if not significant
        """
        try:
            memories_to_store = []

            # Calculate significance
            significance = self._calculate_significance(
                user_input=user_input,
                eevee_response=eevee_response,
                context=context,
                council_decision=council_decision
            )

            # Only process if above threshold
            if significance < self.significance_threshold:
                logger.debug(f"Interaction not significant enough (score: {significance:.1f})")
                return None

            logger.info(f"Processing significant interaction (score: {significance:.1f})")

            # 1. Create episodic memory (always created for significant events)
            episodic_memory = self._create_episodic_memory(
                user_input=user_input,
                eevee_response=eevee_response,
                context=context,
                significance=significance,
                council_decision=council_decision
            )
            memories_to_store.append(episodic_memory)

            # 2. Check if we should create semantic memory (fact/knowledge)
            semantic_memory = self._extract_semantic_memory(
                user_input=user_input,
                context=context,
                significance=significance
            )
            if semantic_memory:
                memories_to_store.append(semantic_memory)

            # 3. Check if we should create emotional association
            emotional_memory = self._extract_emotional_memory(
                context=context,
                significance=significance,
                episodic_id=episodic_memory.memory_id
            )
            if emotional_memory:
                memories_to_store.append(emotional_memory)

            # 4. Check for procedural memory formation (learned behavior)
            procedural_memory = self._detect_procedural_pattern(
                user_input=user_input,
                eevee_response=eevee_response,
                context=context
            )
            if procedural_memory:
                memories_to_store.append(procedural_memory)

            # Store all memories
            for memory in memories_to_store:
                self.vector_store.store_memory(memory)
                logger.info(f"Stored {memory.memory_type.value} memory: {memory.content[:50]}...")

            return memories_to_store

        except Exception as e:
            logger.error(f"Error processing interaction for memories: {e}")
            return None

    def _calculate_significance(
        self,
        user_input: str,
        eevee_response: str,
        context: Dict[str, Any],
        council_decision: Optional[Any]
    ) -> float:
        """
        Calculate significance score for an interaction (0-10 scale).

        Factors that increase significance:
        - Strong emotions (fear, joy, gratitude, loneliness)
        - First-time experiences
        - High internal conflict in brain council
        - Relationship changes (trust/bond shifts)
        - Extreme physical states (very hungry, very low energy)

        Args:
            user_input: User's input
            eevee_response: Eevee's response
            context: Context dict
            council_decision: Council decision object

        Returns:
            float: Significance score (0-10)
        """
        significance = 5.0  # Base significance

        # Factor 1: Emotional intensity
        emotion_intensity = context.get('emotion_intensity', 5.0)
        if emotion_intensity >= 8.0:
            significance += 2.0
        elif emotion_intensity >= 7.0:
            significance += 1.0

        # Factor 2: Strong emotions
        primary_emotion = context.get('primary_emotion', '')
        intense_emotions = ['fear', 'joy', 'gratitude', 'loneliness', 'anger']
        if primary_emotion in intense_emotions:
            significance += 1.0

        # Factor 3: Novel experience (check for "first", "new", "never")
        novelty_keywords = ['first', 'new', 'never', 'discover', 'found']
        if any(word in user_input.lower() for word in novelty_keywords):
            significance += 1.5

        # Factor 4: Council conflict (low consensus = internal struggle = memorable)
        if council_decision and hasattr(council_decision, 'consensus'):
            if council_decision.consensus < 0.3:  # High conflict
                significance += 1.5
            elif council_decision.consensus < 0.5:
                significance += 0.5

        # Factor 5: Relationship moments
        relationship_keywords = ['love', 'trust', 'friend', 'care', 'miss', 'sorry']
        if any(word in user_input.lower() for word in relationship_keywords):
            significance += 1.0

        # Factor 6: Extreme physical states
        physical_state = context.get('physical_state', {})
        hunger = physical_state.get('hunger', 50)
        energy = physical_state.get('energy', 50)

        if hunger > 85 or energy < 15:
            significance += 1.0

        # Factor 7: Dangerous location
        location_safety = context.get('location_safety', 10)
        if location_safety < 5:
            significance += 1.0

        # Factor 8: Gifts and special items
        if 'give' in user_input.lower() or 'gift' in user_input.lower():
            significance += 1.5

        # Cap at 10.0
        return min(10.0, significance)

    def _create_episodic_memory(
        self,
        user_input: str,
        eevee_response: str,
        context: Dict[str, Any],
        significance: float,
        council_decision: Optional[Any]
    ) -> EpisodicMemory:
        """
        Create an episodic memory for this interaction.

        Args:
            user_input: User's input
            eevee_response: Eevee's response
            context: Context dict
            significance: Significance score
            council_decision: Council decision

        Returns:
            EpisodicMemory object
        """
        # Determine event type
        event_type = "interaction"
        if 'explore' in user_input.lower() or 'go' in user_input.lower():
            event_type = "exploration"
        elif 'give' in user_input.lower() or 'found' in user_input.lower():
            event_type = "discovery"
        elif 'play' in user_input.lower() or 'pet' in user_input.lower():
            event_type = "social"

        # Craft memory content
        location = context.get('current_location', 'unknown')
        emotion = context.get('primary_emotion', 'curious')

        content = f"Trainer said: '{user_input[:100]}' at {location}. Felt {emotion}."

        # Add outcome if available
        outcome = None
        if council_decision:
            outcome = f"Decision: {council_decision.winning_vote.decision}"

        # Extract primary emotion
        primary_emotion = None
        emotion_str = context.get('primary_emotion', '')
        try:
            # Map emotion strings to EmotionType
            emotion_mapping = {
                'joy': EmotionType.JOY, 'joyful': EmotionType.JOY,
                'fear': EmotionType.FEAR, 'scared': EmotionType.FEAR,
                'sad': EmotionType.SADNESS, 'sadness': EmotionType.SADNESS,
                'angry': EmotionType.ANGER, 'anger': EmotionType.ANGER,
                'surprise': EmotionType.SURPRISE, 'surprised': EmotionType.SURPRISE,
                'trust': EmotionType.TRUST, 'trusting': EmotionType.TRUST,
                'anticipation': EmotionType.ANTICIPATION,
                'disgust': EmotionType.DISGUST,
                'gratitude': EmotionType.GRATITUDE, 'grateful': EmotionType.GRATITUDE,
                'curiosity': EmotionType.CURIOSITY, 'curious': EmotionType.CURIOSITY,
                'loneliness': EmotionType.LONELINESS, 'lonely': EmotionType.LONELINESS,
                'contentment': EmotionType.CONTENTMENT, 'content': EmotionType.CONTENTMENT
            }
            primary_emotion = emotion_mapping.get(emotion_str.lower())
        except:
            pass

        return EpisodicMemory(
            memory_id=str(uuid.uuid4()),
            memory_type=MemoryType.EPISODIC,
            content=content,
            timestamp=datetime.now(),
            significance=significance,
            primary_emotion=primary_emotion,
            emotion_intensity=context.get('emotion_intensity', 5.0),
            location=location,
            participants=["trainer"],
            tags=["interaction", event_type],
            event_type=event_type,
            outcome=outcome
        )

    def _extract_semantic_memory(
        self,
        user_input: str,
        context: Dict[str, Any],
        significance: float
    ) -> Optional[SemanticMemory]:
        """
        Extract semantic memory (facts/knowledge) from interaction.

        Args:
            user_input: User's input
            context: Context dict
            significance: Significance score

        Returns:
            SemanticMemory or None
        """
        # Look for fact-learning opportunities
        location = context.get('current_location', '')

        # Example: Learning about locations
        if 'safe' in user_input.lower() or 'danger' in user_input.lower():
            location_safety = context.get('location_safety', 10)

            if location_safety < 5:
                fact = f"{location} is dangerous - must be careful here"
                fact_category = "location"
            else:
                fact = f"{location} is safe and comfortable"
                fact_category = "location"

            return SemanticMemory(
                memory_id=str(uuid.uuid4()),
                memory_type=MemoryType.SEMANTIC,
                content=fact,
                timestamp=datetime.now(),
                significance=significance - 1.0,  # Slightly less significant than episodic
                location=location,
                tags=["fact", fact_category],
                fact_category=fact_category,
                confidence=0.7,
                evidence_count=1
            )

        # Example: Learning about items
        if 'berry' in user_input.lower() and 'health' in user_input.lower():
            return SemanticMemory(
                memory_id=str(uuid.uuid4()),
                memory_type=MemoryType.SEMANTIC,
                content="Berries restore health and make me feel better",
                timestamp=datetime.now(),
                significance=significance - 1.0,
                tags=["fact", "item"],
                fact_category="item",
                confidence=0.8,
                evidence_count=1
            )

        return None

    def _extract_emotional_memory(
        self,
        context: Dict[str, Any],
        significance: float,
        episodic_id: str
    ) -> Optional[EmotionalMemory]:
        """
        Extract emotional association from interaction.

        Args:
            context: Context dict
            significance: Significance score
            episodic_id: ID of related episodic memory

        Returns:
            EmotionalMemory or None
        """
        emotion_intensity = context.get('emotion_intensity', 5.0)

        # Only create emotional memories for strong emotions
        if emotion_intensity < 7.0:
            return None

        location = context.get('current_location', '')
        emotion = context.get('primary_emotion', 'curious')

        # Create emotional association
        trigger = location if location else "unknown"
        response = f"Feel {emotion} when thinking about this"

        # Map emotion string
        primary_emotion = None
        try:
            emotion_mapping = {
                'joy': EmotionType.JOY, 'fear': EmotionType.FEAR,
                'sad': EmotionType.SADNESS, 'curious': EmotionType.CURIOSITY,
                'gratitude': EmotionType.GRATITUDE, 'trust': EmotionType.TRUST
            }
            primary_emotion = emotion_mapping.get(emotion.lower())
        except:
            pass

        return EmotionalMemory(
            memory_id=str(uuid.uuid4()),
            memory_type=MemoryType.EMOTIONAL,
            content=f"{trigger} is associated with {emotion}",
            timestamp=datetime.now(),
            significance=significance,
            primary_emotion=primary_emotion,
            emotion_intensity=emotion_intensity,
            location=location,
            tags=["emotion", "association"],
            trigger=trigger,
            response=response,
            learned_from=[episodic_id]
        )

    def _detect_procedural_pattern(
        self,
        user_input: str,
        eevee_response: str,
        context: Dict[str, Any]
    ) -> Optional[ProceduralMemory]:
        """
        Detect if a procedural memory (learned behavior) should be formed.

        Procedural memories form after repeated patterns.

        Args:
            user_input: User's input
            eevee_response: Eevee's response
            context: Context dict

        Returns:
            ProceduralMemory or None
        """
        # Detect behavior patterns
        behavior_name = None
        trigger_condition = None

        # Pattern: Asking for food when hungry
        physical_state = context.get('physical_state', {})
        hunger = physical_state.get('hunger', 50)

        if hunger > 70 and ('feed' in user_input.lower() or 'food' in user_input.lower()):
            behavior_name = "ask_for_food"
            trigger_condition = "When hungry"
            content = "When hungry, look at trainer and make soft sounds to ask for food"

            # Track this pattern
            if behavior_name not in self.behavior_patterns:
                self.behavior_patterns[behavior_name] = []

            self.behavior_patterns[behavior_name].append(datetime.now())

            # Only create procedural memory after seeing pattern 3+ times
            if len(self.behavior_patterns[behavior_name]) >= 3:
                return ProceduralMemory(
                    memory_id=str(uuid.uuid4()),
                    memory_type=MemoryType.PROCEDURAL,
                    content=content,
                    timestamp=datetime.now(),
                    significance=7.0,
                    tags=["behavior", "learned"],
                    behavior_name=behavior_name,
                    trigger_condition=trigger_condition,
                    success_rate=0.8,  # Assume it worked
                    times_used=len(self.behavior_patterns[behavior_name])
                )

        # Pattern: Seeking comfort when scared
        if 'scared' in eevee_response.lower() or 'afraid' in eevee_response.lower():
            behavior_name = "seek_comfort"
            trigger_condition = "When scared or afraid"
            content = "When scared, stay close to trainer and seek reassurance"

            if behavior_name not in self.behavior_patterns:
                self.behavior_patterns[behavior_name] = []

            self.behavior_patterns[behavior_name].append(datetime.now())

            if len(self.behavior_patterns[behavior_name]) >= 3:
                return ProceduralMemory(
                    memory_id=str(uuid.uuid4()),
                    memory_type=MemoryType.PROCEDURAL,
                    content=content,
                    timestamp=datetime.now(),
                    significance=7.5,
                    tags=["behavior", "learned"],
                    behavior_name=behavior_name,
                    trigger_condition=trigger_condition,
                    success_rate=0.9,
                    times_used=len(self.behavior_patterns[behavior_name])
                )

        return None

    def apply_forgetting(self) -> int:
        """
        Apply forgetting mechanism to all memories.

        Memories below significance threshold decay over time.
        Very weak memories may be deleted.

        Returns:
            int: Number of memories deleted
        """
        # TODO: Implement periodic forgetting
        # This would iterate through all memories, apply decay, and delete very weak ones
        # For now, we'll keep all memories
        logger.debug("Forgetting mechanism not yet implemented")
        return 0
