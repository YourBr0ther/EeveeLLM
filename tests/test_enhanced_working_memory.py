"""
Test Enhanced Working Memory - 7-day retention with 100-interaction capacity

Tests:
1. Time-based retention (7 days)
2. Capacity limit (100 interactions)
3. Automatic cleanup of old memories
4. get_memories_since() functionality
5. Persistence (to_dict/from_dict)
"""

import sys
from datetime import datetime, timedelta
from memory.memory_types import WorkingMemory, WorkingMemoryItem


def print_section(title: str):
    print("\n" + "="*70)
    print(title)
    print("="*70)


def test_capacity_increase():
    """Test 1: Verify capacity increased from 10 to 100"""
    print_section("TEST 1: Capacity Increase (10 → 100)")

    wm = WorkingMemory()

    # Add 50 interactions
    for i in range(50):
        wm.add(f"Interaction {i+1}: Casual conversation")

    print(f"✓ Added 50 interactions")
    print(f"✓ Working memory size: {len(wm.memories)}")
    print(f"✓ Max capacity: {wm.max_size}")

    assert len(wm.memories) == 50, "Should store all 50 interactions"
    assert wm.max_size == 100, "Max capacity should be 100"

    print("\n✅ TEST 1 PASSED: Capacity increased to 100")
    return True


def test_time_based_retention():
    """Test 2: Verify 7-day time-based retention"""
    print_section("TEST 2: Time-Based Retention (7 days)")

    wm = WorkingMemory()

    # Add memories with different ages
    now = datetime.now()

    # 1 day old
    old_item_1day = WorkingMemoryItem(
        content="1 day old: I went to the store",
        timestamp=now - timedelta(days=1)
    )
    wm.memories.append(old_item_1day)

    # 3 days old
    old_item_3days = WorkingMemoryItem(
        content="3 days old: We played at the park",
        timestamp=now - timedelta(days=3)
    )
    wm.memories.append(old_item_3days)

    # 6 days old
    old_item_6days = WorkingMemoryItem(
        content="6 days old: I bought groceries",
        timestamp=now - timedelta(days=6)
    )
    wm.memories.append(old_item_6days)

    # 8 days old (should be removed)
    old_item_8days = WorkingMemoryItem(
        content="8 days old: This should be forgotten",
        timestamp=now - timedelta(days=8)
    )
    wm.memories.append(old_item_8days)

    # Fresh memory (today)
    wm.add("Today: Just chatting")

    print(f"✓ Added memories aged: today, 1 day, 3 days, 6 days, 8 days")

    # Trigger cleanup
    all_memories = wm.get_all()

    print(f"✓ Memories after cleanup: {len(all_memories)}")
    for mem in all_memories:
        print(f"  - {mem}")

    assert len(all_memories) == 4, "Should keep 4 memories (8-day-old removed)"
    assert "8 days old" not in str(all_memories), "8-day-old memory should be gone"
    assert "6 days old" in str(all_memories), "6-day-old memory should remain"

    print("\n✅ TEST 2 PASSED: 7-day retention working")
    return True


def test_capacity_limit():
    """Test 3: Verify 100-interaction capacity limit"""
    print_section("TEST 3: Capacity Limit (100 max)")

    wm = WorkingMemory()

    # Add 120 interactions (exceeds limit)
    for i in range(120):
        wm.add(f"Interaction {i+1}")

    all_memories = wm.get_all()

    print(f"✓ Added 120 interactions")
    print(f"✓ Working memory size: {len(all_memories)}")
    print(f"✓ Oldest memory: {all_memories[0]}")
    print(f"✓ Newest memory: {all_memories[-1]}")

    assert len(all_memories) == 100, "Should cap at 100 interactions"
    assert "Interaction 21" in all_memories[0], "Should have removed first 20"
    assert "Interaction 120" in all_memories[-1], "Should keep most recent"

    print("\n✅ TEST 3 PASSED: Capacity limit enforced")
    return True


def test_get_memories_since():
    """Test 4: Verify get_memories_since() functionality"""
    print_section("TEST 4: get_memories_since() Method")

    wm = WorkingMemory()
    now = datetime.now()

    # Add memories at different times
    for days_ago in [0, 1, 2, 3, 4, 5, 6]:
        item = WorkingMemoryItem(
            content=f"Memory from {days_ago} days ago",
            timestamp=now - timedelta(days=days_ago)
        )
        wm.memories.append(item)

    # Get memories from last 1 day
    last_1_day = wm.get_memories_since(days=1)
    print(f"✓ Memories from last 1 day: {len(last_1_day)}")
    for mem in last_1_day:
        print(f"  - {mem}")

    # Get memories from last 3 days
    last_3_days = wm.get_memories_since(days=3)
    print(f"\n✓ Memories from last 3 days: {len(last_3_days)}")
    for mem in last_3_days:
        print(f"  - {mem}")

    assert len(last_1_day) == 1, "Should have 1 memory from last day"
    assert len(last_3_days) == 3, "Should have 3 memories from last 3 days"

    print("\n✅ TEST 4 PASSED: get_memories_since() working")
    return True


def test_persistence():
    """Test 5: Verify to_dict/from_dict persistence"""
    print_section("TEST 5: Persistence (to_dict/from_dict)")

    wm = WorkingMemory()

    # Add some memories
    wm.add("I went to the store")
    wm.add("We played at the park")
    wm.add("I had lunch")

    print(f"✓ Created working memory with {len(wm.memories)} items")

    # Convert to dict
    wm_dict = wm.to_dict()
    print(f"✓ Converted to dict: {len(wm_dict['memories'])} memories stored")

    # Recreate from dict
    wm_loaded = WorkingMemory.from_dict(wm_dict)
    print(f"✓ Loaded from dict: {len(wm_loaded.memories)} memories restored")

    # Verify
    assert len(wm_loaded.memories) == 3, "Should restore all 3 memories"
    assert wm_loaded.max_size == 100, "Should restore max_size"
    assert wm_loaded.max_age_days == 7, "Should restore max_age_days"

    original_contents = [item.content for item in wm.memories]
    loaded_contents = [item.content for item in wm_loaded.memories]
    assert original_contents == loaded_contents, "Contents should match"

    print("\n✓ Original memories:")
    for mem in wm.get_all():
        print(f"  - {mem}")

    print("\n✓ Loaded memories:")
    for mem in wm_loaded.get_all():
        print(f"  - {mem}")

    print("\n✅ TEST 5 PASSED: Persistence working")
    return True


def test_context_string():
    """Test 6: Verify enhanced to_context_string()"""
    print_section("TEST 6: Context String Generation")

    wm = WorkingMemory()

    # Add 15 interactions
    for i in range(15):
        wm.add(f"Interaction {i+1}: Casual talk")

    # Get context string with default (10 recent)
    context = wm.to_context_string()
    print(f"✓ Generated context string (default 10 recent):")
    print(context)

    lines = context.split('\n')
    assert len(lines) == 10, "Should show 10 most recent"
    assert "Interaction 15" in context, "Should include most recent"
    assert "Interaction 6" in context, "Should include 10th most recent"
    assert "Interaction 5" not in context, "Should not include older than 10"

    print("\n✓ Context includes last 10 interactions ✓")

    # Get context string with custom count
    context_5 = wm.to_context_string(recent_count=5)
    print(f"\n✓ Generated context string (5 recent):")
    print(context_5)

    lines_5 = context_5.split('\n')
    assert len(lines_5) == 5, "Should show 5 most recent"

    print("\n✅ TEST 6 PASSED: Context string working")
    return True


def run_all_tests():
    """Run all enhanced working memory tests"""
    print("\n" + "="*70)
    print("ENHANCED WORKING MEMORY TEST SUITE")
    print("Testing: 7-day retention, 100-interaction capacity")
    print("="*70)

    tests = [
        ("Capacity Increase", test_capacity_increase),
        ("Time-Based Retention", test_time_based_retention),
        ("Capacity Limit", test_capacity_limit),
        ("get_memories_since()", test_get_memories_since),
        ("Persistence", test_persistence),
        ("Context String", test_context_string),
    ]

    results = []
    for name, test_func in tests:
        try:
            test_func()
            results.append((name, True))
        except AssertionError as e:
            print(f"\n❌ TEST FAILED: {name}")
            print(f"   Error: {e}")
            results.append((name, False))
        except Exception as e:
            print(f"\n❌ TEST ERROR: {name}")
            print(f"   Error: {e}")
            results.append((name, False))

    # Print summary
    print("\n" + "="*70)
    print("ENHANCED WORKING MEMORY TEST RESULTS")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 ALL ENHANCED WORKING MEMORY TESTS PASSED! 🎉")
        print("Eevee can now remember mundane conversations for up to 7 days!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
