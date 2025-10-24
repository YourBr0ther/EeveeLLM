"""
Eevee Personality System
Manages personality traits that influence decision-making
"""
import sqlite3
from typing import Dict
from pathlib import Path

from config import DATABASE_PATH


class Personality:
    """Manages Eevee's personality traits"""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._load_personality()

    def _load_personality(self):
        """Load personality from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM personality WHERE id = 1")
        row = cursor.fetchone()

        if row:
            self.curiosity = row[1]
            self.bravery = row[2]
            self.playfulness = row[3]
            self.loyalty = row[4]
            self.independence = row[5]
        else:
            # Default values if not found
            from config import Config
            self.curiosity = Config.PERSONALITY_CURIOSITY
            self.bravery = Config.PERSONALITY_BRAVERY
            self.playfulness = Config.PERSONALITY_PLAYFULNESS
            self.loyalty = Config.PERSONALITY_LOYALTY
            self.independence = Config.PERSONALITY_INDEPENDENCE

        conn.close()

    def save(self):
        """Save personality to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE personality SET
                curiosity = ?,
                bravery = ?,
                playfulness = ?,
                loyalty = ?,
                independence = ?
            WHERE id = 1
        """, (
            self.curiosity,
            self.bravery,
            self.playfulness,
            self.loyalty,
            self.independence
        ))

        conn.commit()
        conn.close()

    def adjust_trait(self, trait: str, delta: int):
        """
        Gradually adjust a personality trait
        Traits evolve slowly based on experiences
        """
        if hasattr(self, trait):
            current = getattr(self, trait)
            new_value = max(0, min(10, current + delta))
            setattr(self, trait, new_value)

    def get_influence(self, trait: str) -> float:
        """
        Get normalized influence of a trait (0.0 to 1.0)
        """
        if hasattr(self, trait):
            return getattr(self, trait) / 10.0
        return 0.5

    def to_dict(self) -> Dict[str, int]:
        """Export personality as dictionary"""
        return {
            'curiosity': self.curiosity,
            'bravery': self.bravery,
            'playfulness': self.playfulness,
            'loyalty': self.loyalty,
            'independence': self.independence
        }

    def get_dominant_traits(self, threshold: int = 7) -> list:
        """Get list of traits above threshold"""
        traits = []
        if self.curiosity >= threshold:
            traits.append('curious')
        if self.bravery >= threshold:
            traits.append('brave')
        if self.playfulness >= threshold:
            traits.append('playful')
        if self.loyalty >= threshold:
            traits.append('loyal')
        if self.independence >= threshold:
            traits.append('independent')
        return traits

    def __repr__(self):
        return (f"<Personality: Curiosity={self.curiosity} Bravery={self.bravery} "
                f"Playfulness={self.playfulness} Loyalty={self.loyalty} "
                f"Independence={self.independence}>")
