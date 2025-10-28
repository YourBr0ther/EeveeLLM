#!/usr/bin/env python3
"""
Test that "how are you?" gives a natural response without showing stats table.

This ensures conversations feel natural rather than robotic.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from io import StringIO
import unittest
from unittest.mock import patch, MagicMock
from main import EeveeLLM


class TestConversationalStats(unittest.TestCase):
    """Test natural language stats requests vs explicit stats command"""

    def setUp(self):
        """Set up test fixtures"""
        self.eevee = EeveeLLM()

    def test_natural_language_no_table(self):
        """
        When user asks "how are you?", should NOT display stats table.
        Should only give a natural conversational response.
        """
        # Mock the response generation to avoid LLM call
        with patch.object(self.eevee.response_gen, 'generate_response') as mock_gen:
            mock_gen.return_value = ("I'm doing great! *wags tail*", {})

            # Mock print_detailed_stats to check if it's called
            with patch.object(self.eevee.ui, 'print_detailed_stats') as mock_stats:
                # Simulate natural language: "how are you?"
                with patch('sys.stdout', new_callable=StringIO):
                    self.eevee.process_command("How are you feeling?")

                # Stats table should NOT be displayed
                mock_stats.assert_not_called()

                # Response should be generated with conversational prompt
                mock_gen.assert_called_once()
                call_args = mock_gen.call_args[0]
                self.assertIn("asking", call_args[0].lower())

    def test_explicit_command_shows_table(self):
        """
        When user explicitly types 'stats', should display stats table.
        """
        # Mock the response generation to avoid LLM call
        with patch.object(self.eevee.response_gen, 'generate_response') as mock_gen:
            mock_gen.return_value = ("*tilts head* You're checking on me?", {})

            # Mock print_detailed_stats to check if it's called
            with patch.object(self.eevee.ui, 'print_detailed_stats') as mock_stats:
                # Explicit command: "stats"
                with patch('sys.stdout', new_callable=StringIO):
                    self.eevee.process_command("stats")

                # Stats table SHOULD be displayed
                mock_stats.assert_called_once()

                # Response should be generated with stats check prompt
                mock_gen.assert_called_once()
                call_args = mock_gen.call_args[0]
                self.assertIn("checking", call_args[0].lower())

    def test_various_natural_phrasings(self):
        """
        Test various natural phrasings all avoid showing table.
        """
        natural_phrasings = [
            "How are you?",
            "Are you okay?",
            "How are you feeling?",
            "What's your energy level?"
        ]

        for phrase in natural_phrasings:
            with self.subTest(phrase=phrase):
                # Mock the response generation
                with patch.object(self.eevee.response_gen, 'generate_response') as mock_gen:
                    mock_gen.return_value = ("I'm good!", {})

                    # Mock print_detailed_stats
                    with patch.object(self.eevee.ui, 'print_detailed_stats') as mock_stats:
                        with patch('sys.stdout', new_callable=StringIO):
                            self.eevee.process_command(phrase)

                        # Should NOT show table
                        mock_stats.assert_not_called()


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("TESTING: Conversational Stats (Natural vs Explicit)")
    print("=" * 70)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestConversationalStats)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
        print(f"   Ran {result.testsRun} tests successfully")
        print()
        print("Natural language ('how are you?') will NOT show stats table ✓")
        print("Explicit command ('stats') WILL show stats table ✓")
    else:
        print("❌ SOME TESTS FAILED")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
