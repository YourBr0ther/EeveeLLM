"""
Special Events System for EeveeLLM

Generates random world events, weather changes, and rare encounters
that make the world feel alive and unpredictable.

Phase 5 Part 2: Special Events & Surprises
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional, List
import random
from datetime import datetime


class EventType(Enum):
    """Categories of special events"""
    WEATHER = "weather"
    ENCOUNTER = "encounter"
    DISCOVERY = "discovery"
    PHENOMENON = "phenomenon"
    SEASONAL = "seasonal"


class EventRarity(Enum):
    """How rare an event is"""
    COMMON = "common"           # 40% chance when event rolls
    UNCOMMON = "uncommon"       # 35% chance
    RARE = "rare"               # 20% chance
    VERY_RARE = "very_rare"     # 5% chance


@dataclass
class SpecialEvent:
    """
    Represents a special event that can occur

    Events affect Eevee's state, mood, and create memorable moments.
    """
    id: str
    name: str
    event_type: EventType
    rarity: EventRarity
    description: str

    # State effects
    hunger_delta: int = 0
    energy_delta: int = 0
    happiness_delta: int = 0
    health_delta: int = 0

    # Emotional impact
    emotion: str = "surprise"
    emotion_intensity: float = 6.0
    significance: float = 7.0  # Events are usually memorable

    # Requirements
    required_location: Optional[str] = None  # If None, can happen anywhere
    min_time_of_day: Optional[str] = None

    # Rewards
    grants_item: Optional[str] = None

    def can_occur(self, location: str, time_of_day: str, weather: str) -> bool:
        """Check if this event can occur given current conditions"""
        if self.required_location and location != self.required_location:
            return False
        if self.min_time_of_day and time_of_day != self.min_time_of_day:
            return False
        return True


# ============================================================================
# EVENT CATALOG
# ============================================================================

EVENTS_CATALOG: Dict[str, SpecialEvent] = {
    # --- WEATHER EVENTS ---

    "rainbow_after_rain": SpecialEvent(
        id="rainbow_after_rain",
        name="Rainbow After Rain",
        event_type=EventType.WEATHER,
        rarity=EventRarity.UNCOMMON,
        description="A beautiful rainbow appeared in the sky after the rain! ✨🌈",
        happiness_delta=15,
        emotion="joy",
        emotion_intensity=7.5,
        significance=7.5,
        grants_item="rainbow_wing"
    ),

    "gentle_snow": SpecialEvent(
        id="gentle_snow",
        name="Gentle Snowfall",
        event_type=EventType.WEATHER,
        rarity=EventRarity.UNCOMMON,
        description="Soft snowflakes began to fall, creating a peaceful winter wonderland ❄️",
        happiness_delta=10,
        energy_delta=5,
        emotion="contentment",
        emotion_intensity=6.5,
        significance=6.5
    ),

    "thunderstorm": SpecialEvent(
        id="thunderstorm",
        name="Thunderstorm",
        event_type=EventType.WEATHER,
        rarity=EventRarity.COMMON,
        description="A sudden thunderstorm rolled in! Thunder crashed and lightning flashed ⚡🌩️",
        energy_delta=-10,
        happiness_delta=-15,
        emotion="fear",
        emotion_intensity=8.0,
        significance=7.5
    ),

    "perfect_sunny_day": SpecialEvent(
        id="perfect_sunny_day",
        name="Perfect Sunny Day",
        event_type=EventType.WEATHER,
        rarity=EventRarity.COMMON,
        description="The weather is absolutely perfect! Warm sun, gentle breeze ☀️",
        happiness_delta=8,
        energy_delta=5,
        emotion="contentment",
        emotion_intensity=6.0,
        significance=5.5
    ),

    "meteor_shower": SpecialEvent(
        id="meteor_shower",
        name="Meteor Shower",
        event_type=EventType.PHENOMENON,
        rarity=EventRarity.VERY_RARE,
        description="Shooting stars streaked across the night sky! A breathtaking meteor shower ✨🌠",
        happiness_delta=20,
        emotion="wonder",
        emotion_intensity=9.0,
        significance=9.0,
        min_time_of_day="night"
    ),

    # --- ENCOUNTERS ---

    "friendly_deerling": SpecialEvent(
        id="friendly_deerling",
        name="Friendly Deerling",
        event_type=EventType.ENCOUNTER,
        rarity=EventRarity.COMMON,
        description="A friendly Deerling approached and nuzzled you! 🦌",
        happiness_delta=12,
        emotion="joy",
        emotion_intensity=6.5,
        significance=6.5,
        required_location="meadow"
    ),

    "shiny_pokemon_sighting": SpecialEvent(
        id="shiny_pokemon_sighting",
        name="Shiny Pokémon Sighting!",
        event_type=EventType.ENCOUNTER,
        rarity=EventRarity.VERY_RARE,
        description="A SHINY Pokémon appeared nearby! Its unusual coloring sparkled in the light! ✨",
        happiness_delta=25,
        emotion="excitement",
        emotion_intensity=9.5,
        significance=9.5
    ),

    "wise_old_pokemon": SpecialEvent(
        id="wise_old_pokemon",
        name="Wise Elder Pokémon",
        event_type=EventType.ENCOUNTER,
        rarity=EventRarity.RARE,
        description="An ancient, wise Pokémon appeared and shared a moment of understanding 🧙",
        happiness_delta=15,
        energy_delta=10,
        health_delta=10,
        emotion="gratitude",
        emotion_intensity=7.5,
        significance=8.0
    ),

    "playful_pokemon_group": SpecialEvent(
        id="playful_pokemon_group",
        name="Playful Pokémon Group",
        event_type=EventType.ENCOUNTER,
        rarity=EventRarity.UNCOMMON,
        description="A group of playful Pokémon invited you to join their games! 🎮",
        hunger_delta=5,
        energy_delta=-10,
        happiness_delta=18,
        emotion="joy",
        emotion_intensity=7.0,
        significance=7.0
    ),

    "mysterious_eevee": SpecialEvent(
        id="mysterious_eevee",
        name="Mysterious Eevee",
        event_type=EventType.ENCOUNTER,
        rarity=EventRarity.RARE,
        description="Another Eevee appeared! You felt a strange connection... 👥",
        happiness_delta=20,
        emotion="curiosity",
        emotion_intensity=8.0,
        significance=8.5
    ),

    # --- DISCOVERIES ---

    "hidden_spring": SpecialEvent(
        id="hidden_spring",
        name="Hidden Spring",
        event_type=EventType.DISCOVERY,
        rarity=EventRarity.RARE,
        description="Discovered a hidden spring with crystal-clear water! 💧✨",
        hunger_delta=-15,
        health_delta=15,
        happiness_delta=12,
        emotion="joy",
        emotion_intensity=7.5,
        significance=7.5,
        required_location="deep_forest"
    ),

    "ancient_ruins": SpecialEvent(
        id="ancient_ruins",
        name="Ancient Ruins",
        event_type=EventType.DISCOVERY,
        rarity=EventRarity.VERY_RARE,
        description="Stumbled upon mysterious ancient ruins covered in strange markings 🏛️",
        happiness_delta=15,
        emotion="curiosity",
        emotion_intensity=8.0,
        significance=8.5,
        grants_item="old_amber"
    ),

    "secret_berry_grove": SpecialEvent(
        id="secret_berry_grove",
        name="Secret Berry Grove",
        event_type=EventType.DISCOVERY,
        rarity=EventRarity.UNCOMMON,
        description="Found a secret grove filled with delicious berries! 🍓",
        hunger_delta=-30,
        happiness_delta=15,
        emotion="joy",
        emotion_intensity=7.0,
        significance=7.0,
        grants_item="sitrus_berry"
    ),

    # --- PHENOMENA ---

    "aurora_borealis": SpecialEvent(
        id="aurora_borealis",
        name="Aurora Borealis",
        event_type=EventType.PHENOMENON,
        rarity=EventRarity.VERY_RARE,
        description="The northern lights danced across the sky in brilliant colors! 🌌",
        happiness_delta=22,
        emotion="wonder",
        emotion_intensity=9.0,
        significance=9.0,
        min_time_of_day="night"
    ),

    "double_rainbow": SpecialEvent(
        id="double_rainbow",
        name="Double Rainbow",
        event_type=EventType.PHENOMENON,
        rarity=EventRarity.RARE,
        description="A rare double rainbow stretched across the entire sky! 🌈🌈",
        happiness_delta=18,
        emotion="joy",
        emotion_intensity=8.0,
        significance=8.0
    ),

    "firefly_swarm": SpecialEvent(
        id="firefly_swarm",
        name="Firefly Swarm",
        event_type=EventType.PHENOMENON,
        rarity=EventRarity.UNCOMMON,
        description="Hundreds of fireflies lit up the evening in a magical display ✨",
        happiness_delta=14,
        emotion="contentment",
        emotion_intensity=7.0,
        significance=7.0,
        min_time_of_day="evening"
    ),

    "flower_bloom": SpecialEvent(
        id="flower_bloom",
        name="Sudden Flower Bloom",
        event_type=EventType.PHENOMENON,
        rarity=EventRarity.UNCOMMON,
        description="All the flowers in the meadow bloomed at once in a burst of color! 🌸🌺",
        happiness_delta=12,
        emotion="joy",
        emotion_intensity=6.5,
        significance=6.5,
        required_location="meadow"
    ),
}


class EventGenerator:
    """
    Generates and manages special events

    Events add surprise and unpredictability to the world,
    creating memorable moments and rewarding exploration.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize event generator

        Args:
            config: Configuration dict with event settings
        """
        self.config = config or {}
        self.event_chance = self.config.get('event_chance', 0.15)  # 15% base chance

    def should_generate_event(self) -> bool:
        """Determine if an event should occur"""
        return random.random() < self.event_chance

    def generate_event(
        self,
        location: str,
        time_of_day: str = "day",
        weather: str = "sunny",
        personality_traits: Optional[Dict[str, int]] = None
    ) -> Optional[SpecialEvent]:
        """
        Generate a special event

        Args:
            location: Current location ID
            time_of_day: Time of day (morning, day, evening, night)
            weather: Current weather
            personality_traits: Eevee's personality (affects discovery chance)

        Returns:
            SpecialEvent or None if no event occurs
        """
        if not self.should_generate_event():
            return None

        # Get events that can occur in current conditions
        valid_events = [
            event for event in EVENTS_CATALOG.values()
            if event.can_occur(location, time_of_day, weather)
        ]

        if not valid_events:
            return None

        # Adjust probabilities based on personality
        if personality_traits:
            curiosity = personality_traits.get('curiosity', 5)
            # High curiosity = more likely to discover rare events
            if curiosity >= 8:
                # Boost chance of discoveries and rare events
                discovery_events = [e for e in valid_events if e.event_type == EventType.DISCOVERY]
                if discovery_events and random.random() < 0.3:
                    valid_events = discovery_events

        # Weight events by rarity
        rarity_weights = {
            EventRarity.COMMON: 40,
            EventRarity.UNCOMMON: 35,
            EventRarity.RARE: 20,
            EventRarity.VERY_RARE: 5
        }

        # Build weighted list
        weighted_events = []
        for event in valid_events:
            weight = rarity_weights.get(event.rarity, 10)
            weighted_events.extend([event] * weight)

        if not weighted_events:
            return None

        return random.choice(weighted_events)

    def get_event_by_id(self, event_id: str) -> Optional[SpecialEvent]:
        """Get a specific event by ID"""
        return EVENTS_CATALOG.get(event_id)

    def get_events_by_type(self, event_type: EventType) -> List[SpecialEvent]:
        """Get all events of a specific type"""
        return [e for e in EVENTS_CATALOG.values() if e.event_type == event_type]

    def get_events_by_location(self, location: str) -> List[SpecialEvent]:
        """Get events that can occur at a specific location"""
        return [
            e for e in EVENTS_CATALOG.values()
            if e.required_location is None or e.required_location == location
        ]
