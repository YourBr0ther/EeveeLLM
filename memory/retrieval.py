"""
Memory retrieval logic - Context-aware memory search for the Brain Council

This module provides intelligent memory retrieval that considers:
- Current situation and context
- Emotional state
- Location
- Recent memories
- Memory strength and recency
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging

from memory.vector_store import VectorMemoryStore
from memory.memory_types import Memory, MemoryType, EmotionType, WorkingMemory

logger = logging.getLogger(__name__)


class MemoryRetriever:
    """
    Context-aware memory retrieval for the Hippocampus brain region.

    Retrieves relevant memories based on:
    1. Semantic similarity to current situation
    2. Emotional context
    3. Location context
    4. Temporal relevance (recent vs. old)
    5. Memory strength
    """

    def __init__(self, vector_store: VectorMemoryStore, config: Dict[str, Any]):
        """
        Initialize memory retriever.

        Args:
            vector_store: Vector memory store instance
            config: Configuration dict with retrieval settings
        """
        self.vector_store = vector_store
        self.memory_retrieval_count = config.get('memory_retrieval_count', 5)
        self.min_significance = config.get('memory_significance_threshold', 6.0)
        self.working_memory = WorkingMemory(max_size=config.get('max_working_memory', 10))

    def retrieve_relevant_memories(
        self,
        situation: str,
        context: Dict[str, Any]
    ) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        Retrieve the most relevant memories for a given situation and context.

        This is the main entry point for the Hippocampus to get memories.

        Args:
            situation: Current situation/user input
            context: Full context dict with state, location, emotion, etc.

        Returns:
            List of (memory_content, metadata, relevance_score) tuples
        """
        try:
            all_memories = []

            # 1. Semantic search - Find memories similar to current situation
            semantic_results = self.vector_store.retrieve_similar(
                query=situation,
                n_results=self.memory_retrieval_count * 2,  # Get more, then filter
                min_significance=self.min_significance - 2.0  # Lower threshold initially
            )

            for content, metadata, similarity in semantic_results:
                relevance = self._calculate_relevance(
                    similarity=similarity,
                    metadata=metadata,
                    context=context
                )
                all_memories.append((content, metadata, relevance))

            # 2. Location-based memories - Get memories from current location
            current_location = context.get('current_location')
            if current_location:
                location_results = self.vector_store.retrieve_by_location(
                    location=current_location,
                    n_results=3
                )

                for content, metadata, similarity in location_results:
                    # Check if already in results
                    if not any(mem[0] == content for mem in all_memories):
                        relevance = self._calculate_relevance(
                            similarity=similarity,
                            metadata=metadata,
                            context=context,
                            location_bonus=0.2
                        )
                        all_memories.append((content, metadata, relevance))

            # 3. Emotional context - Get memories with similar emotions
            primary_emotion = context.get('primary_emotion')
            if primary_emotion:
                emotion_results = self.vector_store.retrieve_by_emotion(
                    emotion=primary_emotion,
                    n_results=2
                )

                for content, metadata, similarity in emotion_results:
                    if not any(mem[0] == content for mem in all_memories):
                        relevance = self._calculate_relevance(
                            similarity=similarity,
                            metadata=metadata,
                            context=context,
                            emotion_bonus=0.15
                        )
                        all_memories.append((content, metadata, relevance))

            # Sort by relevance score
            all_memories.sort(key=lambda x: x[2], reverse=True)

            # Return top N most relevant
            relevant_memories = all_memories[:self.memory_retrieval_count]

            # Update access counts for retrieved memories
            self._mark_memories_accessed(relevant_memories)

            logger.debug(f"Retrieved {len(relevant_memories)} relevant memories")
            return relevant_memories

        except Exception as e:
            logger.error(f"Error retrieving memories: {e}")
            return []

    def retrieve_by_type(
        self,
        memory_type: MemoryType,
        situation: str,
        n_results: int = 3
    ) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        Retrieve memories of a specific type.

        Args:
            memory_type: Type of memory to retrieve
            situation: Current situation for semantic search
            n_results: Number of results

        Returns:
            List of (memory_content, metadata, similarity_score) tuples
        """
        try:
            results = self.vector_store.retrieve_similar(
                query=situation,
                memory_type=memory_type,
                n_results=n_results,
                min_significance=self.min_significance - 3.0
            )

            return results

        except Exception as e:
            logger.error(f"Error retrieving {memory_type.value} memories: {e}")
            return []

    def retrieve_procedural_for_situation(
        self,
        situation: str,
        context: Dict[str, Any]
    ) -> Optional[Tuple[str, Dict[str, Any], float]]:
        """
        Retrieve the most relevant procedural memory (behavior) for situation.

        Args:
            situation: Current situation
            context: Context dict

        Returns:
            Single best procedural memory, or None
        """
        try:
            # Get procedural memories
            procedural_memories = self.retrieve_by_type(
                memory_type=MemoryType.PROCEDURAL,
                situation=situation,
                n_results=5
            )

            if not procedural_memories:
                return None

            # Find best match based on success rate and relevance
            best_memory = None
            best_score = 0.0

            for content, metadata, similarity in procedural_memories:
                # Weight by success rate and similarity
                success_rate = metadata.get('success_rate', 0.5)
                combined_score = (similarity * 0.6) + (success_rate * 0.4)

                if combined_score > best_score:
                    best_score = combined_score
                    best_memory = (content, metadata, combined_score)

            return best_memory

        except Exception as e:
            logger.error(f"Error retrieving procedural memory: {e}")
            return None

    def get_emotional_associations(
        self,
        trigger: str
    ) -> List[Tuple[str, str, float]]:
        """
        Get emotional associations for a trigger (e.g., "forest" -> "scary").

        Args:
            trigger: Trigger word/concept

        Returns:
            List of (emotion, response, intensity) tuples
        """
        try:
            # Search emotional memories
            emotional_memories = self.vector_store.retrieve_similar(
                query=trigger,
                memory_type=MemoryType.EMOTIONAL,
                n_results=3
            )

            associations = []
            for content, metadata, similarity in emotional_memories:
                emotion = metadata.get('primary_emotion', 'curious')
                response = metadata.get('response', '')
                intensity = metadata.get('emotion_intensity', 5.0)

                associations.append((emotion, response, intensity))

            return associations

        except Exception as e:
            logger.error(f"Error getting emotional associations: {e}")
            return []

    def search_memories(
        self,
        query: str,
        limit: int = 10
    ) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        General memory search (for 'remember' command).

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of (memory_content, metadata, similarity) tuples
        """
        try:
            return self.vector_store.retrieve_similar(
                query=query,
                n_results=limit,
                min_significance=0.0  # No filter for explicit search
            )

        except Exception as e:
            logger.error(f"Error searching memories: {e}")
            return []

    def _calculate_relevance(
        self,
        similarity: float,
        metadata: Dict[str, Any],
        context: Dict[str, Any],
        location_bonus: float = 0.0,
        emotion_bonus: float = 0.0
    ) -> float:
        """
        Calculate overall relevance score for a memory.

        Factors:
        - Semantic similarity (base)
        - Recency (more recent = more relevant)
        - Memory strength
        - Significance
        - Context bonuses (location, emotion)

        Args:
            similarity: Semantic similarity score (0-1)
            metadata: Memory metadata
            context: Current context
            location_bonus: Bonus for location match
            emotion_bonus: Bonus for emotion match

        Returns:
            float: Relevance score (0-1+)
        """
        # Start with similarity
        relevance = similarity

        # Recency bonus - memories from last 24 hours get boost
        timestamp_str = metadata.get('timestamp', '')
        if timestamp_str:
            try:
                memory_time = datetime.fromisoformat(timestamp_str)
                age_hours = (datetime.now() - memory_time).total_seconds() / 3600

                if age_hours < 24:
                    relevance += 0.2
                elif age_hours < 168:  # 1 week
                    relevance += 0.1
            except:
                pass

        # Strength bonus - strong memories are more accessible
        strength = metadata.get('strength', 0.5)
        relevance += (strength - 0.5) * 0.2  # -0.1 to +0.1

        # Significance bonus
        significance = metadata.get('significance', 5.0)
        if significance >= 8.0:
            relevance += 0.15
        elif significance >= 7.0:
            relevance += 0.10

        # Context bonuses
        relevance += location_bonus
        relevance += emotion_bonus

        # Access count - frequently accessed memories are more important
        access_count = metadata.get('access_count', 0)
        if access_count > 5:
            relevance += 0.1

        return min(1.5, relevance)  # Cap at 1.5

    def _mark_memories_accessed(
        self,
        memories: List[Tuple[str, Dict[str, Any], float]]
    ) -> None:
        """
        Mark retrieved memories as accessed (updates strength/access_count).

        Args:
            memories: List of retrieved memories
        """
        try:
            for content, metadata, relevance in memories:
                # Extract memory ID and type from metadata
                memory_id = metadata.get('memory_id')
                memory_type_str = metadata.get('memory_type')

                if not memory_id or not memory_type_str:
                    continue

                try:
                    memory_type = MemoryType(memory_type_str)
                except ValueError:
                    continue

                # Update access count and strength
                new_access_count = metadata.get('access_count', 0) + 1
                new_strength = min(1.0, metadata.get('strength', 0.5) + 0.05)

                self.vector_store.update_memory_metadata(
                    memory_id=memory_id,
                    memory_type=memory_type,
                    updates={
                        'access_count': new_access_count,
                        'strength': new_strength,
                        'last_accessed': datetime.now().isoformat()
                    }
                )

        except Exception as e:
            logger.error(f"Error marking memories as accessed: {e}")

    def format_memories_for_context(
        self,
        memories: List[Tuple[str, Dict[str, Any], float]],
        include_metadata: bool = False
    ) -> str:
        """
        Format retrieved memories as a context string for brain council.

        Args:
            memories: List of retrieved memories
            include_metadata: Include metadata in output (for debug)

        Returns:
            str: Formatted memory context
        """
        if not memories:
            return "No relevant memories found."

        lines = []
        for i, (content, metadata, relevance) in enumerate(memories, 1):
            if include_metadata:
                emotion = metadata.get('primary_emotion', 'neutral')
                location = metadata.get('location', 'unknown')
                lines.append(f"{i}. {content} [emotion: {emotion}, location: {location}, relevance: {relevance:.2f}]")
            else:
                lines.append(f"{i}. {content}")

        return "\n".join(lines)

    def add_to_working_memory(self, content: str) -> None:
        """
        Add an interaction to working memory.

        Args:
            content: Interaction content
        """
        self.working_memory.add(content)

    def get_working_memory_context(self) -> str:
        """
        Get working memory as context string.

        Returns:
            str: Formatted working memory
        """
        return self.working_memory.to_context_string()

    def clear_working_memory(self) -> None:
        """Clear working memory."""
        self.working_memory.clear()
