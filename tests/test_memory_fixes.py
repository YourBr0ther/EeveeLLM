#!/usr/bin/env python3
"""
Test Memory System Fixes (Phase A Critical Fixes)
Tests:
1. Memory ID in metadata
2. Memory deduplication
3. Working memory integration
4. Optimized retrieval limits
"""
import sys
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def test_memory_id_in_metadata():
    """Test that memory_id and memory_type are stored in metadata"""
    from memory import VectorMemoryStore
    from memory.memory_types import EpisodicMemory, MemoryType, EmotionType
    import uuid

    logger.info("\n" + "=" * 70)
    logger.info("TEST 1: Memory ID in Metadata")
    logger.info("=" * 70)

    # Use temp directory for testing
    store = VectorMemoryStore(persist_directory="data/test_chroma")

    # Create a test memory
    test_memory = EpisodicMemory(
        memory_id=str(uuid.uuid4()),
        memory_type=MemoryType.EPISODIC,
        content="Test memory for metadata fix",
        timestamp=datetime.now(),
        significance=8.0,
        primary_emotion=EmotionType.JOY,
        location="test_location",
        event_type="test"
    )

    # Store it
    success = store.store_memory(test_memory)
    assert success, "Failed to store memory"
    logger.info("✓ Memory stored successfully")

    # Retrieve it
    results = store.retrieve_similar("Test memory", n_results=1)
    assert len(results) > 0, "Failed to retrieve memory"

    content, metadata, similarity = results[0]
    logger.info(f"✓ Retrieved memory: {content[:50]}...")

    # Check metadata has memory_id and memory_type
    memory_id = metadata.get('memory_id')
    memory_type = metadata.get('memory_type')

    logger.info(f"  memory_id: {memory_id}")
    logger.info(f"  memory_type: {memory_type}")

    if memory_id and memory_type:
        logger.info("\n✅ TEST 1 PASSED: memory_id and memory_type are in metadata")
        return True
    else:
        logger.error("\n❌ TEST 1 FAILED: Missing memory_id or memory_type in metadata")
        return False


def test_memory_deduplication():
    """Test that duplicate memories are not added to results"""
    from memory import VectorMemoryStore, MemoryRetriever
    from memory.memory_types import EpisodicMemory, MemoryType, EmotionType
    import uuid

    logger.info("\n" + "=" * 70)
    logger.info("TEST 2: Memory Deduplication")
    logger.info("=" * 70)

    store = VectorMemoryStore(persist_directory="data/test_chroma")
    config = {
        'memory_retrieval_count': 5,
        'memory_significance_threshold': 6.0,
        'max_working_memory': 100
    }
    retriever = MemoryRetriever(vector_store=store, config=config)

    # Create multiple memories at same location with high significance
    location = "test_duplicate_location"
    memory_ids = []

    for i in range(3):
        test_memory = EpisodicMemory(
            memory_id=str(uuid.uuid4()),
            memory_type=MemoryType.EPISODIC,
            content=f"Event {i} at {location} - unique content {i}",
            timestamp=datetime.now(),
            significance=8.0,
            primary_emotion=EmotionType.JOY,
            location=location,
            event_type="test"
        )
        memory_ids.append(test_memory.memory_id)
        store.store_memory(test_memory)
        logger.info(f"✓ Stored memory {i+1}: {test_memory.memory_id[:8]}...")

    # Retrieve with context that triggers multiple search paths
    context = {
        'current_location': location,
        'primary_emotion': 'joy',
        'physical_state': {'hunger': 30, 'energy': 70}
    }

    results = retriever.retrieve_relevant_memories(
        situation=f"Something happened at {location}",
        context=context
    )

    logger.info(f"\n✓ Retrieved {len(results)} memories")

    # Check for duplicates by memory_id
    seen_ids = set()
    duplicates = []

    for content, metadata, relevance in results:
        mem_id = metadata.get('memory_id')
        if mem_id:
            if mem_id in seen_ids:
                duplicates.append(mem_id)
            else:
                seen_ids.add(mem_id)
            logger.info(f"  Memory: {mem_id[:8]}... - {content[:40]}...")

    if len(duplicates) == 0:
        logger.info("\n✅ TEST 2 PASSED: No duplicate memories in results")
        return True
    else:
        logger.error(f"\n❌ TEST 2 FAILED: Found {len(duplicates)} duplicate memories")
        return False


def test_working_memory_integration():
    """Test that working memory is included in context"""
    from memory import MemoryRetriever, VectorMemoryStore
    import uuid

    logger.info("\n" + "=" * 70)
    logger.info("TEST 3: Working Memory Integration")
    logger.info("=" * 70)

    store = VectorMemoryStore(persist_directory="data/test_chroma")
    config = {
        'memory_retrieval_count': 5,
        'memory_significance_threshold': 6.0,
        'max_working_memory': 100
    }
    retriever = MemoryRetriever(vector_store=store, config=config)

    # Add items to working memory
    test_interactions = [
        "User: Hello Eevee!",
        "Eevee: *Vee!* *tail wagging*",
        "User: Want to play?",
        "Eevee: *excited jumping*"
    ]

    for interaction in test_interactions:
        retriever.add_to_working_memory(interaction)
        logger.info(f"✓ Added to working memory: {interaction}")

    # Check working memory contains items
    working_mem_context = retriever.get_working_memory_context()

    logger.info(f"\n✓ Working memory context:\n{working_mem_context}")

    # Verify all interactions are present
    all_present = all(interaction in working_mem_context for interaction in test_interactions)

    if all_present and len(working_mem_context) > 0:
        logger.info("\n✅ TEST 3 PASSED: Working memory integration works")
        return True
    else:
        logger.error("\n❌ TEST 3 FAILED: Working memory not properly integrated")
        return False


def test_optimized_retrieval():
    """Test that retrieval doesn't over-fetch"""
    from memory import VectorMemoryStore, MemoryRetriever
    from memory.memory_types import EpisodicMemory, MemoryType
    import uuid

    logger.info("\n" + "=" * 70)
    logger.info("TEST 4: Optimized Retrieval Limits")
    logger.info("=" * 70)

    store = VectorMemoryStore(persist_directory="data/test_chroma")
    config = {
        'memory_retrieval_count': 3,  # Request only 3 memories
        'memory_significance_threshold': 6.0,
        'max_working_memory': 100
    }
    retriever = MemoryRetriever(vector_store=store, config=config)

    # Create 10 memories
    for i in range(10):
        test_memory = EpisodicMemory(
            memory_id=str(uuid.uuid4()),
            memory_type=MemoryType.EPISODIC,
            content=f"Optimization test memory {i}",
            timestamp=datetime.now(),
            significance=7.0,
            location="test_opt",
            event_type="test"
        )
        store.store_memory(test_memory)

    logger.info("✓ Created 10 test memories")

    # Retrieve with limit of 3
    context = {
        'current_location': 'test_opt',
        'physical_state': {'hunger': 30, 'energy': 70}
    }

    results = retriever.retrieve_relevant_memories(
        situation="optimization test",
        context=context
    )

    logger.info(f"✓ Retrieved {len(results)} memories (requested 3)")

    # Should not exceed requested limit significantly
    if len(results) <= 5:  # Allow small margin (location/emotion bonuses)
        logger.info("\n✅ TEST 4 PASSED: Retrieval respects limits")
        return True
    else:
        logger.error(f"\n❌ TEST 4 FAILED: Over-retrieved ({len(results)} > 5 expected)")
        return False


def cleanup_test_data():
    """Clean up test ChromaDB data"""
    import shutil
    test_dir = Path("data/test_chroma")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        logger.info("\n✓ Cleaned up test data")


def main():
    """Run all memory fix tests"""
    logger.info("=" * 70)
    logger.info("MEMORY SYSTEM FIXES TEST SUITE (Phase A)")
    logger.info("Testing: metadata, deduplication, working memory, optimization")
    logger.info("=" * 70)

    results = []

    try:
        results.append(("Memory ID in Metadata", test_memory_id_in_metadata()))
    except Exception as e:
        logger.error(f"❌ Test 1 crashed: {e}")
        results.append(("Memory ID in Metadata", False))

    try:
        results.append(("Memory Deduplication", test_memory_deduplication()))
    except Exception as e:
        logger.error(f"❌ Test 2 crashed: {e}")
        results.append(("Memory Deduplication", False))

    try:
        results.append(("Working Memory Integration", test_working_memory_integration()))
    except Exception as e:
        logger.error(f"❌ Test 3 crashed: {e}")
        results.append(("Working Memory Integration", False))

    try:
        results.append(("Optimized Retrieval", test_optimized_retrieval()))
    except Exception as e:
        logger.error(f"❌ Test 4 crashed: {e}")
        results.append(("Optimized Retrieval", False))

    # Cleanup
    try:
        cleanup_test_data()
    except Exception as e:
        logger.warning(f"Could not cleanup test data: {e}")

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("MEMORY FIXES TEST RESULTS")
    logger.info("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")

    logger.info(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        logger.info("\n🎉 ALL MEMORY FIXES WORKING! 🎉")
        return 0
    else:
        logger.error(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
