"""
World Location System
Defines locations, their properties, and connections
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Location:
    """Represents a location in the world"""
    id: str
    name: str
    description: str
    safety_level: int  # 0-10, higher is safer
    has_food: bool
    has_water: bool
    has_shelter: bool
    exploration_value: int  # 0-10, novelty/interest
    weather_exposure: int  # 0-10, higher means more exposed
    connected_to: List[str]  # IDs of connected locations

    def to_dict(self) -> Dict:
        """Export location as dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'safety_level': self.safety_level,
            'has_food': self.has_food,
            'has_water': self.has_water,
            'has_shelter': self.has_shelter,
            'exploration_value': self.exploration_value,
            'weather_exposure': self.weather_exposure,
            'connected_to': self.connected_to
        }


class WorldMap:
    """Manages the world map and locations"""

    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self._initialize_default_world()

    def _initialize_default_world(self):
        """Create default world locations"""
        # Trainer's Home - Safe starting point
        self.add_location(Location(
            id="trainer_home",
            name="Trainer's Home",
            description="A cozy house with familiar scents. This is where you usually meet your trainer. The warm sunlight streams through the windows.",
            safety_level=10,
            has_food=True,
            has_water=True,
            has_shelter=True,
            exploration_value=2,
            weather_exposure=0,
            connected_to=["meadow", "garden"]
        ))

        # Garden - Safe, nearby
        self.add_location(Location(
            id="garden",
            name="Sunny Garden",
            description="A pleasant garden with flowers and soft grass. Perfect for playing and relaxing in the sun.",
            safety_level=9,
            has_food=True,
            has_water=True,
            has_shelter=False,
            exploration_value=4,
            weather_exposure=5,
            connected_to=["trainer_home", "meadow"]
        ))

        # Meadow - Open exploration area
        self.add_location(Location(
            id="meadow",
            name="Wide Meadow",
            description="An open meadow with tall grass swaying in the breeze. Great for running and spotting other Pokemon from afar.",
            safety_level=7,
            has_food=True,
            has_water=False,
            has_shelter=False,
            exploration_value=6,
            weather_exposure=8,
            connected_to=["trainer_home", "garden", "stream", "forest_edge"]
        ))

        # Stream - Resource location
        self.add_location(Location(
            id="stream",
            name="Clear Stream",
            description="A gentle stream with cool, fresh water. Berry bushes grow along the banks. The sound of flowing water is peaceful.",
            safety_level=8,
            has_food=True,
            has_water=True,
            has_shelter=False,
            exploration_value=5,
            weather_exposure=6,
            connected_to=["meadow", "forest_edge", "sunny_hill"]
        ))

        # Forest Edge - Slightly mysterious
        self.add_location(Location(
            id="forest_edge",
            name="Forest Edge",
            description="The border between the meadow and the deeper forest. Shadows from tall trees create patterns on the ground. You can hear rustling in the bushes.",
            safety_level=5,
            has_food=True,
            has_water=False,
            has_shelter=True,
            exploration_value=8,
            weather_exposure=3,
            connected_to=["meadow", "stream", "hidden_den", "deep_forest"]
        ))

        # Hidden Den - Secret safe spot
        self.add_location(Location(
            id="hidden_den",
            name="Hidden Den",
            description="Your secret den tucked under the roots of an old tree. Only you know about this place. It's small, dark, and perfectly cozy.",
            safety_level=10,
            has_food=False,
            has_water=False,
            has_shelter=True,
            exploration_value=3,
            weather_exposure=0,
            connected_to=["forest_edge"]
        ))

        # Sunny Hill - Favorite napping spot
        self.add_location(Location(
            id="sunny_hill",
            name="Sunny Hill",
            description="A gentle hill with the perfect view of the sunset. The grass is soft and warm. This is your favorite spot for napping and thinking.",
            safety_level=8,
            has_food=False,
            has_water=False,
            has_shelter=False,
            exploration_value=7,
            weather_exposure=9,
            connected_to=["stream", "meadow"]
        ))

        # Deep Forest - Dangerous but interesting
        self.add_location(Location(
            id="deep_forest",
            name="Deep Forest",
            description="The forest grows thick and shadowy here. Strange sounds echo between the trees. It's both scary and exciting.",
            safety_level=3,
            has_food=True,
            has_water=False,
            has_shelter=True,
            exploration_value=10,
            weather_exposure=2,
            connected_to=["forest_edge"]
        ))

    def add_location(self, location: Location):
        """Add a location to the world"""
        self.locations[location.id] = location

    def get_location(self, location_id: str) -> Optional[Location]:
        """Get location by ID"""
        return self.locations.get(location_id)

    def get_connected_locations(self, location_id: str) -> List[Location]:
        """Get all locations connected to the given location"""
        location = self.get_location(location_id)
        if not location:
            return []

        return [
            self.locations[loc_id]
            for loc_id in location.connected_to
            if loc_id in self.locations
        ]

    def can_travel(self, from_id: str, to_id: str) -> bool:
        """Check if travel is possible between two locations"""
        from_location = self.get_location(from_id)
        if not from_location:
            return False
        return to_id in from_location.connected_to

    def get_location_names(self) -> List[str]:
        """Get list of all location names"""
        return [loc.name for loc in self.locations.values()]

    def get_location_by_name(self, name: str) -> Optional[Location]:
        """Get location by name"""
        for location in self.locations.values():
            if location.name.lower() == name.lower():
                return location
        return None

    def describe_location(self, location_id: str) -> str:
        """Get formatted description of location"""
        location = self.get_location(location_id)
        if not location:
            return "Unknown location"

        desc = f"📍 {location.name.upper()}\n"
        desc += f"{location.description}\n\n"

        # Add connection info
        if location.connected_to:
            connected = self.get_connected_locations(location_id)
            desc += "You can go to: "
            desc += ", ".join([loc.name for loc in connected])

        return desc

    def __repr__(self):
        return f"<WorldMap: {len(self.locations)} locations>"
