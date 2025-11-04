"""
Item System for EeveeLLM

Defines items, their effects, and usage mechanics.
Phase 5: Enhanced item system with functional effects.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, Callable
from enum import Enum


class ItemType(Enum):
    """Categories of items"""
    BERRY = "berry"
    MEDICINE = "medicine"
    TREASURE = "treasure"
    TOY = "toy"
    FOOD = "food"


class ItemRarity(Enum):
    """Item rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    VERY_RARE = "very_rare"


@dataclass
class ItemEffect:
    """
    Represents the effect of using an item

    Effects modify Eevee's state when the item is used.
    """
    hunger_delta: int = 0
    energy_delta: int = 0
    happiness_delta: int = 0
    health_delta: int = 0
    description: str = ""

    def apply(self, current_state: Dict[str, int]) -> Dict[str, int]:
        """
        Apply this effect to a state dict

        Args:
            current_state: Dict with hunger, energy, happiness, health keys

        Returns:
            Dict with updated values (clamped 0-100)
        """
        return {
            'hunger': max(0, min(100, current_state.get('hunger', 50) + self.hunger_delta)),
            'energy': max(0, min(100, current_state.get('energy', 50) + self.energy_delta)),
            'happiness': max(0, min(100, current_state.get('happiness', 70) + self.happiness_delta)),
            'health': max(0, min(100, current_state.get('health', 100) + self.health_delta))
        }


@dataclass
class Item:
    """
    Represents an item in the game

    Items can be found, given, and used to affect Eevee's state.
    """
    id: str
    name: str
    item_type: ItemType
    rarity: ItemRarity
    description: str
    effect: ItemEffect
    consumable: bool = True
    emoji: str = "📦"

    def use(self, current_state: Dict[str, int]) -> tuple[Dict[str, int], str]:
        """
        Use this item

        Args:
            current_state: Current state values

        Returns:
            Tuple of (new_state, response_message)
        """
        new_state = self.effect.apply(current_state)

        # Generate response based on effect
        response_parts = ["*Eevee uses the item*", self.effect.description]

        # Add emotional response based on effect
        total_positive = (
            max(0, -self.effect.hunger_delta) +  # Hunger decrease is good
            max(0, self.effect.energy_delta) +
            max(0, self.effect.happiness_delta) +
            max(0, self.effect.health_delta)
        )

        if total_positive > 30:
            response_parts.append("*Eevee looks very happy!* Vee vee!")
        elif total_positive > 15:
            response_parts.append("*Eevee wags tail* Vee!")
        else:
            response_parts.append("*Eevee seems content*")

        return new_state, " ".join(response_parts)


# ============================================================================
# ITEM CATALOG
# ============================================================================

ITEMS_CATALOG: Dict[str, Item] = {
    # --- BERRIES (Common healing items) ---

    "oran_berry": Item(
        id="oran_berry",
        name="Oran Berry",
        item_type=ItemType.BERRY,
        rarity=ItemRarity.COMMON,
        description="A sweet blue berry that restores health and reduces hunger",
        effect=ItemEffect(
            hunger_delta=-25,
            health_delta=15,
            happiness_delta=5,
            description="*crunch crunch* The sweet juice restores vitality!"
        ),
        emoji="🫐"
    ),

    "pecha_berry": Item(
        id="pecha_berry",
        name="Pecha Berry",
        item_type=ItemType.BERRY,
        rarity=ItemRarity.COMMON,
        description="A pink berry that heals and provides energy",
        effect=ItemEffect(
            hunger_delta=-20,
            energy_delta=10,
            health_delta=10,
            happiness_delta=5,
            description="*nom nom* The refreshing taste energizes!"
        ),
        emoji="🍑"
    ),

    "sitrus_berry": Item(
        id="sitrus_berry",
        name="Sitrus Berry",
        item_type=ItemType.BERRY,
        rarity=ItemRarity.UNCOMMON,
        description="A rare golden berry with powerful healing properties",
        effect=ItemEffect(
            hunger_delta=-30,
            health_delta=25,
            happiness_delta=8,
            description="*munch munch* The golden berry has amazing healing power!"
        ),
        emoji="✨🍊"
    ),

    "leppa_berry": Item(
        id="leppa_berry",
        name="Leppa Berry",
        item_type=ItemType.BERRY,
        rarity=ItemRarity.UNCOMMON,
        description="A red berry that greatly restores energy",
        effect=ItemEffect(
            hunger_delta=-15,
            energy_delta=30,
            happiness_delta=5,
            description="*crunch* A burst of energy surges through!"
        ),
        emoji="🍒"
    ),

    # --- FOOD (Satisfying items) ---

    "poke_puff": Item(
        id="poke_puff",
        name="Poké Puff",
        item_type=ItemType.FOOD,
        rarity=ItemRarity.COMMON,
        description="A fluffy pastry that makes Pokémon happy",
        effect=ItemEffect(
            hunger_delta=-20,
            happiness_delta=15,
            description="*nom nom nom* So delicious and fluffy!"
        ),
        emoji="🧁"
    ),

    "moomoo_milk": Item(
        id="moomoo_milk",
        name="Moomoo Milk",
        item_type=ItemType.FOOD,
        rarity=ItemRarity.COMMON,
        description="Fresh milk that restores health and reduces hunger",
        effect=ItemEffect(
            hunger_delta=-30,
            health_delta=20,
            happiness_delta=5,
            description="*slurp slurp* The creamy milk is so soothing!"
        ),
        emoji="🥛"
    ),

    # --- MEDICINE (Powerful healing) ---

    "potion": Item(
        id="potion",
        name="Potion",
        item_type=ItemType.MEDICINE,
        rarity=ItemRarity.UNCOMMON,
        description="A spray-type medicine that heals wounds",
        effect=ItemEffect(
            health_delta=30,
            description="*spray* The medicine soothes injuries!"
        ),
        emoji="🧪"
    ),

    "full_heal": Item(
        id="full_heal",
        name="Full Heal",
        item_type=ItemType.MEDICINE,
        rarity=ItemRarity.RARE,
        description="A miracle medicine that fully restores health",
        effect=ItemEffect(
            health_delta=50,
            happiness_delta=10,
            description="*sparkle* All wounds heal instantly!"
        ),
        emoji="💊✨"
    ),

    # --- TOYS (Happiness boosters) ---

    "poke_toy": Item(
        id="poke_toy",
        name="Poké Toy",
        item_type=ItemType.TOY,
        rarity=ItemRarity.COMMON,
        description="A fun toy that brings joy",
        effect=ItemEffect(
            happiness_delta=20,
            energy_delta=-5,
            description="*plays excitedly* This toy is so fun!"
        ),
        consumable=False,
        emoji="🎾"
    ),

    "soft_plush": Item(
        id="soft_plush",
        name="Soft Plush",
        item_type=ItemType.TOY,
        rarity=ItemRarity.UNCOMMON,
        description="A cuddly plush that provides comfort",
        effect=ItemEffect(
            happiness_delta=15,
            energy_delta=10,
            description="*cuddles with plush* So soft and comforting!"
        ),
        consumable=False,
        emoji="🧸"
    ),

    # --- TREASURES (Special rare items) ---

    "shiny_stone": Item(
        id="shiny_stone",
        name="Shiny Stone",
        item_type=ItemType.TREASURE,
        rarity=ItemRarity.RARE,
        description="A beautiful stone that sparkles in the light",
        effect=ItemEffect(
            happiness_delta=25,
            description="*stares in wonder* It's so pretty and sparkly!"
        ),
        consumable=False,
        emoji="💎"
    ),

    "rainbow_wing": Item(
        id="rainbow_wing",
        name="Rainbow Wing",
        item_type=ItemType.TREASURE,
        rarity=ItemRarity.VERY_RARE,
        description="A mysterious feather that shimmers with rainbow colors",
        effect=ItemEffect(
            happiness_delta=30,
            health_delta=20,
            description="*awestruck* The rainbow colors fill you with hope and joy!"
        ),
        consumable=False,
        emoji="🌈🪶"
    ),

    "old_amber": Item(
        id="old_amber",
        name="Old Amber",
        item_type=ItemType.TREASURE,
        rarity=ItemRarity.VERY_RARE,
        description="Ancient amber with something preserved inside",
        effect=ItemEffect(
            happiness_delta=20,
            description="*fascinated* What mysteries does this hold?"
        ),
        consumable=False,
        emoji="🟡"
    ),

    "translation_collar": Item(
        id="translation_collar",
        name="Translation Collar",
        item_type=ItemType.TREASURE,
        rarity=ItemRarity.VERY_RARE,
        description="A mystical collar that allows Pokemon to speak in simple human language",
        effect=ItemEffect(
            happiness_delta=15,
            description="*collar glows softly* Me can talk! Words come easy now!"
        ),
        consumable=False,
        emoji="📿✨"
    ),
}


class ItemManager:
    """
    Manages item operations and queries

    Provides convenience methods for working with the item catalog.
    """

    @staticmethod
    def get_item(item_id: str) -> Optional[Item]:
        """Get an item by ID"""
        return ITEMS_CATALOG.get(item_id.lower().replace(" ", "_"))

    @staticmethod
    def get_item_by_name(name: str) -> Optional[Item]:
        """Get an item by display name (case insensitive)"""
        name_lower = name.lower()
        for item in ITEMS_CATALOG.values():
            if item.name.lower() == name_lower:
                return item
        return None

    @staticmethod
    def get_items_by_type(item_type: ItemType) -> list[Item]:
        """Get all items of a specific type"""
        return [item for item in ITEMS_CATALOG.values() if item.item_type == item_type]

    @staticmethod
    def get_items_by_rarity(rarity: ItemRarity) -> list[Item]:
        """Get all items of a specific rarity"""
        return [item for item in ITEMS_CATALOG.values() if item.rarity == rarity]

    @staticmethod
    def get_all_items() -> list[Item]:
        """Get all items in catalog"""
        return list(ITEMS_CATALOG.values())

    @staticmethod
    def get_random_item_by_rarity(rarity: ItemRarity) -> Optional[Item]:
        """Get a random item of specified rarity"""
        import random
        items = ItemManager.get_items_by_rarity(rarity)
        return random.choice(items) if items else None

    @staticmethod
    def get_discoverable_items() -> list[Item]:
        """
        Get items that can be discovered during exploration

        Returns items sorted by rarity (common first)
        """
        rarity_order = {
            ItemRarity.COMMON: 0,
            ItemRarity.UNCOMMON: 1,
            ItemRarity.RARE: 2,
            ItemRarity.VERY_RARE: 3
        }

        items = [
            item for item in ITEMS_CATALOG.values()
            if item.item_type in [ItemType.BERRY, ItemType.TREASURE, ItemType.TOY]
        ]

        return sorted(items, key=lambda x: rarity_order[x.rarity])
