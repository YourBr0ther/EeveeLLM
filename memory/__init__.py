"""
Memory Module - Vector-based memory storage and retrieval (Phase 3)

This module provides:
- Vector storage using ChromaDB for semantic memory retrieval
- 4 memory types: Episodic, Semantic, Emotional, Procedural
- Memory consolidation (significance-based long-term storage)
- Context-aware memory retrieval for the Hippocampus
- Working memory for recent interactions
"""

from memory.memory_types import (
    Memory, MemoryType, EmotionType,
    EpisodicMemory, SemanticMemory, EmotionalMemory, ProceduralMemory,
    WorkingMemory
)
from memory.vector_store import VectorMemoryStore
from memory.retrieval import MemoryRetriever
from memory.consolidation import MemoryConsolidator

__all__ = [
    'Memory', 'MemoryType', 'EmotionType',
    'EpisodicMemory', 'SemanticMemory', 'EmotionalMemory', 'ProceduralMemory',
    'WorkingMemory',
    'VectorMemoryStore',
    'MemoryRetriever',
    'MemoryConsolidator'
]
