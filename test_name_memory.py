"""
Test Name Memory Formation

Test that "My name is Chris" creates a semantic memory properly.
"""

import sys
from datetime import datetime
from memory.consolidation import MemoryConsolidator
from memory.vector_store import VectorMemoryStore
from memory.memory_types import MemoryType

def test_name_memory():
    """Test that name is stored as semantic memory"""
    print("\n" + "="*70)
    print("TEST: 'My name is Chris' Memory Formation")
    print("="*70)

    # Initialize memory system
    vector_store = VectorMemoryStore()
    consolidator = MemoryConsolidator(
        vector_store=vector_store,
        config={'memory_significance_threshold': 6.0}
    )

    # Test input
    user_input = "My name is Chris"
    eevee_response = "*Vee!* Chris! *tail wagging*"

    context = {
        'current_location': 'trainer_home',
        'primary_emotion': 'curious',
        'emotion_intensity': 5.0,
        'physical_state': {
            'hunger': 50,
            'energy': 50,
        },
        'location_safety': 10
    }

    print(f"\nUser input: '{user_input}'")
    print(f"Eevee response: '{eevee_response}'")

    # Calculate significance
    significance = consolidator._calculate_significance(
        user_input=user_input,
        eevee_response=eevee_response,
        context=context,
        council_decision=None
    )

    print(f"\nSignificance calculated: {significance:.1f}")
    print(f"Threshold: 6.0")
    print(f"Will be stored: {'✅ YES' if significance >= 6.0 else '❌ NO'}")

    # Process interaction
    memories = consolidator.process_interaction(
        user_input=user_input,
        eevee_response=eevee_response,
        context=context,
        council_decision=None
    )

    if memories:
        print(f"\n✓ Formed {len(memories)} memor{'y' if len(memories) == 1 else 'ies'}:")
        for memory in memories:
            print(f"\n  Type: {memory.memory_type.value}")
            print(f"  Content: {memory.content}")
            print(f"  Significance: {memory.significance:.1f}")
            if memory.memory_type == MemoryType.SEMANTIC:
                print(f"  Category: {memory.fact_category}")
                print(f"  Confidence: {memory.confidence}")

        # Check for semantic memory with trainer_identity
        semantic_memories = [m for m in memories if m.memory_type == MemoryType.SEMANTIC]
        if semantic_memories:
            identity_memories = [m for m in semantic_memories if m.fact_category == "trainer_identity"]
            if identity_memories:
                print("\n✅ TEST PASSED: Name stored as trainer_identity semantic memory")
                return True
            else:
                print(f"\n⚠️  Semantic memory created but wrong category: {semantic_memories[0].fact_category}")
                print(f"   Expected: trainer_identity")
                return False
        else:
            print("\n❌ TEST FAILED: No semantic memory created for name")
            return False
    else:
        print(f"\n❌ TEST FAILED: No memories formed")
        print(f"   Significance {significance:.1f} did not meet threshold")
        return False


def test_name_variations():
    """Test different ways of saying name"""
    print("\n" + "="*70)
    print("TEST: Name Variation Patterns")
    print("="*70)

    vector_store = VectorMemoryStore()
    consolidator = MemoryConsolidator(
        vector_store=vector_store,
        config={'memory_significance_threshold': 6.0}
    )

    context = {
        'current_location': 'trainer_home',
        'primary_emotion': 'curious',
        'emotion_intensity': 5.0,
        'physical_state': {'hunger': 50, 'energy': 50},
        'location_safety': 10
    }

    test_cases = [
        "My name is Chris",
        "my name is Chris",
        "MY NAME IS CHRIS",
        "My name is chris",
        "Call me Chris",
        "I'm called Chris",
    ]

    results = []
    for test_input in test_cases:
        significance = consolidator._calculate_significance(
            user_input=test_input,
            eevee_response="*Vee!*",
            context=context,
            council_decision=None
        )

        memories = consolidator.process_interaction(
            user_input=test_input,
            eevee_response="*Vee!*",
            context=context,
            council_decision=None
        )

        has_semantic = any(m.memory_type == MemoryType.SEMANTIC for m in memories) if memories else False

        status = "✅" if has_semantic else "❌"
        print(f"{status} '{test_input}' → sig:{significance:.1f}, semantic:{has_semantic}")
        results.append(has_semantic)

    if all(results):
        print("\n✅ TEST PASSED: All name variations create semantic memories")
        return True
    else:
        failed = sum(1 for r in results if not r)
        print(f"\n❌ TEST FAILED: {failed}/{len(results)} variations failed")
        return False


def test_retrieval():
    """Test that we can retrieve the name memory"""
    print("\n" + "="*70)
    print("TEST: Name Memory Retrieval")
    print("="*70)

    from memory.retrieval import MemoryRetriever

    vector_store = VectorMemoryStore()
    consolidator = MemoryConsolidator(
        vector_store=vector_store,
        config={'memory_significance_threshold': 6.0}
    )

    retriever = MemoryRetriever(
        vector_store=vector_store,
        config={'memory_retrieval_count': 5, 'min_significance': 4.0}
    )

    # Store the name
    context = {
        'current_location': 'trainer_home',
        'primary_emotion': 'curious',
        'emotion_intensity': 5.0,
        'physical_state': {'hunger': 50, 'energy': 50},
        'location_safety': 10
    }

    print("\n✓ Storing: 'My name is Chris'")
    memories = consolidator.process_interaction(
        user_input="My name is Chris",
        eevee_response="*Vee!* Chris!",
        context=context,
        council_decision=None
    )

    if not memories:
        print("❌ Failed to store memory")
        return False

    print(f"✓ Stored {len(memories)} memor{'y' if len(memories) == 1 else 'ies'}")

    # Try to retrieve it
    print("\n✓ Querying: 'What is my name?'")
    results = retriever.search_memories("What is my name?", limit=5)

    if results:
        print(f"\n✓ Retrieved {len(results)} result(s):")
        for content, metadata, relevance in results[:3]:
            print(f"  - {content[:80]}... (relevance: {relevance:.2f})")

        # Check if "Chris" is in any result
        has_chris = any("Chris" in content or "chris" in content for content, _, _ in results)
        if has_chris:
            print("\n✅ TEST PASSED: Name memory retrieved successfully")
            return True
        else:
            print("\n❌ TEST FAILED: Retrieved memories don't contain 'Chris'")
            return False
    else:
        print("\n❌ TEST FAILED: No memories retrieved")
        return False


def run_all_tests():
    """Run all name memory tests"""
    print("\n" + "="*70)
    print("NAME MEMORY TEST SUITE")
    print("Testing: 'My name is Chris' memory formation and retrieval")
    print("="*70)

    tests = [
        ("Name Memory Formation", test_name_memory),
        ("Name Variations", test_name_variations),
        ("Name Retrieval", test_retrieval),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ TEST ERROR: {name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Print summary
    print("\n" + "="*70)
    print("NAME MEMORY TEST RESULTS")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 ALL NAME MEMORY TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("\nDiagnosis needed - name memory formation may have issues")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
