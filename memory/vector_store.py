"""
Vector Storage using ChromaDB for semantic memory retrieval

This module wraps ChromaDB to provide semantic similarity search for memories.
Memories are stored as vector embeddings, allowing retrieval of contextually
relevant memories even when exact keywords don't match.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import os
import logging
from pathlib import Path

from memory.memory_types import Memory, MemoryType

logger = logging.getLogger(__name__)


class VectorMemoryStore:
    """
    ChromaDB wrapper for storing and retrieving memories via semantic similarity.

    Uses sentence transformers for embedding generation (default: all-MiniLM-L6-v2)
    Stores memories in persistent ChromaDB collection at data/chroma_data/
    """

    def __init__(self, persist_directory: str = "data/chroma_data"):
        """
        Initialize ChromaDB client and collections.

        Args:
            persist_directory: Directory for ChromaDB persistence
        """
        self.persist_directory = persist_directory

        # Create directory if it doesn't exist
        Path(persist_directory).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Create separate collections for each memory type
        # This allows type-specific retrieval and better organization
        self.collections = {}
        for memory_type in MemoryType:
            collection_name = f"eevee_memories_{memory_type.value}"
            try:
                self.collections[memory_type] = self.client.get_or_create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"}  # Cosine similarity for semantic search
                )
                logger.info(f"Initialized collection: {collection_name}")
            except Exception as e:
                logger.error(f"Error creating collection {collection_name}: {e}")
                raise

    def store_memory(self, memory: Memory) -> bool:
        """
        Store a memory in the vector database.

        Args:
            memory: Memory object to store

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            collection = self.collections[memory.memory_type]

            # Prepare metadata (ChromaDB requires string, int, float, or bool values)
            metadata = {
                "timestamp": memory.timestamp.isoformat(),
                "significance": memory.significance,
                "emotion_intensity": memory.emotion_intensity,
                "location": memory.location or "",
                "strength": memory.strength,
                "access_count": memory.access_count,
                "primary_emotion": memory.primary_emotion.value if memory.primary_emotion else "",
                "tags": ",".join(memory.tags) if memory.tags else ""
            }

            # Add type-specific metadata
            if hasattr(memory, 'event_type'):
                metadata["event_type"] = memory.event_type
            if hasattr(memory, 'fact_category'):
                metadata["fact_category"] = memory.fact_category
                metadata["confidence"] = memory.confidence
            if hasattr(memory, 'trigger'):
                metadata["trigger"] = memory.trigger
            if hasattr(memory, 'behavior_name'):
                metadata["behavior_name"] = memory.behavior_name
                metadata["success_rate"] = memory.success_rate

            # Store in ChromaDB (it will generate embeddings automatically)
            collection.add(
                documents=[memory.content],
                metadatas=[metadata],
                ids=[memory.memory_id]
            )

            logger.debug(f"Stored memory {memory.memory_id} (type: {memory.memory_type.value})")
            return True

        except Exception as e:
            logger.error(f"Error storing memory {memory.memory_id}: {e}")
            return False

    def retrieve_similar(
        self,
        query: str,
        memory_type: Optional[MemoryType] = None,
        n_results: int = 5,
        min_significance: float = 0.0,
        where_filter: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        Retrieve similar memories using semantic search.

        Args:
            query: Text query to search for
            memory_type: Specific memory type to search (None = all types)
            n_results: Number of results to return
            min_significance: Minimum significance threshold
            where_filter: Additional metadata filters

        Returns:
            List of tuples: (memory_content, metadata, similarity_score)
        """
        try:
            results = []

            # Determine which collections to search
            collections_to_search = (
                [self.collections[memory_type]] if memory_type
                else self.collections.values()
            )

            for collection in collections_to_search:
                # Build filter
                where = where_filter or {}
                # Note: ChromaDB filters use specific operators
                # We'll apply min_significance filter after retrieval for simplicity

                # Query the collection
                query_results = collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    where=where if where else None
                )

                # Process results
                if query_results and query_results['documents']:
                    for i, doc in enumerate(query_results['documents'][0]):
                        metadata = query_results['metadatas'][0][i]
                        distance = query_results['distances'][0][i] if query_results.get('distances') else 0.0

                        # Convert distance to similarity score (1.0 = perfect match, 0.0 = no match)
                        similarity = 1.0 - distance

                        # Apply significance filter
                        if metadata.get('significance', 0.0) >= min_significance:
                            results.append((doc, metadata, similarity))

            # Sort by similarity score (highest first)
            results.sort(key=lambda x: x[2], reverse=True)

            # Return top n_results
            return results[:n_results]

        except Exception as e:
            logger.error(f"Error retrieving memories: {e}")
            return []

    def retrieve_by_emotion(
        self,
        emotion: str,
        n_results: int = 5,
        memory_type: Optional[MemoryType] = None
    ) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        Retrieve memories associated with a specific emotion.

        Args:
            emotion: Emotion type to filter by
            n_results: Number of results to return
            memory_type: Optional memory type filter

        Returns:
            List of tuples: (memory_content, metadata, similarity_score)
        """
        where_filter = {"primary_emotion": emotion}
        return self.retrieve_similar(
            query=f"memories about {emotion}",
            memory_type=memory_type,
            n_results=n_results,
            where_filter=where_filter
        )

    def retrieve_by_location(
        self,
        location: str,
        n_results: int = 5,
        memory_type: Optional[MemoryType] = None
    ) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        Retrieve memories from a specific location.

        Args:
            location: Location to filter by
            n_results: Number of results to return
            memory_type: Optional memory type filter

        Returns:
            List of tuples: (memory_content, metadata, similarity_score)
        """
        where_filter = {"location": location}
        return self.retrieve_similar(
            query=f"memories at {location}",
            memory_type=memory_type,
            n_results=n_results,
            where_filter=where_filter
        )

    def get_all_memories_by_type(
        self,
        memory_type: MemoryType,
        limit: int = 100
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Get all memories of a specific type (for browsing).

        Args:
            memory_type: Type of memory to retrieve
            limit: Maximum number of memories to return

        Returns:
            List of tuples: (memory_content, metadata)
        """
        try:
            collection = self.collections[memory_type]

            # Get all items (ChromaDB doesn't have a direct "get all" with limit)
            # We'll use a generic query
            results = collection.get(
                limit=limit,
                include=["documents", "metadatas"]
            )

            memories = []
            if results and results['documents']:
                for i, doc in enumerate(results['documents']):
                    metadata = results['metadatas'][i]
                    memories.append((doc, metadata))

            # Sort by timestamp (most recent first)
            memories.sort(
                key=lambda x: x[1].get('timestamp', ''),
                reverse=True
            )

            return memories

        except Exception as e:
            logger.error(f"Error getting all memories: {e}")
            return []

    def update_memory_metadata(
        self,
        memory_id: str,
        memory_type: MemoryType,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update metadata for an existing memory (e.g., strength, access_count).

        Args:
            memory_id: ID of memory to update
            memory_type: Type of memory
            updates: Dictionary of metadata updates

        Returns:
            bool: True if successful
        """
        try:
            collection = self.collections[memory_type]

            # Get current metadata
            result = collection.get(ids=[memory_id], include=["metadatas"])

            if not result or not result['metadatas']:
                logger.warning(f"Memory {memory_id} not found")
                return False

            current_metadata = result['metadatas'][0]

            # Apply updates
            current_metadata.update(updates)

            # Update in ChromaDB
            collection.update(
                ids=[memory_id],
                metadatas=[current_metadata]
            )

            logger.debug(f"Updated memory {memory_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating memory {memory_id}: {e}")
            return False

    def delete_memory(self, memory_id: str, memory_type: MemoryType) -> bool:
        """
        Delete a memory from the vector store.

        Args:
            memory_id: ID of memory to delete
            memory_type: Type of memory

        Returns:
            bool: True if successful
        """
        try:
            collection = self.collections[memory_type]
            collection.delete(ids=[memory_id])
            logger.debug(f"Deleted memory {memory_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting memory {memory_id}: {e}")
            return False

    def get_memory_count(self, memory_type: Optional[MemoryType] = None) -> int:
        """
        Get total count of memories.

        Args:
            memory_type: Specific type (None = all types)

        Returns:
            int: Total memory count
        """
        try:
            if memory_type:
                return self.collections[memory_type].count()
            else:
                return sum(col.count() for col in self.collections.values())

        except Exception as e:
            logger.error(f"Error counting memories: {e}")
            return 0

    def clear_all_memories(self) -> bool:
        """
        Clear all memories from all collections (use with caution!).

        Returns:
            bool: True if successful
        """
        try:
            for memory_type, collection in self.collections.items():
                # Get all IDs and delete them
                result = collection.get(include=[])
                if result and result.get('ids'):
                    collection.delete(ids=result['ids'])
                    logger.info(f"Cleared {len(result['ids'])} memories from {memory_type.value}")
                else:
                    logger.info(f"No memories to clear from {memory_type.value}")

            return True

        except Exception as e:
            logger.error(f"Error clearing memories: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored memories.

        Returns:
            Dict with memory counts by type and other stats
        """
        stats = {
            "total_memories": 0,
            "by_type": {}
        }

        for memory_type in MemoryType:
            count = self.get_memory_count(memory_type)
            stats["by_type"][memory_type.value] = count
            stats["total_memories"] += count

        return stats
