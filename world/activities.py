"""
Activity Generation for Autonomous Time Passage

Generates realistic activities that Eevee performs when the user is away.
Activities are driven by needs, personality, and environmental factors.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum
import random


class ActivityType(Enum):
    """Types of activities Eevee can perform"""
    NEEDS = "needs"              # Basic needs (eat, sleep, drink)
    EXPLORATION = "exploration"  # Discovering new places
    SOCIAL = "social"           # Interactions with other Pokemon
    SURVIVAL = "survival"       # Responding to threats/weather
    EMOTIONAL = "emotional"     # Missing trainer, feeling lonely
    PLAY = "play"              # Playing alone or with objects
    REST = "rest"              # Resting, napping, relaxing


class EmotionIntensity(Enum):
    """Emotion intensity levels"""
    LOW = 3.0
    MEDIUM = 5.0
    HIGH = 7.0
    VERY_HIGH = 9.0


@dataclass
class Activity:
    """
    Represents a single activity during autonomous time passage

    Significance > 7.0 will become a long-term memory
    """
    timestamp: datetime
    activity_type: ActivityType
    description: str
    location: str

    # State changes
    hunger_delta: int = 0
    energy_delta: int = 0
    happiness_delta: int = 0
    health_delta: int = 0

    # Emotional context
    emotion: str = "neutral"
    emotion_intensity: float = 5.0
    significance: float = 5.0

    # Additional context
    details: Dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}


class ActivityGenerator:
    """
    Generates realistic activities based on Eevee's state and personality

    Activity generation follows this logic:
    1. Check urgent needs (hunger > 80, energy < 20)
    2. Check personality-driven behaviors
    3. Check time-of-day patterns
    4. Add random events based on chance
    """

    def __init__(self, personality: Dict[str, int], world_map):
        """
        Initialize activity generator

        Args:
            personality: Dict with traits (curiosity, bravery, playfulness, etc.)
            world_map: WorldMap instance for location data
        """
        self.personality = personality
        self.world_map = world_map

        # Activity templates
        self._init_activity_templates()

    def _init_activity_templates(self):
        """Initialize activity templates for different scenarios"""

        # NEEDS-based activities
        self.hunger_activities = [
            ("Found some Oran berries near the stream", "clear_stream", -30, 0, 5, 0, "contentment", 4.0, 5.0),
            ("Discovered a Pecha berry bush in the meadow", "meadow", -25, 0, 8, 0, "joy", 5.0, 6.0),
            ("Ate some berries, but still a bit hungry", "forest_edge", -15, 0, 3, 0, "neutral", 3.0, 4.0),
            ("Hunted for food but couldn't find much", "deep_forest", -5, -10, -5, 0, "frustration", 4.0, 5.0),
        ]

        self.energy_activities = [
            ("Curled up in the hidden den for a peaceful nap", "hidden_den", 0, 40, 10, 0, "contentment", 4.0, 5.0),
            ("Dozed off under the warm sun on the hill", "sunny_hill", 0, 35, 12, 0, "peace", 5.0, 6.0),
            ("Took a quick rest in the garden", "sunny_garden", 0, 25, 5, 0, "neutral", 3.0, 4.0),
            ("Tried to sleep but felt restless and worried", "trainer_home", 0, 20, -5, 0, "anxiety", 5.0, 6.5),
        ]

        # EMOTIONAL activities (missing trainer)
        self.loneliness_activities = [
            ("Sat at the meeting spot, hoping trainer would return", "trainer_home", 0, -5, -10, 0, "loneliness", 7.0, 7.5),
            ("Walked to where we last played together, felt sad", "sunny_garden", 0, -5, -8, 0, "sadness", 6.0, 7.0),
            ("Found trainer's scent on an old blanket, missed them deeply", "trainer_home", 0, 0, -12, 0, "longing", 8.0, 8.5),
            ("Howled softly, wondering when trainer will come back", "meadow", 0, -5, -10, 0, "loneliness", 7.5, 8.0),
        ]

        # EXPLORATION activities
        self.exploration_activities = [
            ("Discovered a new patch of wildflowers", "meadow", 0, -5, 8, 0, "curiosity", 5.0, 6.5),
            ("Found a shiny smooth stone by the stream", "clear_stream", 0, -5, 10, 0, "joy", 6.0, 7.0),
            ("Explored deeper into the forest, felt nervous but excited", "deep_forest", 0, -10, 5, 0, "curiosity", 7.0, 7.5),
            ("Climbed to the top of the hill and watched the clouds", "sunny_hill", 0, -5, 8, 0, "peace", 5.0, 6.0),
        ]

        # PLAY activities
        self.play_activities = [
            ("Chased butterflies in the garden", "sunny_garden", 5, -15, 10, 0, "joy", 5.0, 5.5),
            ("Practiced pouncing on leaves", "forest_edge", 5, -10, 8, 0, "playfulness", 4.0, 5.0),
            ("Ran in circles just for fun", "meadow", 0, -15, 12, 0, "joy", 6.0, 6.5),
            ("Found a stick and played with it for a while", "sunny_garden", 0, -10, 7, 0, "contentment", 4.0, 5.0),
        ]

        # SOCIAL activities (NPC encounters)
        self.social_activities = [
            ("Met a friendly Pidgey, played together briefly", "meadow", 0, -10, 12, 0, "joy", 6.0, 7.0),
            ("Saw a Rattata but it ran away quickly", "forest_edge", 0, -5, 0, 0, "curiosity", 3.0, 4.0),
            ("Heard a Hoothoot in the distance, felt a bit scared", "deep_forest", 0, -5, -5, 0, "fear", 5.0, 6.0),
            ("Watched a Butterfree dance around flowers", "sunny_garden", 0, 0, 5, 0, "wonder", 4.0, 5.5),
        ]

        # SURVIVAL activities (weather/danger)
        self.survival_activities = [
            ("Thunder crashed nearby, ran to hide in the den", "hidden_den", 0, -15, -15, 0, "fear", 8.0, 8.5),
            ("Rain started, found shelter under a big tree", "forest_edge", 0, -5, -8, 0, "anxiety", 6.0, 6.5),
            ("Heard strange noises, stayed very still and quiet", "deep_forest", 0, -10, -12, 0, "fear", 7.5, 7.8),
            ("Strong winds made me nervous, went to safe spot", "hidden_den", 0, -8, -10, 0, "fear", 6.5, 7.0),
        ]

    def generate_activity(self, state: Dict[str, Any], elapsed_hours: float,
                         current_time: datetime, last_location: str) -> Activity:
        """
        Generate a single activity based on current state

        Args:
            state: Current Eevee state (hunger, energy, happiness, etc.)
            elapsed_hours: Hours since last activity
            current_time: Timestamp for this activity
            last_location: Previous location

        Returns:
            Activity object
        """
        hunger = state.get('hunger', 50)
        energy = state.get('energy', 50)
        happiness = state.get('happiness', 70)
        time_since_trainer = state.get('hours_since_trainer', 0)

        # Priority 1: URGENT NEEDS
        if hunger > 80:
            return self._generate_hunger_activity(current_time, last_location)

        if energy < 20:
            return self._generate_rest_activity(current_time, last_location)

        # Priority 2: EMOTIONAL NEEDS (loneliness after 24+ hours)
        if time_since_trainer > 24 and random.random() < 0.3:
            return self._generate_loneliness_activity(current_time, last_location, time_since_trainer)

        # Priority 3: PERSONALITY-DRIVEN BEHAVIORS
        curiosity = self.personality.get('curiosity', 5)
        playfulness = self.personality.get('playfulness', 5)
        bravery = self.personality.get('bravery', 5)

        # Roll for activity type based on personality
        roll = random.random() * 10

        if roll < curiosity / 10 * 3:  # Curiosity influences exploration
            return self._generate_exploration_activity(current_time, last_location, bravery)

        elif roll < (curiosity + playfulness) / 10 * 3:  # Playfulness
            return self._generate_play_activity(current_time, last_location, energy)

        elif roll < 0.6:  # Social encounter (moderate chance)
            return self._generate_social_activity(current_time, last_location)

        elif roll < 0.75:  # Random event / survival
            return self._generate_survival_activity(current_time, last_location)

        else:  # Rest/routine activity
            if energy < 50:
                return self._generate_rest_activity(current_time, last_location)
            else:
                return self._generate_routine_activity(current_time, last_location)

    def _generate_hunger_activity(self, timestamp: datetime, location: str) -> Activity:
        """Generate food-seeking activity"""
        desc, loc, h_delta, e_delta, hap_delta, heal_delta, emotion, intensity, sig = random.choice(self.hunger_activities)

        return Activity(
            timestamp=timestamp,
            activity_type=ActivityType.NEEDS,
            description=desc,
            location=loc,
            hunger_delta=h_delta,
            energy_delta=e_delta,
            happiness_delta=hap_delta,
            health_delta=heal_delta,
            emotion=emotion,
            emotion_intensity=intensity,
            significance=sig
        )

    def _generate_rest_activity(self, timestamp: datetime, location: str) -> Activity:
        """Generate resting/sleeping activity"""
        desc, loc, h_delta, e_delta, hap_delta, heal_delta, emotion, intensity, sig = random.choice(self.energy_activities)

        return Activity(
            timestamp=timestamp,
            activity_type=ActivityType.REST,
            description=desc,
            location=loc,
            hunger_delta=h_delta,
            energy_delta=e_delta,
            happiness_delta=hap_delta,
            health_delta=heal_delta,
            emotion=emotion,
            emotion_intensity=intensity,
            significance=sig
        )

    def _generate_loneliness_activity(self, timestamp: datetime, location: str, hours_away: float) -> Activity:
        """Generate loneliness/missing trainer activity"""
        desc, loc, h_delta, e_delta, hap_delta, heal_delta, emotion, intensity, sig = random.choice(self.loneliness_activities)

        # Intensity increases with time
        if hours_away > 72:  # 3 days
            intensity = min(9.0, intensity + 1.0)
            sig = min(9.5, sig + 1.0)

        return Activity(
            timestamp=timestamp,
            activity_type=ActivityType.EMOTIONAL,
            description=desc,
            location=loc,
            hunger_delta=h_delta,
            energy_delta=e_delta,
            happiness_delta=hap_delta,
            health_delta=heal_delta,
            emotion=emotion,
            emotion_intensity=intensity,
            significance=sig,
            details={'hours_away': hours_away}
        )

    def _generate_exploration_activity(self, timestamp: datetime, location: str, bravery: int) -> Activity:
        """Generate exploration activity (Phase 5: Can find items)"""
        desc, loc, h_delta, e_delta, hap_delta, heal_delta, emotion, intensity, sig = random.choice(self.exploration_activities)

        # High bravery = more likely to explore dangerous areas
        if bravery < 5 and "deep_forest" in loc:
            # Re-roll for safer location
            desc, loc, h_delta, e_delta, hap_delta, heal_delta, emotion, intensity, sig = random.choice([
                a for a in self.exploration_activities if "deep_forest" not in a[1]
            ])

        # Phase 5: Chance to find items during exploration (25%)
        found_item = None
        if random.random() < 0.25:
            from world.items import ItemManager, ItemRarity

            # Determine rarity based on location
            if "deep_forest" in loc or "mountain" in loc:
                # Dangerous areas = better loot
                rarity_roll = random.random()
                if rarity_roll < 0.05:  # 5% very rare
                    found_item = ItemManager.get_random_item_by_rarity(ItemRarity.VERY_RARE)
                elif rarity_roll < 0.20:  # 15% rare
                    found_item = ItemManager.get_random_item_by_rarity(ItemRarity.RARE)
                elif rarity_roll < 0.50:  # 30% uncommon
                    found_item = ItemManager.get_random_item_by_rarity(ItemRarity.UNCOMMON)
                else:  # 50% common
                    found_item = ItemManager.get_random_item_by_rarity(ItemRarity.COMMON)
            else:
                # Safe areas = mostly common items
                rarity_roll = random.random()
                if rarity_roll < 0.01:  # 1% very rare
                    found_item = ItemManager.get_random_item_by_rarity(ItemRarity.VERY_RARE)
                elif rarity_roll < 0.10:  # 9% rare
                    found_item = ItemManager.get_random_item_by_rarity(ItemRarity.RARE)
                elif rarity_roll < 0.30:  # 20% uncommon
                    found_item = ItemManager.get_random_item_by_rarity(ItemRarity.UNCOMMON)
                else:  # 70% common
                    found_item = ItemManager.get_random_item_by_rarity(ItemRarity.COMMON)

            if found_item:
                desc = f"{desc} - Found {found_item.emoji} {found_item.name}!"
                hap_delta += 10  # Extra happiness from discovery
                sig = max(sig, 6.5)  # Finding items is somewhat memorable

        activity = Activity(
            timestamp=timestamp,
            activity_type=ActivityType.EXPLORATION,
            description=desc,
            location=loc,
            hunger_delta=h_delta,
            energy_delta=e_delta,
            happiness_delta=hap_delta,
            health_delta=heal_delta,
            emotion=emotion,
            emotion_intensity=intensity,
            significance=sig
        )

        # Store found item in details
        if found_item:
            activity.details['found_item'] = found_item.id

        return activity

    def _generate_play_activity(self, timestamp: datetime, location: str, energy: int) -> Activity:
        """Generate play activity"""
        # Low energy = less energetic play
        activities = self.play_activities
        if energy < 40:
            activities = [a for a in activities if a[4] > -12]  # Filter out high-energy activities

        desc, loc, h_delta, e_delta, hap_delta, heal_delta, emotion, intensity, sig = random.choice(activities)

        return Activity(
            timestamp=timestamp,
            activity_type=ActivityType.PLAY,
            description=desc,
            location=loc,
            hunger_delta=h_delta,
            energy_delta=e_delta,
            happiness_delta=hap_delta,
            health_delta=heal_delta,
            emotion=emotion,
            emotion_intensity=intensity,
            significance=sig
        )

    def _generate_social_activity(self, timestamp: datetime, location: str) -> Activity:
        """Generate social encounter activity"""
        desc, loc, h_delta, e_delta, hap_delta, heal_delta, emotion, intensity, sig = random.choice(self.social_activities)

        return Activity(
            timestamp=timestamp,
            activity_type=ActivityType.SOCIAL,
            description=desc,
            location=loc,
            hunger_delta=h_delta,
            energy_delta=e_delta,
            happiness_delta=hap_delta,
            health_delta=heal_delta,
            emotion=emotion,
            emotion_intensity=intensity,
            significance=sig
        )

    def _generate_survival_activity(self, timestamp: datetime, location: str) -> Activity:
        """Generate survival/weather activity"""
        desc, loc, h_delta, e_delta, hap_delta, heal_delta, emotion, intensity, sig = random.choice(self.survival_activities)

        return Activity(
            timestamp=timestamp,
            activity_type=ActivityType.SURVIVAL,
            description=desc,
            location=loc,
            hunger_delta=h_delta,
            energy_delta=e_delta,
            happiness_delta=hap_delta,
            health_delta=heal_delta,
            emotion=emotion,
            emotion_intensity=intensity,
            significance=sig
        )

    def _generate_routine_activity(self, timestamp: datetime, location: str) -> Activity:
        """Generate routine/mundane activity"""
        routine_activities = [
            ("Groomed fur and cleaned paws", location, 0, -5, 3, 0, "contentment", 3.0, 4.0),
            ("Stretched and yawned, feeling relaxed", location, 0, 5, 2, 0, "neutral", 3.0, 3.5),
            ("Sat quietly, listening to the sounds of nature", location, 0, 0, 5, 0, "peace", 4.0, 4.5),
            ("Watched the clouds drift by lazily", location, 0, 0, 3, 0, "calm", 3.0, 4.0),
        ]

        desc, loc, h_delta, e_delta, hap_delta, heal_delta, emotion, intensity, sig = random.choice(routine_activities)

        return Activity(
            timestamp=timestamp,
            activity_type=ActivityType.REST,
            description=desc,
            location=loc,
            hunger_delta=h_delta,
            energy_delta=e_delta,
            happiness_delta=hap_delta,
            health_delta=heal_delta,
            emotion=emotion,
            emotion_intensity=intensity,
            significance=sig
        )
