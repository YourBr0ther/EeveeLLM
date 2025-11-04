#!/usr/bin/env python3
"""
Test suite for ProactiveManager functionality

Tests the proactive interaction system that allows Eevee to initiate conversations
and express needs autonomously.
"""

import sys
import os
import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from eevee.proactive import ProactiveManager, ProactiveEventType, ProactiveLevel, ProactiveEvent


class MockEeveeState:
    """Mock EeveeState for testing"""

    def __init__(self, hunger=50, energy=50, happiness=50, health=50):
        self.hunger = hunger
        self.energy = energy
        self.happiness = happiness
        self.health = health
        self.location = "trainer_home"


class TestProactiveManager(unittest.TestCase):
    """Test ProactiveManager functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            'proactive_level': 'normal',
            'min_absence_for_greeting': 1800,  # 30 minutes
            'max_proactive_events_per_hour': 3
        }
        self.manager = ProactiveManager(self.config)
        self.mock_state = MockEeveeState()
        self.context = {'test': True}

    def test_initialization(self):
        """Test ProactiveManager initialization"""
        self.assertEqual(self.manager.proactive_level, ProactiveLevel.NORMAL)
        self.assertEqual(self.manager.min_absence_for_greeting, 1800)
        self.assertEqual(self.manager.max_proactive_events_per_hour, 3)
        self.assertTrue(self.manager.user_is_present)

    def test_user_interaction_tracking(self):
        """Test user interaction and absence tracking"""
        # Initially user is present
        self.assertTrue(self.manager.user_is_present)

        # Mark user interaction
        old_time = self.manager.last_user_interaction
        self.manager.mark_user_interaction()
        new_time = self.manager.last_user_interaction
        self.assertGreater(new_time, old_time)

        # Mark user as absent
        self.manager.mark_user_absence()
        self.assertFalse(self.manager.user_is_present)

    def test_greeting_opportunity_detection(self):
        """Test greeting when user returns after absence"""
        # Simulate user being absent for 31 minutes
        self.manager.last_user_interaction = datetime.now() - timedelta(minutes=31)
        self.manager.user_is_present = True  # User just returned

        # Check for greeting
        event = self.manager._check_greeting_opportunity(self.mock_state, self.context)

        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, ProactiveEventType.GREETING)
        self.assertGreater(event.urgency, 0.5)
        self.assertIn("absence_duration", event.context)

    def test_no_greeting_for_short_absence(self):
        """Test no greeting for short absence"""
        # Simulate user being absent for only 10 minutes
        self.manager.last_user_interaction = datetime.now() - timedelta(minutes=10)
        self.manager.user_is_present = True

        event = self.manager._check_greeting_opportunity(self.mock_state, self.context)
        self.assertIsNone(event)

    def test_urgent_hunger_detection(self):
        """Test urgent hunger need expression"""
        # Set very low hunger
        self.mock_state.hunger = 5

        event = self.manager._check_urgent_needs(self.mock_state, self.context)

        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, ProactiveEventType.NEED_EXPRESSION)
        self.assertEqual(event.context['need_type'], 'hunger')
        self.assertGreater(event.urgency, 0.8)  # Very urgent

    def test_urgent_energy_detection(self):
        """Test urgent energy need expression"""
        # Set very low energy
        self.mock_state.energy = 8

        event = self.manager._check_urgent_needs(self.mock_state, self.context)

        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, ProactiveEventType.NEED_EXPRESSION)
        self.assertEqual(event.context['need_type'], 'energy')
        self.assertGreater(event.urgency, 0.6)

    def test_urgent_happiness_detection(self):
        """Test urgent happiness need expression"""
        # Set very low happiness
        self.mock_state.happiness = 15

        event = self.manager._check_urgent_needs(self.mock_state, self.context)

        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, ProactiveEventType.NEED_EXPRESSION)
        self.assertEqual(event.context['need_type'], 'happiness')
        self.assertGreater(event.urgency, 0.4)

    def test_no_urgent_needs_when_healthy(self):
        """Test no urgent needs when Eevee is healthy"""
        # Set good stats
        self.mock_state.hunger = 80
        self.mock_state.energy = 75
        self.mock_state.happiness = 85

        event = self.manager._check_urgent_needs(self.mock_state, self.context)
        self.assertIsNone(event)

    def test_rate_limiting(self):
        """Test rate limiting prevents spam"""
        # Create an event and execute it
        event = ProactiveEvent(
            event_type=ProactiveEventType.GREETING,
            message="Test greeting",
            urgency=0.5,
            context={},
            timestamp=datetime.now()
        )

        self.manager.execute_proactive_event(event)

        # Immediately check if another event should be allowed
        # Should be blocked by rate limiting
        self.assertFalse(self.manager._should_allow_proactive_event())

    def test_proactive_level_effects(self):
        """Test different proactive levels affect frequency"""
        # Test quiet level
        quiet_manager = ProactiveManager({'proactive_level': 'quiet'})
        quiet_interval = quiet_manager._get_min_event_interval()

        # Test chatty level
        chatty_manager = ProactiveManager({'proactive_level': 'chatty'})
        chatty_interval = chatty_manager._get_min_event_interval()

        # Quiet should have longer intervals than chatty
        self.assertGreater(quiet_interval, chatty_interval)

    def test_mood_assessment(self):
        """Test mood assessment based on state"""
        # Test very happy mood
        self.mock_state.happiness = 90
        self.mock_state.energy = 85
        self.mock_state.health = 95
        mood = self.manager._assess_mood(self.mock_state)
        self.assertEqual(mood, "very_happy")

        # Test down mood
        self.mock_state.happiness = 20
        self.mock_state.energy = 15
        self.mock_state.health = 25
        mood = self.manager._assess_mood(self.mock_state)
        self.assertEqual(mood, "down")

    def test_attention_seeking_with_loneliness(self):
        """Test attention seeking when lonely"""
        # Simulate user being away for 2 hours
        self.manager.last_user_interaction = datetime.now() - timedelta(hours=2)

        # Use a deterministic random seed for testing
        with patch('random.random', return_value=0.1):  # Force event to trigger
            event = self.manager._check_attention_seeking(self.mock_state, self.context)

            self.assertIsNotNone(event)
            self.assertEqual(event.event_type, ProactiveEventType.ATTENTION_SEEKING)
            self.assertIn("loneliness_factor", event.context)

    def test_statistics_tracking(self):
        """Test statistics tracking"""
        initial_stats = self.manager.get_stats()

        # Execute a greeting event
        greeting_event = ProactiveEvent(
            event_type=ProactiveEventType.GREETING,
            message="Hello!",
            urgency=0.7,
            context={},
            timestamp=datetime.now()
        )

        self.manager.execute_proactive_event(greeting_event)

        updated_stats = self.manager.get_stats()

        # Check that greeting count increased
        self.assertEqual(updated_stats['total_greetings'], 1)
        self.assertEqual(updated_stats['recent_events_count'], 1)

    def test_event_context_preservation(self):
        """Test that event context is preserved correctly"""
        # Test hunger event context
        self.mock_state.hunger = 5
        event = self.manager._check_urgent_needs(self.mock_state, self.context)

        self.assertIsNotNone(event)
        self.assertEqual(event.context['need_type'], 'hunger')
        self.assertEqual(event.context['value'], 5)

    @patch('random.choice')
    def test_message_generation_variety(self, mock_choice):
        """Test that message generation has variety"""
        mock_choice.return_value = "Test message"

        # Test hunger message generation
        message = self.manager._generate_hunger_message(5)
        self.assertEqual(message, "Test message")
        mock_choice.assert_called()

    def test_full_proactive_check_integration(self):
        """Test the full proactive event checking flow"""
        # Set up scenario: user away for long time, Eevee is hungry
        self.manager.last_user_interaction = datetime.now() - timedelta(hours=1)
        self.manager.last_proactive_event = datetime.now() - timedelta(hours=2)  # Allow event
        self.manager.user_is_present = True
        self.mock_state.hunger = 10  # Very hungry

        # This should trigger a greeting (user returning) or hunger expression
        event = self.manager.check_for_proactive_events(self.mock_state, self.context)

        self.assertIsNotNone(event)
        # Should be either greeting or need expression
        self.assertIn(event.event_type, [ProactiveEventType.GREETING, ProactiveEventType.NEED_EXPRESSION])


def run_tests():
    """Run all proactive manager tests"""
    print("🧪 Running ProactiveManager Tests...")
    print("=" * 50)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestProactiveManager)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All ProactiveManager tests passed!")
        print(f"📊 Tests run: {result.testsRun}")
    else:
        print("❌ Some ProactiveManager tests failed!")
        print(f"📊 Tests run: {result.testsRun}")
        print(f"🔥 Failures: {len(result.failures)}")
        print(f"💥 Errors: {len(result.errors)}")

        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")

        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)