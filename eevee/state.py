"""
Eevee State Management
Handles Eevee's physical state, location, inventory, and persistence
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from config import Config, DATABASE_PATH


class EeveeState:
    """Manages Eevee's current state and persistence"""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._initialize_database()
        self._load_or_create_state()

    def _initialize_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main state table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eevee_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_interaction TIMESTAMP,

                -- Physical state
                hunger INTEGER DEFAULT 40,
                energy INTEGER DEFAULT 70,
                health INTEGER DEFAULT 95,
                happiness INTEGER DEFAULT 85,

                -- Location and world
                current_location TEXT DEFAULT 'trainer_home',
                time_of_day TEXT DEFAULT 'morning',
                weather TEXT DEFAULT 'sunny',

                -- Relationship
                trust_level INTEGER DEFAULT 50,
                bond_strength INTEGER DEFAULT 30,
                time_together_minutes INTEGER DEFAULT 0,

                -- Inventory (stored as JSON)
                inventory TEXT DEFAULT '[]',

                -- Metadata
                total_interactions INTEGER DEFAULT 0,
                memories_count INTEGER DEFAULT 0
            )
        """)

        # Personality traits table (semi-permanent)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personality (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                curiosity INTEGER DEFAULT 8,
                bravery INTEGER DEFAULT 5,
                playfulness INTEGER DEFAULT 9,
                loyalty INTEGER DEFAULT 10,
                independence INTEGER DEFAULT 6
            )
        """)

        # Interaction history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                interaction_type TEXT,
                user_input TEXT,
                eevee_response TEXT,
                location TEXT,
                emotional_state TEXT,
                significance REAL DEFAULT 5.0
            )
        """)

        conn.commit()
        conn.close()

    def _load_or_create_state(self):
        """Load existing state or create new one"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if state exists
        cursor.execute("SELECT COUNT(*) FROM eevee_state")
        exists = cursor.fetchone()[0] > 0

        if not exists:
            # Create initial state
            cursor.execute("""
                INSERT INTO eevee_state (
                    hunger, energy, health, happiness,
                    current_location, trust_level, bond_strength,
                    last_interaction, inventory
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                Config.INITIAL_HUNGER,
                Config.INITIAL_ENERGY,
                Config.INITIAL_HEALTH,
                Config.INITIAL_HAPPINESS,
                Config.STARTING_LOCATION,
                Config.INITIAL_TRUST,
                Config.INITIAL_BOND,
                datetime.now().isoformat(),
                json.dumps([])
            ))

            # Create initial personality
            cursor.execute("""
                INSERT INTO personality (
                    curiosity, bravery, playfulness, loyalty, independence
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                Config.PERSONALITY_CURIOSITY,
                Config.PERSONALITY_BRAVERY,
                Config.PERSONALITY_PLAYFULNESS,
                Config.PERSONALITY_LOYALTY,
                Config.PERSONALITY_INDEPENDENCE
            ))

            conn.commit()

        # Load current state
        cursor.execute("SELECT * FROM eevee_state WHERE id = 1")
        row = cursor.fetchone()
        columns = [description[0] for description in cursor.description]
        self._state = dict(zip(columns, row))

        # Parse JSON fields
        self._state['inventory'] = json.loads(self._state['inventory'])

        conn.close()

    def save(self):
        """Persist current state to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE eevee_state SET
                last_updated = ?,
                last_interaction = ?,
                hunger = ?,
                energy = ?,
                health = ?,
                happiness = ?,
                current_location = ?,
                time_of_day = ?,
                weather = ?,
                trust_level = ?,
                bond_strength = ?,
                time_together_minutes = ?,
                inventory = ?,
                total_interactions = ?,
                memories_count = ?
            WHERE id = 1
        """, (
            datetime.now().isoformat(),
            self._state['last_interaction'],
            self._state['hunger'],
            self._state['energy'],
            self._state['health'],
            self._state['happiness'],
            self._state['current_location'],
            self._state['time_of_day'],
            self._state['weather'],
            self._state['trust_level'],
            self._state['bond_strength'],
            self._state['time_together_minutes'],
            json.dumps(self._state['inventory']),
            self._state['total_interactions'],
            self._state['memories_count']
        ))

        conn.commit()
        conn.close()

    def log_interaction(self, interaction_type: str, user_input: str,
                       eevee_response: str, emotional_state: str,
                       significance: float = 5.0):
        """Log an interaction to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO interactions (
                interaction_type, user_input, eevee_response,
                location, emotional_state, significance
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            interaction_type,
            user_input,
            eevee_response,
            self._state['current_location'],
            emotional_state,
            significance
        ))

        conn.commit()
        conn.close()

        # Update interaction count
        self._state['total_interactions'] += 1
        self._state['last_interaction'] = datetime.now().isoformat()

    def update_physical_state(self, **kwargs):
        """Update physical stats (hunger, energy, health, happiness)"""
        for key, value in kwargs.items():
            if key in ['hunger', 'energy', 'health', 'happiness']:
                # Clamp values between 0 and 100
                self._state[key] = max(0, min(100, value))

    def update_relationship(self, trust_delta: int = 0, bond_delta: int = 0):
        """Update relationship stats"""
        if trust_delta:
            self._state['trust_level'] = max(0, min(100,
                self._state['trust_level'] + trust_delta))
        if bond_delta:
            self._state['bond_strength'] = max(0, min(100,
                self._state['bond_strength'] + bond_delta))

    def add_item(self, item: str):
        """Add item to inventory"""
        if item not in self._state['inventory']:
            self._state['inventory'].append(item)

    def remove_item(self, item: str) -> bool:
        """Remove item from inventory"""
        if item in self._state['inventory']:
            self._state['inventory'].remove(item)
            return True
        return False

    def has_item(self, item: str) -> bool:
        """Check if item is in inventory"""
        return item in self._state['inventory']

    def get_time_since_last_interaction(self) -> float:
        """Get hours since last interaction"""
        last = datetime.fromisoformat(self._state['last_interaction'])
        now = datetime.now()
        delta = now - last
        return delta.total_seconds() / 3600

    # Property accessors
    @property
    def hunger(self) -> int:
        return self._state['hunger']

    @property
    def energy(self) -> int:
        return self._state['energy']

    @property
    def health(self) -> int:
        return self._state['health']

    @property
    def happiness(self) -> int:
        return self._state['happiness']

    @property
    def location(self) -> str:
        return self._state['current_location']

    @property
    def trust(self) -> int:
        return self._state['trust_level']

    @property
    def bond(self) -> int:
        return self._state['bond_strength']

    @property
    def inventory(self) -> List[str]:
        return self._state['inventory'].copy()

    @property
    def time_of_day(self) -> str:
        return self._state['time_of_day']

    @property
    def weather(self) -> str:
        return self._state['weather']

    def to_dict(self) -> Dict[str, Any]:
        """Export state as dictionary"""
        return {
            'physical_state': {
                'hunger': self.hunger,
                'energy': self.energy,
                'health': self.health,
                'happiness': self.happiness
            },
            'location': self.location,
            'current_location': self.location,  # Phase 3: Also provide as current_location for memory system
            'time_of_day': self.time_of_day,
            'weather': self.weather,
            'relationship': {
                'trust': self.trust,
                'bond': self.bond,
                'time_together_hours': self._state['time_together_minutes'] / 60
            },
            'inventory': self.inventory,
            'total_interactions': self._state['total_interactions']
        }

    def __repr__(self):
        return f"<EeveeState: H={self.hunger} E={self.energy} Happiness={self.happiness} Location={self.location}>"
