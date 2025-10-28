"""
Test Command Responses - Verify commands use Eevee's brain council

Tests that commands like stats, inventory, and world now generate
natural responses from Eevee instead of just system messages.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch
from main import EeveeLLM


def test_stats_command_has_eevee_response():
    """Test that stats command generates Eevee response"""
    print("\n" + "="*70)
    print("TEST 1: Stats Command Has Eevee Response")
    print("="*70)

    with patch('main.TerminalUI') as mock_ui, \
         patch('main.NanoGPTClient') as mock_llm, \
         patch('main.VectorMemoryStore'):

        # Create app instance
        app = EeveeLLM()

        # Mock the response generator to track calls
        mock_response = "*Vee!* *sits up proudly* I'm doing well!"
        app.response_gen.generate_response = Mock(return_value=(mock_response, None))

        # Call show_stats
        print("\n✓ Calling show_stats()...")
        app.show_stats()

        # Verify generate_response was called
        if app.response_gen.generate_response.called:
            call_args = app.response_gen.generate_response.call_args
            message = call_args[0][0]  # First positional argument
            print(f"✓ generate_response called with: '{message}'")
            print(f"✓ Eevee response would be: '{mock_response}'")
            print("\n✅ TEST 1 PASSED: Stats command uses Eevee response")
            return True
        else:
            print("\n❌ TEST 1 FAILED: Stats command did not call generate_response")
            return False


def test_world_command_has_eevee_response():
    """Test that world command generates Eevee response"""
    print("\n" + "="*70)
    print("TEST 2: World Command Has Eevee Response")
    print("="*70)

    with patch('main.TerminalUI') as mock_ui, \
         patch('main.NanoGPTClient') as mock_llm, \
         patch('main.VectorMemoryStore'):

        # Create app instance
        app = EeveeLLM()

        # Mock the response generator
        mock_response = "*Vee!* *looks around curiously* This place is nice!"
        app.response_gen.generate_response = Mock(return_value=(mock_response, None))

        # Call show_world
        print("\n✓ Calling show_world()...")
        app.show_world()

        # Verify generate_response was called
        if app.response_gen.generate_response.called:
            call_args = app.response_gen.generate_response.call_args
            message = call_args[0][0]
            print(f"✓ generate_response called with: '{message}'")
            print(f"✓ Eevee response would be: '{mock_response}'")
            print("\n✅ TEST 2 PASSED: World command uses Eevee response")
            return True
        else:
            print("\n❌ TEST 2 FAILED: World command did not call generate_response")
            return False


def test_inventory_command_has_eevee_response():
    """Test that inventory command generates Eevee response"""
    print("\n" + "="*70)
    print("TEST 3: Inventory Command Has Eevee Response")
    print("="*70)

    with patch('main.TerminalUI') as mock_ui, \
         patch('main.NanoGPTClient') as mock_llm, \
         patch('main.VectorMemoryStore'):

        # Create app instance
        app = EeveeLLM()

        # Add an item to inventory
        app.eevee_state.add_item("test_item")

        # Mock the response generator
        mock_response = "*Vee!* *shows items proudly* Look what I have!"
        app.response_gen.generate_response = Mock(return_value=(mock_response, None))

        # Call show_inventory
        print("\n✓ Calling show_inventory()...")
        app.show_inventory()

        # Verify generate_response was called
        if app.response_gen.generate_response.called:
            call_args = app.response_gen.generate_response.call_args
            message = call_args[0][0]
            print(f"✓ generate_response called with: '{message}'")
            print(f"✓ Eevee response would be: '{mock_response}'")
            print("\n✅ TEST 3 PASSED: Inventory command uses Eevee response")
            return True
        else:
            print("\n❌ TEST 3 FAILED: Inventory command did not call generate_response")
            return False


def test_existing_commands_still_work():
    """Test that existing commands with Eevee responses still work"""
    print("\n" + "="*70)
    print("TEST 4: Existing Commands Still Use Eevee Responses")
    print("="*70)

    with patch('main.TerminalUI') as mock_ui, \
         patch('main.NanoGPTClient') as mock_llm, \
         patch('main.VectorMemoryStore'):

        # Create app instance
        app = EeveeLLM()

        # Mock the response generator
        mock_response = "*Vee!* *purrs happily*"
        app.response_gen.generate_response = Mock(return_value=(mock_response, None))

        # Test pet command
        print("\n✓ Testing pet command...")
        app.pet_eevee()

        if app.response_gen.generate_response.called:
            print("✓ Pet command uses Eevee response")

            # Reset mock
            app.response_gen.generate_response.reset_mock()
            app.response_gen.describe_action = Mock(return_value=mock_response)

            # Test play command
            print("✓ Testing play command...")
            app.play_with_eevee()

            if app.response_gen.describe_action.called:
                print("✓ Play command uses Eevee response")
                print("\n✅ TEST 4 PASSED: Existing commands still work")
                return True
            else:
                print("\n❌ TEST 4 FAILED: Play command broken")
                return False
        else:
            print("\n❌ TEST 4 FAILED: Pet command broken")
            return False


def run_all_tests():
    """Run all command response tests"""
    print("\n" + "="*70)
    print("COMMAND RESPONSE TEST SUITE")
    print("Testing: Commands use Eevee's brain council for responses")
    print("="*70)

    tests = [
        ("Stats Command", test_stats_command_has_eevee_response),
        ("World Command", test_world_command_has_eevee_response),
        ("Inventory Command", test_inventory_command_has_eevee_response),
        ("Existing Commands", test_existing_commands_still_work),
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
    print("COMMAND RESPONSE TEST RESULTS")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 ALL COMMAND RESPONSE TESTS PASSED! 🎉")
        print("Commands now use Eevee's natural responses!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
