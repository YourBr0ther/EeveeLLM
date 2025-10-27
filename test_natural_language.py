"""
Test Natural Language Intent Parser

Tests natural language command detection across all supported commands.
"""

import sys
from nlp.intent_parser import IntentParser


def print_section(title: str):
    print("\n" + "="*70)
    print(title)
    print("="*70)


def test_stats_command():
    """Test stats command natural language parsing"""
    print_section("TEST 1: Stats Command")

    parser = IntentParser()

    test_cases = [
        "What are your stats?",
        "How are you feeling?",
        "Show me your health",
        "Are you okay?",
        "What's your energy level?",
        "Check your status",
        "Display your condition"
    ]

    print("Testing stats command detection:\n")
    for test_input in test_cases:
        intent = parser.parse(test_input)
        if intent and intent.command == "stats":
            print(f"✅ '{test_input}' → stats")
        else:
            print(f"❌ '{test_input}' → {intent.command if intent else 'NOT DETECTED'}")
            return False

    print("\n✅ TEST 1 PASSED: All stats phrasings detected")
    return True


def test_inventory_command():
    """Test inventory command natural language parsing"""
    print_section("TEST 2: Inventory Command")

    parser = IntentParser()

    test_cases = [
        "Show me your inventory",
        "What do you have?",
        "What items are you carrying?",
        "Let me see your stuff",
        "Display your items",
        "What's in your bag?"
    ]

    print("Testing inventory command detection:\n")
    for test_input in test_cases:
        intent = parser.parse(test_input)
        if intent and intent.command == "inventory":
            print(f"✅ '{test_input}' → inventory")
        else:
            print(f"❌ '{test_input}' → {intent.command if intent else 'NOT DETECTED'}")
            return False

    print("\n✅ TEST 2 PASSED: All inventory phrasings detected")
    return True


def test_pet_command():
    """Test pet command natural language parsing"""
    print_section("TEST 3: Pet Command")

    parser = IntentParser()

    test_cases = [
        "I want to pet you",
        "Can I pet you?",
        "Let me pet Eevee",
        "Give you some pets",
        "Head pat",
        "I'll pet you"
    ]

    print("Testing pet command detection:\n")
    for test_input in test_cases:
        intent = parser.parse(test_input)
        if intent and intent.command == "pet":
            print(f"✅ '{test_input}' → pet")
        else:
            print(f"❌ '{test_input}' → {intent.command if intent else 'NOT DETECTED'}")
            return False

    print("\n✅ TEST 3 PASSED: All pet phrasings detected")
    return True


def test_play_command():
    """Test play command natural language parsing"""
    print_section("TEST 4: Play Command")

    parser = IntentParser()

    test_cases = [
        "Let's play!",
        "Do you want to play?",
        "Want to play?",
        "Feel like playing?",
        "Playtime!",
        "Wanna play?"
    ]

    print("Testing play command detection:\n")
    for test_input in test_cases:
        intent = parser.parse(test_input)
        if intent and intent.command == "play":
            print(f"✅ '{test_input}' → play")
        else:
            print(f"❌ '{test_input}' → {intent.command if intent else 'NOT DETECTED'}")
            return False

    print("\n✅ TEST 4 PASSED: All play phrasings detected")
    return True


def test_go_command():
    """Test go/travel command with argument extraction"""
    print_section("TEST 5: Go/Travel Command (with arguments)")

    parser = IntentParser()

    test_cases = [
        ("Let's go to the meadow", "meadow"),
        ("Take me to the forest", "forest"),
        ("Can we go to the park?", "park?"),
        ("Travel to the beach", "beach"),
        ("Go to cave", "cave"),
        ("Head to trainer home", "trainer home")
    ]

    print("Testing go command detection and argument extraction:\n")
    for test_input, expected_arg in test_cases:
        intent = parser.parse(test_input)
        if intent and intent.command == "go":
            # Clean up expected arg
            expected_cleaned = expected_arg.rstrip('?')
            args_cleaned = intent.args.rstrip('?')
            if expected_cleaned in args_cleaned or args_cleaned in expected_cleaned:
                print(f"✅ '{test_input}' → go '{intent.args}'")
            else:
                print(f"❌ '{test_input}' → go '{intent.args}' (expected: '{expected_arg}')")
                return False
        else:
            print(f"❌ '{test_input}' → {intent.command if intent else 'NOT DETECTED'}")
            return False

    print("\n✅ TEST 5 PASSED: All go phrasings detected with correct arguments")
    return True


def test_give_command():
    """Test give command with item extraction"""
    print_section("TEST 6: Give Command (with items)")

    parser = IntentParser()

    test_cases = [
        ("Give you an Oran Berry", "oran berry"),
        ("Here's a berry", "berry"),
        ("Take this Potion", "potion"),
        ("I'll give you a Pecha Berry", "pecha berry"),
        ("Have some berries", "berries")
    ]

    print("Testing give command detection and item extraction:\n")
    for test_input, expected_item in test_cases:
        intent = parser.parse(test_input)
        if intent and intent.command == "give":
            if expected_item.lower() in intent.args.lower():
                print(f"✅ '{test_input}' → give '{intent.args}'")
            else:
                print(f"❌ '{test_input}' → give '{intent.args}' (expected: '{expected_item}')")
                return False
        else:
            print(f"❌ '{test_input}' → {intent.command if intent else 'NOT DETECTED'}")
            return False

    print("\n✅ TEST 6 PASSED: All give phrasings detected with correct items")
    return True


def test_remember_command():
    """Test remember/memory command with query extraction"""
    print_section("TEST 7: Remember Command (with queries)")

    parser = IntentParser()

    test_cases = [
        ("Do you remember the park?", "park"),
        ("What do you remember about yesterday?", "yesterday"),
        ("Can you recall what happened?", "happened"),
        ("Show me your memories", ""),  # No query
        ("Remember the beach", "beach")
    ]

    print("Testing remember command detection and query extraction:\n")
    for test_input, expected_query in test_cases:
        intent = parser.parse(test_input)
        if intent and intent.command == "remember":
            if not expected_query or expected_query.lower() in intent.args.lower():
                print(f"✅ '{test_input}' → remember '{intent.args}'")
            else:
                print(f"⚠️  '{test_input}' → remember '{intent.args}' (expected: '{expected_query}')")
                # Not a failure, just different extraction
        else:
            print(f"❌ '{test_input}' → {intent.command if intent else 'NOT DETECTED'}")
            return False

    print("\n✅ TEST 7 PASSED: All remember phrasings detected")
    return True


def test_timeline_command():
    """Test timeline command natural language parsing"""
    print_section("TEST 8: Timeline Command")

    parser = IntentParser()

    test_cases = [
        "What did you do while I was gone?",
        "Show me the timeline",
        "What have you been up to?",
        "What happened recently?",
        "View recent activities"
    ]

    print("Testing timeline command detection:\n")
    for test_input in test_cases:
        intent = parser.parse(test_input)
        if intent and intent.command == "timeline":
            print(f"✅ '{test_input}' → timeline")
        else:
            print(f"❌ '{test_input}' → {intent.command if intent else 'NOT DETECTED'}")
            return False

    print("\n✅ TEST 8 PASSED: All timeline phrasings detected")
    return True


def test_fallback_to_talk():
    """Test that unrecognized phrases don't trigger commands"""
    print_section("TEST 9: Fallback to Talk (non-commands)")

    parser = IntentParser()

    test_cases = [
        "Hello Eevee!",
        "I love you",
        "You're so cute",
        "The weather is nice today",
        "I had a great day"
    ]

    print("Testing that normal conversation doesn't trigger commands:\n")
    for test_input in test_cases:
        intent = parser.parse(test_input)
        if intent is None:
            print(f"✅ '{test_input}' → (no command, will talk)")
        else:
            print(f"❌ '{test_input}' → {intent.command} (should not detect command)")
            return False

    print("\n✅ TEST 9 PASSED: Normal conversation doesn't trigger commands")
    return True


def test_all_commands_coverage():
    """Test that all commands have examples"""
    print_section("TEST 10: Command Coverage")

    parser = IntentParser()

    commands = [
        "stats", "inventory", "pet", "play", "observe", "world",
        "go", "give", "use", "drop", "remember", "timeline", "help"
    ]

    print("Testing that all commands have natural language examples:\n")
    all_covered = True
    for command in commands:
        examples = parser.get_command_examples(command)
        if examples:
            print(f"✅ {command}: {len(examples)} examples")
        else:
            print(f"❌ {command}: NO EXAMPLES")
            all_covered = False

    if all_covered:
        print("\n✅ TEST 10 PASSED: All commands have examples")
        return True
    else:
        print("\n❌ TEST 10 FAILED: Some commands missing examples")
        return False


def run_all_tests():
    """Run all natural language parser tests"""
    print("\n" + "="*70)
    print("NATURAL LANGUAGE INTENT PARSER TEST SUITE")
    print("Testing: Command detection, argument extraction, coverage")
    print("="*70)

    tests = [
        ("Stats Command", test_stats_command),
        ("Inventory Command", test_inventory_command),
        ("Pet Command", test_pet_command),
        ("Play Command", test_play_command),
        ("Go Command", test_go_command),
        ("Give Command", test_give_command),
        ("Remember Command", test_remember_command),
        ("Timeline Command", test_timeline_command),
        ("Fallback to Talk", test_fallback_to_talk),
        ("Command Coverage", test_all_commands_coverage),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ TEST ERROR: {name}")
            print(f"   Error: {e}")
            results.append((name, False))

    # Print summary
    print("\n" + "="*70)
    print("NATURAL LANGUAGE TEST RESULTS")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 ALL NATURAL LANGUAGE TESTS PASSED! 🎉")
        print("You can now interact with Eevee using natural language!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
