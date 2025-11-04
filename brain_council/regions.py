"""
Brain Council - Individual Brain Regions
Each region represents a different aspect of decision-making
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, List, Optional
from dataclasses import dataclass, field


@dataclass
class RegionVote:
    """Represents a brain region's vote on a decision"""
    region_name: str
    decision: str
    reasoning: str
    confidence: float  # 0.0 to 1.0
    emotional_weight: float  # 0.0 to 1.0
    primary_emotion: str = "neutral"  # Phase 6: Primary emotion (joy, fear, sadness, etc.)
    arousal_level: float = 0.5  # Phase 6: How intense is this emotion (0.0 = calm, 1.0 = intense)
    retrieved_memories: Optional[List[Tuple[str, Dict[str, Any], float]]] = field(default=None)  # Memories retrieved by this region (Hippocampus)


class BrainRegion(ABC):
    """Base class for brain regions"""

    def __init__(self, name: str, base_weight: float):
        self.name = name
        self.base_weight = base_weight
        # Phase 6: Emotional contagion state
        self.current_emotion = "neutral"  # Current emotional state of this region
        self.emotion_intensity = 0.5  # How strongly this region feels the emotion

    @abstractmethod
    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """
        Analyze situation and return a vote

        Args:
            situation: Description of current situation
            context: Context including state, memories, etc.

        Returns:
            RegionVote with decision and reasoning
        """
        pass

    @abstractmethod
    def get_role_description(self) -> str:
        """Get description of this region's role"""
        pass

    def get_effective_weight(self, context: Dict[str, Any]) -> float:
        """
        Calculate effective weight based on context

        Args:
            context: Current state context

        Returns:
            Modified weight
        """
        return self.base_weight

    def receive_emotional_contagion(self, other_votes: list, receptivity: float = 0.3):
        """
        Phase 6: Receive emotional influence from other brain regions

        Args:
            other_votes: List of RegionVote objects from other regions
            receptivity: How much this region is influenced (0.0 = immune, 1.0 = fully receptive)
        """
        if not other_votes:
            return

        # Clamp receptivity to valid range
        receptivity = max(0.0, min(1.0, receptivity))
        if receptivity == 0.0:
            return

        # Calculate average emotion from other regions
        emotion_counts = {}
        total_intensity = 0.0

        for vote in other_votes:
            # Validate vote attributes and handle edge cases
            if not hasattr(vote, 'primary_emotion') or not hasattr(vote, 'arousal_level') or not hasattr(vote, 'emotional_weight'):
                continue

            emotion = vote.primary_emotion
            if not emotion or emotion == "":
                emotion = "neutral"

            # Handle potential NaN or infinity values with bounds checking
            arousal = getattr(vote, 'arousal_level', 0.5)
            emotional_weight = getattr(vote, 'emotional_weight', 0.5)

            # Clamp values to valid ranges
            arousal = max(0.0, min(1.0, arousal)) if isinstance(arousal, (int, float)) and not (arousal != arousal) else 0.5  # NaN check
            emotional_weight = max(0.0, min(1.0, emotional_weight)) if isinstance(emotional_weight, (int, float)) and not (emotional_weight != emotional_weight) else 0.5  # NaN check

            intensity = arousal * emotional_weight

            if emotion not in emotion_counts:
                emotion_counts[emotion] = 0.0
            emotion_counts[emotion] += intensity
            total_intensity += intensity

        # Handle edge cases: no valid emotions or zero total intensity
        if not emotion_counts or total_intensity <= 1e-6:  # Use small epsilon instead of exact zero
            return

        # Find dominant emotion
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
        dominant_intensity = emotion_counts[dominant_emotion] / total_intensity

        # Apply contagion with decay
        if dominant_emotion != "neutral":
            # Validate current emotion_intensity
            if not hasattr(self, 'emotion_intensity') or not isinstance(self.emotion_intensity, (int, float)) or self.emotion_intensity != self.emotion_intensity:
                self.emotion_intensity = 0.5  # Default if invalid

            # Blend current emotion with incoming emotion
            self.current_emotion = dominant_emotion
            self.emotion_intensity = (
                self.emotion_intensity * (1.0 - receptivity) +
                dominant_intensity * receptivity
            )
            # Clamp to valid range
            self.emotion_intensity = max(0.0, min(1.0, self.emotion_intensity))

    def get_emotional_state(self) -> Tuple[str, float]:
        """
        Phase 6: Get current emotional state of this region

        Returns:
            Tuple of (emotion_name, intensity)
        """
        return (self.current_emotion, self.emotion_intensity)


class PrefrontalCortex(BrainRegion):
    """Logic, planning, and long-term thinking"""

    def __init__(self):
        from config import Config
        super().__init__("Prefrontal Cortex", Config.VOTE_WEIGHT_PREFRONTAL)

    def get_role_description(self) -> str:
        return "Logic & Planning - Evaluates long-term consequences and trainer relationship"

    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Analyze from logical and planning perspective"""
        state = context.get('physical_state', {})
        relationship = context.get('relationship', {})

        # Consider energy levels for planning
        energy = state.get('energy', 50)
        trust = relationship.get('trust', 50)

        # Logical assessment
        if "explore" in situation.lower() or "adventure" in situation.lower():
            if energy > 40:
                decision = "agree_cautiously"
                reasoning = "Exploring builds experience and strengthens our bond with trainer. But we should stay alert."
                confidence = 0.7 + (trust / 200)  # Higher trust = more confidence
                primary_emotion = "calm_focus"
                arousal_level = 0.6
            else:
                decision = "suggest_rest_first"
                reasoning = "Logic suggests we rest before exploring. Low energy could be dangerous."
                confidence = 0.8
                primary_emotion = "concern"
                arousal_level = 0.5
        elif "play" in situation.lower():
            if energy > 30:
                decision = "agree"
                reasoning = "Playing strengthens bond with trainer. It's a good use of energy."
                confidence = 0.8
                primary_emotion = "contentment"
                arousal_level = 0.4
            else:
                decision = "suggest_later"
                reasoning = "We should conserve energy. Perhaps after rest?"
                confidence = 0.7
                primary_emotion = "practical_concern"
                arousal_level = 0.3
        elif "food" in situation.lower() or "eat" in situation.lower():
            decision = "agree"
            reasoning = "Meeting basic needs is logical and necessary."
            confidence = 0.9
            primary_emotion = "rational_approval"
            arousal_level = 0.3
        else:
            decision = "consider_options"
            reasoning = "Let's think about the consequences before acting."
            confidence = 0.6
            primary_emotion = "neutral"
            arousal_level = 0.4

        return RegionVote(
            region_name=self.name,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            emotional_weight=0.3,
            primary_emotion=primary_emotion,
            arousal_level=arousal_level
        )


class Amygdala(BrainRegion):
    """Emotion and survival instincts"""

    def __init__(self):
        from config import Config
        super().__init__("Amygdala", Config.VOTE_WEIGHT_AMYGDALA)

    def get_role_description(self) -> str:
        return "Emotion & Survival - Processes fear, joy, and excitement"

    def get_effective_weight(self, context: Dict[str, Any]) -> float:
        """Amygdala weight increases under stress or strong emotion"""
        state = context.get('physical_state', {})
        location_safety = context.get('location_safety', 10)

        # Increase weight in dangerous situations
        if location_safety < 5:
            return 0.60  # Survival instinct takes over
        elif state.get('health', 100) < 30:
            return 0.50  # Fear from being hurt

        return self.base_weight

    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Analyze from emotional perspective"""
        state = context.get('physical_state', {})
        relationship = context.get('relationship', {})
        location_safety = context.get('location_safety', 10)

        happiness = state.get('happiness', 50)
        trust = relationship.get('trust', 50)

        # Emotional reactions
        if "trainer" in situation.lower() and trust > 60:
            decision = "enthusiastic_yes"
            reasoning = "TRAINER! My favorite person! This makes me so happy!"
            confidence = 0.95
            emotional_weight = 1.0
            primary_emotion = "joy"
            arousal_level = 0.9

        elif "explore" in situation.lower():
            if location_safety > 7 and trust > 60:
                decision = "excited_agree"
                reasoning = "Adventure with trainer! Exciting but safe with them!"
                confidence = 0.8
                emotional_weight = 0.9
                primary_emotion = "excitement"
                arousal_level = 0.8
            elif location_safety < 5:
                decision = "fear_disagree"
                reasoning = "Scary... Unknown places make me nervous. Too dangerous!"
                confidence = 0.9
                emotional_weight = 1.0
                primary_emotion = "fear"
                arousal_level = 0.95
            else:
                decision = "cautious_maybe"
                reasoning = "Nervous but curious... Stay close to trainer?"
                confidence = 0.6
                emotional_weight = 0.7
                primary_emotion = "anxiety"
                arousal_level = 0.6

        elif "play" in situation.lower():
            if happiness > 50:
                decision = "joyful_yes"
                reasoning = "YES! Playing is the BEST! So much joy!"
                confidence = 0.9
                emotional_weight = 1.0
                primary_emotion = "joy"
                arousal_level = 0.85
            else:
                decision = "subdued_yes"
                reasoning = "Playing might make me feel better..."
                confidence = 0.6
                emotional_weight = 0.5
                primary_emotion = "hope"
                arousal_level = 0.4

        elif "alone" in situation.lower() or "leave" in situation.lower():
            decision = "sad_protest"
            reasoning = "Don't go! Being alone is scary and lonely!"
            confidence = 0.8
            emotional_weight = 0.9
            primary_emotion = "sadness"
            arousal_level = 0.7

        else:
            decision = "curious"
            reasoning = "Interesting... How do I feel about this?"
            confidence = 0.5
            emotional_weight = 0.6
            primary_emotion = "curiosity"
            arousal_level = 0.5

        return RegionVote(
            region_name=self.name,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            emotional_weight=emotional_weight,
            primary_emotion=primary_emotion,
            arousal_level=arousal_level
        )


class Hippocampus(BrainRegion):
    """Memory and context - Now powered by vector memory retrieval (Phase 3)"""

    def __init__(self, memory_retriever=None):
        from config import Config
        super().__init__("Hippocampus", Config.VOTE_WEIGHT_HIPPOCAMPUS)
        self.memory_retriever = memory_retriever  # Optional: MemoryRetriever instance

    def get_role_description(self) -> str:
        return "Memory - Recalls past experiences and identifies patterns"

    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Analyze based on memories and patterns (Phase 3: uses vector memory if available)"""

        # Phase 3: If memory retriever is available, use it for semantic search
        if self.memory_retriever:
            return self._analyze_with_vector_memory(situation, context)

        # Fallback: Original implementation using working memory
        return self._analyze_with_working_memory(situation, context)

    def _analyze_with_vector_memory(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Phase 3: Analyze using vector memory retrieval"""
        try:
            # Retrieve relevant long-term memories
            relevant_memories = self.memory_retriever.retrieve_relevant_memories(
                situation=situation,
                context=context
            )

            # Get working memory context
            working_memory_str = self.memory_retriever.get_working_memory_context()

            # Analyze retrieved memories
            if relevant_memories:
                # Find the most relevant memory
                best_memory = relevant_memories[0]  # Already sorted by relevance
                memory_content = best_memory[0]
                memory_metadata = best_memory[1]
                relevance_score = best_memory[2]

                # Determine sentiment of memory
                emotion = memory_metadata.get('primary_emotion', 'neutral')
                significance = memory_metadata.get('significance', 5.0)

                # Positive memories
                if emotion in ['joy', 'gratitude', 'trust', 'contentment']:
                    decision = "remember_positive"
                    reasoning = f"I remember: {memory_content[:80]}... That was good!"
                    confidence = min(0.9, 0.6 + (relevance_score * 0.3))
                    primary_emotion = emotion  # Inherit emotion from memory
                    arousal_level = 0.6

                # Negative memories
                elif emotion in ['fear', 'sadness', 'anger']:
                    decision = "remember_negative"
                    reasoning = f"I remember: {memory_content[:80]}... That was scary/difficult."
                    confidence = min(0.9, 0.6 + (relevance_score * 0.3))
                    primary_emotion = emotion  # Inherit emotion from memory
                    arousal_level = 0.7

                # Neutral or curious memories
                else:
                    decision = "remember_neutral"
                    reasoning = f"I recall something similar: {memory_content[:80]}..."
                    confidence = min(0.8, 0.5 + (relevance_score * 0.3))
                    primary_emotion = "nostalgia"
                    arousal_level = 0.4

                # Adjust confidence based on memory significance
                confidence += (significance - 6.0) / 20.0  # Small boost for very significant memories

            else:
                # No relevant memories found
                relationship = context.get('relationship', {})
                bond = relationship.get('bond', 0)

                if bond > 50:
                    decision = "trust_pattern"
                    reasoning = "No direct memory, but I trust trainer based on our relationship."
                    confidence = 0.6
                    primary_emotion = "trust"
                    arousal_level = 0.5
                else:
                    decision = "no_pattern"
                    reasoning = "This is new. No past experience to guide us."
                    confidence = 0.4
                    primary_emotion = "uncertainty"
                    arousal_level = 0.6

            return RegionVote(
                region_name=self.name,
                decision=decision,
                reasoning=reasoning,
                confidence=confidence,
                emotional_weight=0.4,
                primary_emotion=primary_emotion,
                arousal_level=arousal_level,
                retrieved_memories=relevant_memories  # Include retrieved memories
            )

        except Exception as e:
            # If vector memory fails, fall back to working memory
            import logging
            logging.getLogger(__name__).error(f"Vector memory retrieval failed: {e}")
            return self._analyze_with_working_memory(situation, context)

    def _analyze_with_working_memory(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Original implementation using working memory (fallback)"""
        memories = context.get('recent_memories', [])
        relationship = context.get('relationship', {})

        # Check for relevant memories
        relevant_memory = None
        for memory in memories[:5]:  # Check recent memories
            if any(word in memory.lower() for word in situation.lower().split()):
                relevant_memory = memory
                break

        if relevant_memory:
            # We have relevant experience
            if "positive" in relevant_memory or "fun" in relevant_memory or "happy" in relevant_memory:
                decision = "remember_positive"
                reasoning = f"I remember: {relevant_memory}. That was good!"
                confidence = 0.8
                primary_emotion = "joy"
                arousal_level = 0.6
            elif "scary" in relevant_memory or "bad" in relevant_memory or "hurt" in relevant_memory:
                decision = "remember_negative"
                reasoning = f"I remember: {relevant_memory}. That was scary..."
                confidence = 0.8
                primary_emotion = "fear"
                arousal_level = 0.7
            else:
                decision = "remember_neutral"
                reasoning = f"I remember something similar: {relevant_memory}"
                confidence = 0.6
                primary_emotion = "nostalgia"
                arousal_level = 0.4
        else:
            # New experience
            if relationship.get('bond', 0) > 50:
                decision = "trust_pattern"
                reasoning = "No direct memory, but past experiences with trainer have been mostly positive."
                confidence = 0.6
                primary_emotion = "trust"
                arousal_level = 0.5
            else:
                decision = "no_pattern"
                reasoning = "This is new. No past experience to guide us."
                confidence = 0.4
                primary_emotion = "uncertainty"
                arousal_level = 0.6

        return RegionVote(
            region_name=self.name,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            emotional_weight=0.4,
            primary_emotion=primary_emotion,
            arousal_level=arousal_level
        )


class Hypothalamus(BrainRegion):
    """Physical needs and drives"""

    def __init__(self):
        from config import Config
        super().__init__("Hypothalamus", Config.VOTE_WEIGHT_HYPOTHALAMUS)

    def get_role_description(self) -> str:
        return "Needs & Drives - Monitors hunger, energy, comfort, and physical state"

    def get_effective_weight(self, context: Dict[str, Any]) -> float:
        """Weight increases when needs are urgent"""
        state = context.get('physical_state', {})

        hunger = state.get('hunger', 50)
        energy = state.get('energy', 50)

        # Urgent needs increase weight
        if hunger > 80 or energy < 20:
            return 0.35  # Needs become more important
        elif hunger > 60 or energy < 40:
            return 0.25

        return self.base_weight

    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Analyze based on physical needs"""
        state = context.get('physical_state', {})

        hunger = state.get('hunger', 50)
        energy = state.get('energy', 50)
        health = state.get('health', 100)

        # Check if situation addresses needs
        if "food" in situation.lower() or "eat" in situation.lower() or "berry" in situation.lower():
            if hunger > 50:
                decision = "urgent_need"
                reasoning = "HUNGRY! Need food now!"
                confidence = 0.95
                primary_emotion = "craving"
                arousal_level = 0.8
            else:
                decision = "accept"
                reasoning = "Food is always good, even if not urgent."
                confidence = 0.7
                primary_emotion = "satisfaction"
                arousal_level = 0.3

        elif "rest" in situation.lower() or "sleep" in situation.lower() or "nap" in situation.lower():
            if energy < 30:
                decision = "urgent_need"
                reasoning = "So tired... Need rest badly."
                confidence = 0.95
                primary_emotion = "exhaustion"
                arousal_level = 0.2
            else:
                decision = "not_needed"
                reasoning = "Not particularly tired right now."
                confidence = 0.6
                primary_emotion = "neutral"
                arousal_level = 0.5

        elif "play" in situation.lower() or "explore" in situation.lower():
            if energy < 30:
                decision = "too_tired"
                reasoning = "Too exhausted for this. Need energy first."
                confidence = 0.9
                primary_emotion = "fatigue"
                arousal_level = 0.3
            elif hunger > 70:
                decision = "too_hungry"
                reasoning = "Too hungry to focus. Need food first."
                confidence = 0.85
                primary_emotion = "discomfort"
                arousal_level = 0.7
            elif health < 50:
                decision = "too_hurt"
                reasoning = "Not feeling well. Should rest."
                confidence = 0.9
                primary_emotion = "pain"
                arousal_level = 0.6
            else:
                decision = "acceptable"
                reasoning = "Physical state is adequate for this activity."
                confidence = 0.7
                primary_emotion = "wellness"
                arousal_level = 0.5

        else:
            # General assessment
            if hunger > 70:
                decision = "distracted_hungry"
                reasoning = "Hard to focus... so hungry..."
                confidence = 0.7
                primary_emotion = "discomfort"
                arousal_level = 0.6
            elif energy < 25:
                decision = "distracted_tired"
                reasoning = "Having trouble staying alert... need rest..."
                confidence = 0.7
                primary_emotion = "drowsiness"
                arousal_level = 0.3
            else:
                decision = "fine"
                reasoning = "Physical needs are manageable."
                confidence = 0.6
                primary_emotion = "neutral"
                arousal_level = 0.4

        return RegionVote(
            region_name=self.name,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            emotional_weight=0.2,
            primary_emotion=primary_emotion,
            arousal_level=arousal_level
        )


class BasalGanglia(BrainRegion):
    """
    Basal Ganglia - Habit formation, motor routines, and instinctive behaviors

    Phase 6 Note: Renamed from "Cerebellum" for neuroscience accuracy.
    This region actually models Basal Ganglia functions (habits, instincts, automatic responses)
    rather than true Cerebellum functions (fine motor control, balance).
    """

    def __init__(self):
        from config import Config
        super().__init__("Basal Ganglia", Config.VOTE_WEIGHT_CEREBELLUM)  # Note: Config uses old name "cerebellum"

    def get_role_description(self) -> str:
        return "Instinct & Habits - Species-specific behaviors, automatic responses, and learned routines"

    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Analyze based on instinct"""
        personality = context.get('personality', {})
        state = context.get('physical_state', {})

        playfulness = personality.get('playfulness', 5)
        energy = state.get('energy', 50)

        # Instinctive Eevee behaviors
        if "play" in situation.lower():
            if energy > 40 and playfulness > 6:
                decision = "instinct_yes"
                reasoning = "*tail wagging intensifies* Eevee instincts say PLAY!"
                confidence = 0.8
                primary_emotion = "excitement"
                arousal_level = 0.8
            else:
                decision = "instinct_mild"
                reasoning = "*ears perk up* Play instinct triggered but subdued."
                confidence = 0.6
                primary_emotion = "interest"
                arousal_level = 0.5

        elif "danger" in situation.lower() or "threat" in situation.lower():
            decision = "fight_or_flight"
            reasoning = "*fur bristles* Survival instinct activated!"
            confidence = 0.9
            primary_emotion = "alarm"
            arousal_level = 0.95

        elif "trainer" in situation.lower():
            decision = "bond_response"
            reasoning = "*automatic tail wag* Pack bond instinct!"
            confidence = 0.85
            primary_emotion = "affection"
            arousal_level = 0.7

        elif "explore" in situation.lower():
            curiosity = personality.get('curiosity', 5)
            if curiosity > 6:
                decision = "explore_instinct"
                reasoning = "*nose twitching* Natural curiosity activated!"
                confidence = 0.7
                primary_emotion = "curiosity"
                arousal_level = 0.7
            else:
                decision = "cautious_instinct"
                reasoning = "*ears swivel* Proceed with caution."
                confidence = 0.6
                primary_emotion = "wariness"
                arousal_level = 0.6

        elif "food" in situation.lower():
            decision = "approach_food"
            reasoning = "*nose sniffing* Food-seeking behavior engaged!"
            confidence = 0.8
            primary_emotion = "appetite"
            arousal_level = 0.6

        else:
            decision = "observe"
            reasoning = "*alert posture* Monitoring situation instinctively."
            confidence = 0.5
            primary_emotion = "vigilance"
            arousal_level = 0.5

        return RegionVote(
            region_name=self.name,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            emotional_weight=0.3,
            primary_emotion=primary_emotion,
            arousal_level=arousal_level
        )
