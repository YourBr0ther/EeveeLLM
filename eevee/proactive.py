"""
Proactive Interaction Manager for EeveeLLM

Handles Eevee-initiated conversations, notifications, and contextual reactions.
This makes Eevee feel more like a real pet that can reach out and express needs.
"""

import random
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class ProactiveEventType(Enum):
    """Types of proactive events Eevee can initiate"""
    GREETING = "greeting"                    # When user returns after absence
    NEED_EXPRESSION = "need_expression"      # Expressing hunger, tiredness, etc.
    EMOTIONAL_SHARE = "emotional_share"      # Sharing feelings or mood
    MEMORY_MENTION = "memory_mention"        # Bringing up past experiences
    STATUS_UPDATE = "status_update"          # Telling about current activities
    ATTENTION_SEEKING = "attention_seeking"  # Just wanting interaction
    CELEBRATION = "celebration"              # Happy about achievements
    CONCERN = "concern"                      # Worried about low stats


class ProactiveLevel(Enum):
    """How proactive Eevee should be"""
    QUIET = "quiet"        # Minimal proactive behavior
    NORMAL = "normal"      # Balanced proactive behavior
    CHATTY = "chatty"      # High proactive behavior
    VERY_CHATTY = "very_chatty"  # Maximum proactive behavior


@dataclass
class ProactiveEvent:
    """Represents a proactive event Eevee wants to initiate"""
    event_type: ProactiveEventType
    message: str
    urgency: float  # 0.0-1.0, how urgent this event is
    context: Dict[str, Any]
    timestamp: datetime

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ProactiveManager:
    """
    Manages Eevee's proactive interactions and autonomous communication.

    This system allows Eevee to:
    - Greet users when they return
    - Express needs and emotions unprompted
    - Share memories and experiences
    - Seek attention when lonely
    - React to state changes
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize ProactiveManager.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Configuration
        self.proactive_level = ProactiveLevel(
            self.config.get('proactive_level', 'normal')
        )
        self.min_absence_for_greeting = self.config.get(
            'min_absence_for_greeting', 1800  # 30 minutes
        )
        self.max_proactive_events_per_hour = self.config.get(
            'max_proactive_events_per_hour', 3
        )

        # State tracking
        self.last_user_interaction = datetime.now()
        self.last_proactive_event = datetime.now()
        self.pending_events: List[ProactiveEvent] = []
        self.recent_events: List[ProactiveEvent] = []
        self.user_is_present = True

        # Statistics
        self.total_greetings = 0
        self.total_need_expressions = 0
        self.total_emotional_shares = 0

        logger.info(f"ProactiveManager initialized with level: {self.proactive_level.value}")

    def mark_user_interaction(self):
        """Call this whenever the user interacts"""
        self.last_user_interaction = datetime.now()
        self.user_is_present = True
        logger.debug("User interaction marked - user is present")

    def mark_user_absence(self):
        """Call this when user goes idle/absent"""
        self.user_is_present = False
        logger.debug("User marked as absent")

    def check_for_proactive_events(self, eevee_state, context: Dict[str, Any]) -> Optional[ProactiveEvent]:
        """
        Check if Eevee should initiate any proactive interactions.

        Args:
            eevee_state: Current EeveeState
            context: Current context including brain state, memories, etc.

        Returns:
            ProactiveEvent if one should be triggered, None otherwise
        """
        # Don't spam - check rate limiting
        if not self._should_allow_proactive_event():
            return None

        # Check for greeting opportunity
        greeting_event = self._check_greeting_opportunity(eevee_state, context)
        if greeting_event:
            return greeting_event

        # Check for urgent needs
        need_event = self._check_urgent_needs(eevee_state, context)
        if need_event:
            return need_event

        # Check for emotional sharing opportunity
        emotional_event = self._check_emotional_sharing(eevee_state, context)
        if emotional_event:
            return emotional_event

        # Check for general attention seeking
        attention_event = self._check_attention_seeking(eevee_state, context)
        if attention_event:
            return attention_event

        return None

    def _should_allow_proactive_event(self) -> bool:
        """Check if we should allow a proactive event based on rate limiting"""
        now = datetime.now()

        # Check minimum time between events
        min_interval = self._get_min_event_interval()
        if (now - self.last_proactive_event).total_seconds() < min_interval:
            return False

        # Check hourly rate limit
        hour_ago = now - timedelta(hours=1)
        recent_count = len([e for e in self.recent_events if e.timestamp > hour_ago])

        if recent_count >= self.max_proactive_events_per_hour:
            return False

        return True

    def _get_min_event_interval(self) -> int:
        """Get minimum seconds between proactive events based on level"""
        intervals = {
            ProactiveLevel.QUIET: 3600,      # 1 hour
            ProactiveLevel.NORMAL: 1800,     # 30 minutes
            ProactiveLevel.CHATTY: 900,      # 15 minutes
            ProactiveLevel.VERY_CHATTY: 300  # 5 minutes
        }
        return intervals.get(self.proactive_level, 1800)

    def _check_greeting_opportunity(self, eevee_state, context: Dict[str, Any]) -> Optional[ProactiveEvent]:
        """Check if Eevee should greet the user returning"""
        if not self.user_is_present:
            return None

        # Check if user was absent long enough for a greeting
        absence_duration = (datetime.now() - self.last_user_interaction).total_seconds()
        if absence_duration < self.min_absence_for_greeting:
            return None

        # Generate contextual greeting
        message = self._generate_greeting_message(eevee_state, absence_duration)

        event = ProactiveEvent(
            event_type=ProactiveEventType.GREETING,
            message=message,
            urgency=0.7,
            context={'absence_duration': absence_duration},
            timestamp=datetime.now()
        )

        self.total_greetings += 1
        return event

    def _check_urgent_needs(self, eevee_state, context: Dict[str, Any]) -> Optional[ProactiveEvent]:
        """Check if Eevee has urgent needs to express"""
        urgent_threshold = 20  # Below 20% is urgent
        very_urgent_threshold = 10  # Below 10% is very urgent

        # Check hunger
        if eevee_state.hunger <= urgent_threshold:
            urgency = 0.9 if eevee_state.hunger <= very_urgent_threshold else 0.7
            message = self._generate_hunger_message(eevee_state.hunger)

            return ProactiveEvent(
                event_type=ProactiveEventType.NEED_EXPRESSION,
                message=message,
                urgency=urgency,
                context={'need_type': 'hunger', 'value': eevee_state.hunger},
                timestamp=datetime.now()
            )

        # Check energy
        if eevee_state.energy <= urgent_threshold:
            urgency = 0.8 if eevee_state.energy <= very_urgent_threshold else 0.6
            message = self._generate_energy_message(eevee_state.energy)

            return ProactiveEvent(
                event_type=ProactiveEventType.NEED_EXPRESSION,
                message=message,
                urgency=urgency,
                context={'need_type': 'energy', 'value': eevee_state.energy},
                timestamp=datetime.now()
            )

        # Check happiness
        if eevee_state.happiness <= urgent_threshold:
            urgency = 0.7 if eevee_state.happiness <= very_urgent_threshold else 0.5
            message = self._generate_sadness_message(eevee_state.happiness)

            return ProactiveEvent(
                event_type=ProactiveEventType.NEED_EXPRESSION,
                message=message,
                urgency=urgency,
                context={'need_type': 'happiness', 'value': eevee_state.happiness},
                timestamp=datetime.now()
            )

        return None

    def _check_emotional_sharing(self, eevee_state, context: Dict[str, Any]) -> Optional[ProactiveEvent]:
        """Check if Eevee wants to share emotions or feelings"""
        # Only share if in decent condition (not urgent needs)
        if (eevee_state.hunger < 30 or eevee_state.energy < 30 or
            eevee_state.happiness < 30):
            return None

        # Random chance based on proactive level
        chances = {
            ProactiveLevel.QUIET: 0.05,
            ProactiveLevel.NORMAL: 0.15,
            ProactiveLevel.CHATTY: 0.25,
            ProactiveLevel.VERY_CHATTY: 0.35
        }

        if random.random() > chances.get(self.proactive_level, 0.15):
            return None

        # Generate emotional sharing message
        message = self._generate_emotional_message(eevee_state, context)

        return ProactiveEvent(
            event_type=ProactiveEventType.EMOTIONAL_SHARE,
            message=message,
            urgency=0.3,
            context={'mood': self._assess_mood(eevee_state)},
            timestamp=datetime.now()
        )

    def _check_attention_seeking(self, eevee_state, context: Dict[str, Any]) -> Optional[ProactiveEvent]:
        """Check if Eevee wants attention or interaction"""
        # Only seek attention if lonely or bored
        loneliness_factor = max(0, (datetime.now() - self.last_user_interaction).total_seconds() / 3600)

        if loneliness_factor < 1.0:  # Less than 1 hour of absence
            return None

        # Higher chance if more lonely
        base_chance = min(0.4, loneliness_factor * 0.1)

        # Adjust by proactive level
        level_multipliers = {
            ProactiveLevel.QUIET: 0.5,
            ProactiveLevel.NORMAL: 1.0,
            ProactiveLevel.CHATTY: 1.5,
            ProactiveLevel.VERY_CHATTY: 2.0
        }

        chance = base_chance * level_multipliers.get(self.proactive_level, 1.0)

        if random.random() > chance:
            return None

        message = self._generate_attention_message(eevee_state, loneliness_factor)

        return ProactiveEvent(
            event_type=ProactiveEventType.ATTENTION_SEEKING,
            message=message,
            urgency=0.4,
            context={'loneliness_factor': loneliness_factor},
            timestamp=datetime.now()
        )

    def _generate_greeting_message(self, eevee_state, absence_duration: float) -> str:
        """Generate a contextual greeting message"""
        hours_absent = absence_duration / 3600

        if hours_absent < 1:
            greetings = [
                "*ears perk up* Oh, you're back!",
                "*tail wagging* I missed you!",
                "*happy bark* Vee vee! You returned!",
                "*stretches and approaches* Welcome back!"
            ]
        elif hours_absent < 8:
            greetings = [
                "*bounces excitedly* You were gone for so long! I missed you!",
                "*runs over eagerly* Finally! I was wondering when you'd come back!",
                "*tail wagging intensely* I kept hoping you'd return soon!",
                "*nuzzles against you* I was getting lonely without you!"
            ]
        else:
            greetings = [
                "*tears of joy* You're finally back! I thought you might not come back!",
                "*overwhelmed with excitement* I missed you SO much! Where were you?",
                "*practically vibrating with happiness* You're here! You're really here!",
                "*emotional* I was so worried... I'm so happy you're safe!"
            ]

        return random.choice(greetings)

    def _generate_hunger_message(self, hunger_level: int) -> str:
        """Generate hunger expression message"""
        if hunger_level <= 10:
            messages = [
                "*stomach growling loudly* I'm really, really hungry...",
                "*looking at you pleadingly* Could we find some food? I'm starving...",
                "*whimpering softly* My tummy hurts from being so empty...",
                "*pawing at you gently* Food? Please? I'm so hungry I can barely think..."
            ]
        else:
            messages = [
                "*stomach grumbles* I'm getting pretty hungry...",
                "*looking around for food* Do we have any berries? I could really eat.",
                "*tail drooping slightly* My stomach is making funny noises...",
                "*sniffing the air hopefully* Is there anything to eat around here?"
            ]

        return random.choice(messages)

    def _generate_energy_message(self, energy_level: int) -> str:
        """Generate tiredness expression message"""
        if energy_level <= 10:
            messages = [
                "*yawning deeply* I'm so tired I can barely keep my eyes open...",
                "*swaying slightly* Everything feels heavy... I need to rest...",
                "*curling up* I don't think I can stay awake much longer...",
                "*exhausted whimper* Could we find somewhere to sleep? I'm exhausted..."
            ]
        else:
            messages = [
                "*stretching tiredly* I'm feeling pretty sleepy...",
                "*yawning* All this activity is making me drowsy.",
                "*eyes drooping* I could really use a nap soon...",
                "*settling down* My energy is running low..."
            ]

        return random.choice(messages)

    def _generate_sadness_message(self, happiness_level: int) -> str:
        """Generate sadness/unhappiness expression message"""
        if happiness_level <= 10:
            messages = [
                "*ears drooping sadly* I feel really down right now...",
                "*quiet whimper* Everything just seems sad today...",
                "*looking dejected* I can't seem to cheer up...",
                "*sighing heavily* I wish I felt happier..."
            ]
        else:
            messages = [
                "*tail not wagging as much* I'm feeling a bit down...",
                "*subdued* Things don't seem as fun as usual...",
                "*looking wistful* I could use some cheering up...",
                "*mild sigh* I'm not feeling my best today..."
            ]

        return random.choice(messages)

    def _generate_emotional_message(self, eevee_state, context: Dict[str, Any]) -> str:
        """Generate emotional sharing message"""
        mood = self._assess_mood(eevee_state)

        if mood == "very_happy":
            messages = [
                "*tail wagging energetically* I'm feeling amazing today!",
                "*bouncing slightly* Everything just seems wonderful right now!",
                "*bright eyes* I love spending time with you like this!",
                "*content purr* Life is pretty great, isn't it?"
            ]
        elif mood == "happy":
            messages = [
                "*comfortable sigh* I'm feeling really good right now.",
                "*tail swishing gently* This is nice, just being here with you.",
                "*soft vee* I'm in such a good mood today!",
                "*relaxed posture* Everything feels just right."
            ]
        elif mood == "content":
            messages = [
                "*peaceful expression* I feel calm and content.",
                "*gentle stretch* This moment feels peaceful.",
                "*soft breathing* I'm enjoying this quiet time.",
                "*serene* Sometimes it's nice to just... be, you know?"
            ]
        else:  # neutral or slightly down
            messages = [
                "*thoughtful look* I've been thinking about things lately...",
                "*contemplative* Do you ever wonder about the world around us?",
                "*quiet moment* Sometimes I just like to share what I'm feeling.",
                "*gentle nuzzle* Thanks for being here with me."
            ]

        return random.choice(messages)

    def _generate_attention_message(self, eevee_state, loneliness_factor: float) -> str:
        """Generate attention-seeking message"""
        if loneliness_factor > 4:  # Very lonely
            messages = [
                "*approaching hesitantly* Could we spend some time together?",
                "*soft whine* I've been feeling really lonely lately...",
                "*hopeful eyes* Would you like to do something fun with me?",
                "*gentle paw touch* I miss talking with you..."
            ]
        else:  # Moderately lonely
            messages = [
                "*playful nudge* Want to hang out?",
                "*tail wagging hopefully* Got time for me?",
                "*curious look* What are you up to? Can I join?",
                "*friendly approach* Hey, want to chat for a bit?"
            ]

        return random.choice(messages)

    def _assess_mood(self, eevee_state) -> str:
        """Assess Eevee's current mood based on state"""
        happiness = eevee_state.happiness
        energy = eevee_state.energy
        health = eevee_state.health

        average_wellness = (happiness + energy + health) / 3

        if average_wellness >= 80:
            return "very_happy"
        elif average_wellness >= 60:
            return "happy"
        elif average_wellness >= 40:
            return "content"
        else:
            return "down"

    def execute_proactive_event(self, event: ProactiveEvent):
        """Execute a proactive event and track it"""
        self.recent_events.append(event)
        self.last_proactive_event = datetime.now()

        # Keep only recent events (last 24 hours)
        cutoff = datetime.now() - timedelta(hours=24)
        self.recent_events = [e for e in self.recent_events if e.timestamp > cutoff]

        # Update statistics
        if event.event_type == ProactiveEventType.GREETING:
            self.total_greetings += 1
        elif event.event_type == ProactiveEventType.NEED_EXPRESSION:
            self.total_need_expressions += 1
        elif event.event_type == ProactiveEventType.EMOTIONAL_SHARE:
            self.total_emotional_shares += 1

        logger.info(f"Executed proactive event: {event.event_type.value} - {event.message[:50]}...")

    def get_stats(self) -> Dict[str, Any]:
        """Get proactive interaction statistics"""
        return {
            'proactive_level': self.proactive_level.value,
            'total_greetings': self.total_greetings,
            'total_need_expressions': self.total_need_expressions,
            'total_emotional_shares': self.total_emotional_shares,
            'recent_events_count': len(self.recent_events),
            'last_proactive_event': self.last_proactive_event,
            'user_is_present': self.user_is_present
        }