#!/usr/bin/env python3
"""
Test "Remember" Keyword Fix
Verify that Eevee properly stores facts when user says "remember" or shares preferences
"""
import sys
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def test_remember_keyword():
    """Test that 'remember' keyword boosts significance"""
    from memory import VectorMemoryStore, MemoryConsolidator

    logger.info("\n" + "=" * 70)
    logger.info("TEST 1: 'Remember' Keyword Significance Boost")
    logger.info("=" * 70)

    store = VectorMemoryStore(persist_directory="data/test_chroma_remember")
    config = {'memory_significance_threshold': 6.0}
    consolidator = MemoryConsolidator(vector_store=store, config=config)

    # Test input with "remember"
    user_input = "Remember that my favorite color is green"
    eevee_response = "*Vee!* *nods*"
    context = {
        'physical_state': {'hunger': 50, 'energy': 50, 'health': 100, 'happiness': 60},
        'relationship': {'trust': 50, 'bond': 40},
        'location_safety': 10,
        'current_location': 'trainer_home'
    }

    # Process interaction
    memories = consolidator.process_interaction(
        user_input=user_input,
        eevee_response=eevee_response,
        context=context,
        council_decision=None
    )

    logger.info(f"✓ User input: '{user_input}'")
    logger.info(f"✓ Memories formed: {len(memories) if memories else 0}")

    if memories:
        for memory in memories:
            logger.info(f"  - {memory.memory_type.value}: {memory.content[:60]}...")
            logger.info(f"    Significance: {memory.significance:.1f}")

    # Check if semantic memory was created
    semantic_found = False
    if memories:
        for memory in memories:
            if memory.memory_type.value == "semantic":
                semantic_found = True
                if "favorite color is green" in memory.content.lower():
                    logger.info("\n✅ TEST 1 PASSED: Semantic memory created for trainer fact")
                    return True

    logger.error("\n❌ TEST 1 FAILED: No semantic memory created")
    return False


def test_favorite_keyword():
    """Test that 'favorite' keyword creates semantic memory"""
    from memory import VectorMemoryStore, MemoryConsolidator

    logger.info("\n" + "=" * 70)
    logger.info("TEST 2: 'Favorite' Keyword Detection")
    logger.info("=" * 70)

    store = VectorMemoryStore(persist_directory="data/test_chroma_remember")
    config = {'memory_significance_threshold': 6.0}
    consolidator = MemoryConsolidator(vector_store=store, config=config)

    # Test without "remember" but with "favorite"
    user_input = "My favorite food is pizza"
    eevee_response = "*Vee vee!*"
    context = {
        'physical_state': {'hunger': 50, 'energy': 50, 'health': 100, 'happiness': 60},
        'relationship': {'trust': 50, 'bond': 40},
        'location_safety': 10,
        'current_location': 'trainer_home'
    }

    memories = consolidator.process_interaction(
        user_input=user_input,
        eevee_response=eevee_response,
        context=context,
        council_decision=None
    )

    logger.info(f"✓ User input: '{user_input}'")
    logger.info(f"✓ Memories formed: {len(memories) if memories else 0}")

    if memories:
        for memory in memories:
            logger.info(f"  - {memory.memory_type.value}: {memory.content[:60]}...")
            logger.info(f"    Significance: {memory.significance:.1f}")

    # Check if semantic memory was created
    semantic_found = False
    if memories:
        for memory in memories:
            if memory.memory_type.value == "semantic":
                semantic_found = True
                if "favorite food is pizza" in memory.content.lower():
                    logger.info("\n✅ TEST 2 PASSED: Semantic memory created for favorite")
                    return True

    logger.error("\n❌ TEST 2 FAILED: No semantic memory created")
    return False


def test_retrieval_of_fact():
    """Test that stored facts can be retrieved"""
    from memory import VectorMemoryStore, MemoryRetriever

    logger.info("\n" + "=" * 70)
    logger.info("TEST 3: Fact Retrieval")
    logger.info("=" * 70)

    store = VectorMemoryStore(persist_directory="data/test_chroma_remember")
    config = {
        'memory_retrieval_count': 5,
        'memory_significance_threshold': 6.0,
        'max_working_memory': 10
    }
    retriever = MemoryRetriever(vector_store=store, config=config)

    # Try to retrieve the fact about favorite color
    context = {
        'current_location': 'trainer_home',
        'physical_state': {'hunger': 50, 'energy': 50}
    }

    results = retriever.retrieve_relevant_memories(
        situation="What is my favorite color?",
        context=context
    )

    logger.info(f"✓ Retrieved {len(results)} memories for 'What is my favorite color?'")

    for i, (content, metadata, relevance) in enumerate(results, 1):
        logger.info(f"  {i}. {content[:60]}...")
        logger.info(f"     Relevance: {relevance:.2f}")

    # Check if favorite color is in results
    color_found = False
    for content, metadata, relevance in results:
        if "favorite color" in content.lower() and "green" in content.lower():
            color_found = True
            break

    if color_found:
        logger.info("\n✅ TEST 3 PASSED: Fact retrieved correctly")
        return True
    else:
        logger.error("\n❌ TEST 3 FAILED: Favorite color not found in retrieval")
        return False


def test_name_memory():
    """Test that trainer name is remembered"""
    from memory import VectorMemoryStore, MemoryConsolidator

    logger.info("\n" + "=" * 70)
    logger.info("TEST 4: Trainer Name Memory")
    logger.info("=" * 70)

    store = VectorMemoryStore(persist_directory="data/test_chroma_remember")
    config = {'memory_significance_threshold': 6.0}
    consolidator = MemoryConsolidator(vector_store=store, config=config)

    user_input = "My name is Alex"
    eevee_response = "*Vee!* *excited tail wagging*"
    context = {
        'physical_state': {'hunger': 50, 'energy': 50, 'health': 100, 'happiness': 70},
        'relationship': {'trust': 60, 'bond': 50},
        'location_safety': 10,
        'current_location': 'trainer_home'
    }

    memories = consolidator.process_interaction(
        user_input=user_input,
        eevee_response=eevee_response,
        context=context,
        council_decision=None
    )

    logger.info(f"✓ User input: '{user_input}'")
    logger.info(f"✓ Memories formed: {len(memories) if memories else 0}")

    if memories:
        for memory in memories:
            logger.info(f"  - {memory.memory_type.value}: {memory.content[:60]}...")
            if hasattr(memory, 'fact_category'):
                logger.info(f"    Category: {memory.fact_category}")

    # Check if name memory was created with correct category
    name_found = False
    if memories:
        for memory in memories:
            if (memory.memory_type.value == "semantic" and
                hasattr(memory, 'fact_category') and
                memory.fact_category == "trainer_identity"):
                name_found = True
                break

    if name_found:
        logger.info("\n✅ TEST 4 PASSED: Trainer name stored as identity fact")
        return True
    else:
        logger.error("\n❌ TEST 4 FAILED: Name not properly categorized")
        return False


def cleanup_test_data():
    """Clean up test ChromaDB data"""
    import shutil
    test_dir = Path("data/test_chroma_remember")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        logger.info("\n✓ Cleaned up test data")


def main():
    """Run all remember fix tests"""
    logger.info("=" * 70)
    logger.info("'REMEMBER' KEYWORD FIX TEST SUITE")
    logger.info("Testing: significance boost, semantic memory, fact retrieval")
    logger.info("=" * 70)

    results = []

    try:
        results.append(("Remember Keyword Boost", test_remember_keyword()))
    except Exception as e:
        logger.error(f"❌ Test 1 crashed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Remember Keyword Boost", False))

    try:
        results.append(("Favorite Keyword Detection", test_favorite_keyword()))
    except Exception as e:
        logger.error(f"❌ Test 2 crashed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Favorite Keyword Detection", False))

    try:
        results.append(("Fact Retrieval", test_retrieval_of_fact()))
    except Exception as e:
        logger.error(f"❌ Test 3 crashed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Fact Retrieval", False))

    try:
        results.append(("Trainer Name Memory", test_name_memory()))
    except Exception as e:
        logger.error(f"❌ Test 4 crashed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Trainer Name Memory", False))

    # Cleanup
    try:
        cleanup_test_data()
    except Exception as e:
        logger.warning(f"Could not cleanup test data: {e}")

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("'REMEMBER' FIX TEST RESULTS")
    logger.info("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")

    logger.info(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        logger.info("\n🎉 ALL 'REMEMBER' TESTS PASSED! 🎉")
        logger.info("Eevee will now remember facts when you say 'remember' or share preferences!")
        return 0
    else:
        logger.error(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
