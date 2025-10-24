"""
EeveeLLM Configuration System
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Data directory
DATA_DIR = PROJECT_ROOT / "data"
MEMORIES_DIR = DATA_DIR / "memories"

# Database paths
DATABASE_PATH = DATA_DIR / "eevee_save.db"
WORLD_STATE_PATH = DATA_DIR / "world_state.json"

# Ensure data directories exist
DATA_DIR.mkdir(exist_ok=True)
MEMORIES_DIR.mkdir(exist_ok=True)


class Config:
    """Configuration management for EeveeLLM"""

    # NanoGPT Settings
    NANOGPT_API_KEY: str = os.getenv("NANOGPT_API_KEY", "")
    NANOGPT_ENDPOINT: str = os.getenv("NANOGPT_ENDPOINT", "https://api.nanogpt.com/v1/generate")
    NANOGPT_MODEL: str = "gpt-2-medium"
    NANOGPT_MAX_TOKENS: int = 150
    NANOGPT_TEMPERATURE: float = 0.8

    # Time Settings
    TIME_ACCELERATION: float = 1.0  # 1.0 = real-time
    ACTIVITY_FREQUENCY: str = "hourly"
    SIGNIFICANT_EVENT_CHANCE: float = 0.15  # 15% chance per day

    # Memory Settings
    MEMORY_SIGNIFICANCE_THRESHOLD: float = 6.0  # 0-10 scale
    MAX_WORKING_MEMORY: int = 10
    MEMORY_RETRIEVAL_COUNT: int = 5
    FORGETTING_RATE: float = 0.01

    # Eevee Initial Personality (0-10 scale)
    PERSONALITY_CURIOSITY: int = 8
    PERSONALITY_BRAVERY: int = 5
    PERSONALITY_PLAYFULNESS: int = 9
    PERSONALITY_LOYALTY: int = 10
    PERSONALITY_INDEPENDENCE: int = 6

    # Eevee Initial Physical State (0-100 scale)
    INITIAL_HUNGER: int = 40
    INITIAL_ENERGY: int = 70
    INITIAL_HEALTH: int = 95
    INITIAL_HAPPINESS: int = 85

    # Relationship Settings
    INITIAL_TRUST: int = 50
    INITIAL_BOND: int = 30

    # World Settings
    STARTING_LOCATION: str = "trainer_home"
    WEATHER_CHANGE_FREQUENCY: str = "daily"
    ENABLE_RANDOM_EVENTS: bool = True

    # Brain Council Vote Weights (percentages)
    VOTE_WEIGHT_PREFRONTAL: float = 0.25
    VOTE_WEIGHT_AMYGDALA: float = 0.30
    VOTE_WEIGHT_HIPPOCAMPUS: float = 0.20
    VOTE_WEIGHT_HYPOTHALAMUS: float = 0.15
    VOTE_WEIGHT_CEREBELLUM: float = 0.10

    # Brain Council Stress Modifiers
    AMYGDALA_STRESS_WEIGHT: float = 0.60  # Under threat

    # Debug Settings
    SHOW_BRAIN_COUNCIL: bool = False
    SHOW_MEMORY_RETRIEVAL: bool = False
    VERBOSE_LOGGING: bool = True
    DEBUG_MODE: bool = False

    # UI Settings
    DISPLAY_WIDTH: int = 80
    USE_COLOR: bool = True
    SHOW_STATS_BAR: bool = True

    @classmethod
    def load_from_file(cls, config_path: str = "config.yaml") -> None:
        """Load configuration from YAML file"""
        config_file = PROJECT_ROOT / config_path
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
                if config_data:
                    cls._update_from_dict(config_data)

    @classmethod
    def _update_from_dict(cls, config_dict: Dict[str, Any]) -> None:
        """Update config from dictionary"""
        for key, value in config_dict.items():
            attr_name = key.upper()
            if hasattr(cls, attr_name):
                setattr(cls, attr_name, value)

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        return {
            key.lower(): value
            for key, value in cls.__dict__.items()
            if not key.startswith('_') and key.isupper()
        }

    @classmethod
    def save_to_file(cls, config_path: str = "config.yaml") -> None:
        """Save current configuration to YAML file"""
        config_file = PROJECT_ROOT / config_path
        with open(config_file, 'w') as f:
            yaml.dump(cls.to_dict(), f, default_flow_style=False)


# Try to load config from file if it exists
try:
    Config.load_from_file()
except Exception as e:
    print(f"Warning: Could not load config file: {e}")
    print("Using default configuration")


# Create a default config.yaml if it doesn't exist
if not (PROJECT_ROOT / "config.yaml").exists():
    Config.save_to_file()
