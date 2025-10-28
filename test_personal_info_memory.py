"""
Test Personal Information Memory - Comprehensive verification

Tests that all types of personal information shared by the trainer
are properly stored as semantic memories with appropriate significance.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import Mock, patch
from memory.consolidation import MemoryConsolidator
from memory.vector_store import VectorMemoryStore
from eevee.state import EeveeState


def print_section(title: str):
    print("\n" + "="*70)
    print(title)
    print("="*70)


def test_name_variations():
    """Test all name introduction variations"""
    print_section("TEST 1: Name Introduction Variations")

    vector_store = VectorMemoryStore()
    consolidation = MemoryConsolidator(
        vector_store=vector_store,
        config={'memory_significance_threshold': 6.0}
    )
    eevee = EeveeState()

    test_cases = [
        "My name is Chris",
        "Call me Chris",
        "I'm called Chris",
        "I am called Christopher",
    ]

    print("\nTesting name introduction patterns:\n")
    all_passed = True
    for user_input in test_cases:
        memories = consolidation.consolidate_memories(
            user_input=user_input,
            eevee_response="*Vee!* Nice to meet you!",
            eevee_state=eevee,
            world_location="trainer_home"
        )

        # Find semantic memory
        semantic = next((m for m in memories if m.memory_type.value == "semantic"), None)

        if semantic and semantic.significance >= 6.0:
            print(f"✅ '{user_input}' → sig:{semantic.significance}, stored:YES")
        else:
            sig = semantic.significance if semantic else "N/A"
            print(f"❌ '{user_input}' → sig:{sig}, stored:NO")
            all_passed = False

    if all_passed:
        print("\n✅ TEST 1 PASSED: All name variations stored properly")
        return True
    else:
        print("\n❌ TEST 1 FAILED: Some name variations not stored")
        return False


def test_preferences():
    """Test preference sharing patterns"""
    print_section("TEST 2: Preference Sharing")

    vector_store = VectorMemoryStore()
    consolidation = MemoryConsolidator(
        vector_store=vector_store,
        config={'memory_significance_threshold': 6.0}
    )
    eevee = EeveeState()

    test_cases = [
        "My favorite color is blue",
        "I prefer coffee over tea",
        "I like playing video games",
        "I dislike loud noises",
        "I love pizza",
        "I hate mornings",
    ]

    print("\nTesting preference patterns:\n")
    all_passed = True
    for user_input in test_cases:
        memories = consolidation.consolidate_memories(
            user_input=user_input,
            eevee_response="*Vee!* *listens attentively*",
            eevee_state=eevee,
            world_location="trainer_home"
        )

        # Find semantic memory
        semantic = next((m for m in memories if m.memory_type.value == "semantic"), None)

        if semantic and semantic.significance >= 6.0:
            print(f"✅ '{user_input}' → sig:{semantic.significance}, stored:YES")
        else:
            sig = semantic.significance if semantic else "N/A"
            print(f"❌ '{user_input}' → sig:{sig}, stored:NO")
            all_passed = False

    if all_passed:
        print("\n✅ TEST 2 PASSED: All preferences stored properly")
        return True
    else:
        print("\n❌ TEST 2 FAILED: Some preferences not stored")
        return False


def test_explicit_remember_requests():
    """Test explicit 'remember' keyword usage"""
    print_section("TEST 3: Explicit Remember Requests")

    vector_store = VectorMemoryStore()
    consolidation = MemoryConsolidator(
        vector_store=vector_store,
        config={'memory_significance_threshold': 6.0}
    )
    eevee = EeveeState()

    test_cases = [
        "Remember that I work from home",
        "Don't forget I'm allergic to peanuts",
        "Please memorize this: I have a cat named Whiskers",
        "Keep in mind I exercise in the morning",
        "Note that I speak Spanish",
    ]

    print("\nTesting explicit remember patterns:\n")
    all_passed = True
    for user_input in test_cases:
        memories = consolidation.consolidate_memories(
            user_input=user_input,
            eevee_response="*Vee!* *nods seriously* I'll remember!",
            eevee_state=eevee,
            world_location="trainer_home"
        )

        # Find semantic memory
        semantic = next((m for m in memories if m.memory_type.value == "semantic"), None)

        if semantic and semantic.significance >= 6.0:
            print(f"✅ '{user_input}' → sig:{semantic.significance}, stored:YES")
        else:
            sig = semantic.significance if semantic else "N/A"
            print(f"❌ '{user_input}' → sig:{sig}, stored:NO")
            all_passed = False

    if all_passed:
        print("\n✅ TEST 3 PASSED: All remember requests stored properly")
        return True
    else:
        print("\n❌ TEST 3 FAILED: Some remember requests not stored")
        return False


def test_significance_levels():
    """Test that different types of info get appropriate significance"""
    print_section("TEST 4: Significance Level Verification")

    vector_store = VectorMemoryStore()
    consolidation = MemoryConsolidator(
        vector_store=vector_store,
        config={'memory_significance_threshold': 6.0}
    )
    eevee = EeveeState()

    # Test cases with expected significance ranges
    test_cases = [
        ("My name is Chris", 6.0, 7.0, "name (should get personal info boost)"),
        ("Remember my birthday is June 15th", 7.0, 8.5, "remember + personal info"),
        ("I like pizza", 6.0, 7.0, "preference (personal info boost)"),
        ("The weather is nice", 4.0, 5.5, "mundane comment (no boost)"),
    ]

    print("\nTesting significance calculation accuracy:\n")
    all_passed = True
    for user_input, min_sig, max_sig, description in test_cases:
        memories = consolidation.consolidate_memories(
            user_input=user_input,
            eevee_response="*Vee!*",
            eevee_state=eevee,
            world_location="trainer_home"
        )

        # Get significance from any memory type
        sig = memories[0].significance if memories else 0.0

        if min_sig <= sig <= max_sig:
            print(f"✅ '{user_input}' → sig:{sig} ({description})")
        else:
            print(f"❌ '{user_input}' → sig:{sig} (expected {min_sig}-{max_sig}) ({description})")
            all_passed = False

    if all_passed:
        print("\n✅ TEST 4 PASSED: Significance levels appropriate")
        return True
    else:
        print("\n❌ TEST 4 FAILED: Some significance levels incorrect")
        return False


def run_all_tests():
    """Run all personal information memory tests"""
    print("\n" + "="*70)
    print("PERSONAL INFORMATION MEMORY TEST SUITE")
    print("Testing: Name, preferences, remember keyword, significance")
    print("="*70)

    tests = [
        ("Name Variations", test_name_variations),
        ("Preferences", test_preferences),
        ("Explicit Remember", test_explicit_remember_requests),
        ("Significance Levels", test_significance_levels),
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
    print("PERSONAL INFORMATION MEMORY TEST RESULTS")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 ALL PERSONAL INFORMATION TESTS PASSED! 🎉")
        print("Eevee will properly remember names, preferences, and explicit requests!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
