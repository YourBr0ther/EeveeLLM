#!/usr/bin/env python3
"""
Test critical bug fixes from UX changes bug review.

Tests:
1. Bug #1: Timeline validation for missing keys
2. Bug #2: print_stat_bar() prints instead of returns
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from io import StringIO
import unittest
from unittest.mock import patch, MagicMock
from main import EeveeLLM
from ui import TerminalUI


class TestCriticalBugFixes(unittest.TestCase):
    """Test the 2 critical bugs from UX changes"""

    def setUp(self):
        """Set up test fixtures"""
        self.eevee = EeveeLLM()
        self.ui = TerminalUI(use_color=False)

    def test_timeline_with_missing_keys(self):
        """
        Bug #1: Timeline should handle missing keys gracefully.

        Test that show_timeline() validates data structure and doesn't crash.
        """
        # Test 1: Missing all keys
        self.eevee.last_timeline_data = {}

        # Capture actual behavior
        with patch('sys.stdout', new_callable=StringIO):
            self.eevee.show_timeline(detailed=False)
            # Should not crash - that's the key test
            # The validation prevents KeyError

    def test_timeline_with_partial_keys_summary(self):
        """
        Bug #1: Timeline summary view should check for all 4 required keys.
        """
        # Missing 'items_found' and 'net_changes' for summary view
        self.eevee.last_timeline_data = {
            'activities': [],
            'hours_elapsed': 5.0
        }

        # Capture actual behavior - should not crash
        with patch('sys.stdout', new_callable=StringIO):
            self.eevee.show_timeline(detailed=False)
            # Should not crash - validation prevents KeyError

    def test_timeline_with_partial_keys_detail(self):
        """
        Bug #1: Timeline detail view only needs 2 keys (activities, hours_elapsed).
        """
        # Simplify - just test that validation allows detail view with 2 keys
        # Empty activities list should work
        self.eevee.last_timeline_data = {
            'activities': [],
            'hours_elapsed': 2.0
        }

        # Should not crash with just these keys in detail mode
        with patch('sys.stdout', new_callable=StringIO):
            self.eevee.show_timeline(detailed=True)
            # Should not crash - validation allows these 2 keys for detail

    def test_timeline_with_all_keys(self):
        """
        Bug #1: Timeline should work normally with all keys present.
        """
        # Test with all required keys for summary view
        self.eevee.last_timeline_data = {
            'activities': [],
            'hours_elapsed': 3.0,
            'net_changes': {'energy': -10, 'hunger': 15},
            'items_found': ['Oran Berry']
        }

        # Should work without errors
        with patch('sys.stdout', new_callable=StringIO):
            self.eevee.show_timeline(detailed=False)
            # Should not crash - all keys present

    def test_print_stat_bar_prints_directly(self):
        """
        Bug #2: print_stat_bar() should print directly, not return a string.

        This ensures consistency with other print_* methods.
        """
        # Capture stdout
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.ui.print_stat_bar("Health", 85, emoji="❤️")

            # Should return None (not a string)
            self.assertIsNone(result)

            # Should have printed to stdout
            output = mock_stdout.getvalue()
            self.assertIn("Health", output)
            self.assertIn("85%", output)
            self.assertIn("❤️", output)

    def test_print_stat_bar_with_low_value(self):
        """
        Bug #2: print_stat_bar() should handle low values correctly.
        """
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.ui.print_stat_bar("Energy", 25, emoji="⚡")

            # Should return None
            self.assertIsNone(result)

            # Should show low value context
            output = mock_stdout.getvalue()
            self.assertIn("25%", output)
            self.assertIn("Energy", output)

    def test_print_stat_bar_reverse_mode(self):
        """
        Bug #2: print_stat_bar() should handle reverse mode (hunger).
        """
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.ui.print_stat_bar("Hunger", 80, emoji="🍖", reverse=True)

            # Should return None
            self.assertIsNone(result)

            # Should show hunger context
            output = mock_stdout.getvalue()
            self.assertIn("80%", output)
            self.assertIn("hunger", output.lower())
            # Case-insensitive check
            self.assertTrue("very hungry" in output.lower())

    def test_no_timeline_data(self):
        """
        Bug #1: Timeline should handle missing attribute gracefully.
        """
        # Remove timeline data entirely
        if hasattr(self.eevee, 'last_timeline_data'):
            delattr(self.eevee, 'last_timeline_data')

        with patch.object(self.eevee.ui, 'print_info') as mock_info:
            self.eevee.show_timeline(detailed=False)
            # Should print info message, not crash
            mock_info.assert_called_once()
            info_msg = mock_info.call_args[0][0]
            self.assertIn("No recent timeline", info_msg)


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("TESTING: Critical Bug Fixes from UX Changes")
    print("=" * 70)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCriticalBugFixes)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✅ ALL CRITICAL BUG FIXES VERIFIED!")
        print(f"   Ran {result.testsRun} tests successfully")
    else:
        print("❌ SOME TESTS FAILED")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
