"""
Natural Language Intent Parser

Detects user intent from natural language input and converts it to commands.
Allows users to interact naturally instead of using exact command syntax.

Examples:
  "What are your stats?" → stats command
  "Can you show me your health?" → stats command
  "Let's go to the meadow" → go meadow
  "I want to pet you" → pet command
  "Show me what you have" → inventory command
"""

import re
from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass


@dataclass
class Intent:
    """Detected user intent"""
    command: str  # The command to execute
    args: str = ""  # Arguments for the command
    confidence: float = 1.0  # Confidence score (0.0-1.0)
    is_natural_language: bool = True  # True if parsed from NL, False if exact command


class IntentParser:
    """
    Parses natural language input to detect user intent.

    Uses pattern matching to identify common phrasings and convert them
    to executable commands.
    """

    def __init__(self):
        """Initialize intent parser with pattern definitions"""

        # Pattern categories for each command
        # Format: (pattern, command, extract_args_function, confidence)

        self.patterns = self._build_patterns()

    def _build_patterns(self) -> List[Tuple[str, str, Optional[callable], float]]:
        """Build pattern list for intent detection"""

        patterns = []

        # === STATS COMMAND ===
        stats_patterns = [
            (r"(show|view|check|what are|what's|display)\s+(me\s+)?(your\s+)?(stats?|status|health|condition|state)", "stats", None, 1.0),
            (r"how (are you|is your health|are you feeling)", "stats", None, 0.9),
            (r"(are you (okay|ok|alright|hungry|tired))", "stats", None, 0.9),
            (r"what'?s your (health|energy|happiness|hunger)", "stats", None, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in stats_patterns])

        # === INVENTORY COMMAND ===
        inventory_patterns = [
            (r"(show|view|check|what's in|display)\s+(me\s+)?(your\s+)?(inventory|items?|bag|stuff|things?)", "inventory", None, 1.0),
            (r"what (do you have|have you got)", "inventory", None, 1.0),
            (r"what (items?|things?) (are you|you are) carrying", "inventory", None, 1.0),
            (r"(let me see|show me)\s+(what you have|your (items?|stuff|things?))", "inventory", None, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in inventory_patterns])

        # === PET COMMAND ===
        pet_patterns = [
            (r"(i('d like to|want to|'ll|will)\s+)?pet\s+(you|eevee)", "pet", None, 1.0),
            (r"(can i|let me|i want to)\s+pet\s+(you|eevee)", "pet", None, 1.0),
            (r"(give you|you get)\s+some\s+(pets?|pats?)", "pet", None, 1.0),
            (r"(head\s+)?(pat|scratch|rub)(?!\s+(the|this))", "pet", None, 0.8),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in pet_patterns])

        # === PLAY COMMAND ===
        play_patterns = [
            (r"(let'?s|do you (want to|wanna)|want to|wanna)\s+play", "play", None, 1.0),
            (r"play(time)?( with (me|you))?(!)?$", "play", None, 1.0),
            (r"(feel like playing|up for (some\s+)?play)", "play", None, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in play_patterns])

        # === OBSERVE COMMAND ===
        observe_patterns = [
            (r"^(what are you doing|what'?s (happening|going on)|what are you up to)", "observe", None, 1.0),
            (r"^(show me|let me see)\s+what you'?re doing", "observe", None, 1.0),
            (r"^observe", "observe", None, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in observe_patterns])

        # === WORLD COMMAND ===
        world_patterns = [
            (r"^(where are we|where am i|where is this|what'?s this place)", "world", None, 1.0),
            (r"^(show|describe|tell me about)\s+(the\s+)?(area|location|place|surroundings?)", "world", None, 1.0),
            (r"^look around", "world", None, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in world_patterns])

        # === GO/TRAVEL COMMAND ===
        # These need special handling to extract location
        go_patterns = [
            (r"^(let'?s\s+)?(go|travel|head|move)\s+(to\s+)?(the\s+)?(.+)", "go", self._extract_location, 1.0),
            (r"^(take me|let'?s go)\s+(to\s+)?(the\s+)?(.+)", "go", self._extract_location, 1.0),
            (r"^(can we|shall we)\s+go\s+(to\s+)?(the\s+)?(.+)", "go", self._extract_location, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in go_patterns])

        # === GIVE COMMAND ===
        give_patterns = [
            (r"^(i('ll|will)\s+)?give\s+(you\s+)?(a\s+|an\s+)?(.+)", "give", self._extract_item, 1.0),
            (r"^(here'?s|have)\s+(a\s+|an\s+|some\s+)?(.+)", "give", self._extract_item_simple, 1.0),
            (r"^(take|you can have)\s+(this\s+|a\s+|an\s+)?(.+)", "give", self._extract_item_simple, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in give_patterns])

        # === USE COMMAND ===
        use_patterns = [
            (r"^(let'?s\s+)?use\s+(the\s+|a\s+|an\s+)?(.+)", "use", self._extract_item_simple, 1.0),
            (r"^(i want to|let me)\s+use\s+(the\s+)?(.+)", "use", self._extract_item_simple, 1.0),
            (r"^(can you|you should)\s+use\s+(the\s+)?(.+)", "use", self._extract_item_simple, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in use_patterns])

        # === DROP COMMAND ===
        drop_patterns = [
            (r"^(drop|remove|get rid of)\s+(the\s+)?(.+)", "drop", self._extract_item_simple, 1.0),
            (r"^(i don'?t want|we don'?t need)\s+(the\s+)?(.+)", "drop", self._extract_item_simple, 0.9),
            (r"^(throw away|toss)\s+(the\s+)?(.+)", "drop", self._extract_item_simple, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in drop_patterns])

        # === TIMELINE COMMAND ===
        # NOTE: Must come BEFORE remember patterns to avoid "what happened" conflict
        timeline_patterns = [
            (r"what (did you do|have you been doing)", "timeline", None, 1.0),
            (r"what have you been up to", "timeline", None, 1.0),
            (r"show me what you('ve| have) been (up to|doing)", "timeline", None, 1.0),
            (r"(show|view)\s+(me\s+)?(the\s+)?(timeline|recent activities|history)", "timeline", None, 1.0),
            (r"what (happened|did you do)\s+(while i was (gone|away)|recently|today|lately)", "timeline", None, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in timeline_patterns])

        # === REMEMBER/MEMORY COMMAND ===
        remember_patterns = [
            (r"(do you remember|can you recall|what do you remember about)\s+(.+)", "remember", self._extract_query, 1.0),
            (r"(show|view)\s+(me\s+)?(your\s+)?memories(\s+about\s+(.+))?", "remember", self._extract_memory_query, 0.9),
            (r"remember\s+(.+)", "remember", self._extract_query, 1.0),
            (r"what happened\s+(.+)", "remember", self._extract_query, 0.8),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in remember_patterns])

        # === HELP COMMAND ===
        help_patterns = [
            (r"^(help|what can (i|you) do|commands?|how do (i|you))", "help", None, 1.0),
            (r"^(show|list)\s+(available\s+)?(commands?|options)", "help", None, 1.0),
        ]
        patterns.extend([(p, c, a, conf) for p, c, a, conf in help_patterns])

        return patterns

    # === Argument Extraction Functions ===

    def _extract_location(self, match: re.Match) -> str:
        """Extract location from go/travel patterns"""
        # Get the last group (location name)
        groups = match.groups()
        location = groups[-1] if groups else ""
        return location.strip()

    def _extract_item(self, match: re.Match) -> str:
        """Extract item from give patterns"""
        groups = match.groups()
        item = groups[-1] if groups else ""
        return item.strip()

    def _extract_item_simple(self, match: re.Match) -> str:
        """Extract item from simpler patterns"""
        groups = match.groups()
        item = groups[-1] if groups else ""
        return item.strip()

    def _extract_query(self, match: re.Match) -> str:
        """Extract query from remember patterns"""
        groups = match.groups()
        query = groups[-1] if groups else ""
        return query.strip() if query else ""

    def _extract_memory_query(self, match: re.Match) -> str:
        """Extract query from 'show memories about X' patterns"""
        groups = match.groups()
        # Get last non-None group
        for group in reversed(groups):
            if group:
                return group.strip()
        return ""

    # === Main Parsing Function ===

    def parse(self, user_input: str) -> Optional[Intent]:
        """
        Parse user input and detect intent.

        Args:
            user_input: Raw user input string

        Returns:
            Intent object if pattern matched, None otherwise
        """
        if not user_input:
            return None

        # Normalize input
        normalized = user_input.strip().lower()

        # Check each pattern
        for pattern, command, extract_args, confidence in self.patterns:
            match = re.search(pattern, normalized, re.IGNORECASE)
            if match:
                # Extract arguments if function provided
                args = ""
                if extract_args:
                    args = extract_args(match)

                return Intent(
                    command=command,
                    args=args,
                    confidence=confidence,
                    is_natural_language=True
                )

        # No pattern matched
        return None

    def get_command_examples(self, command: str) -> List[str]:
        """
        Get example natural language phrasings for a command.

        Args:
            command: Command name (e.g., "stats", "inventory")

        Returns:
            List of example phrasings
        """
        examples = {
            "stats": [
                "What are your stats?",
                "How are you feeling?",
                "Show me your health",
                "Are you okay?",
                "What's your energy level?"
            ],
            "inventory": [
                "Show me your inventory",
                "What do you have?",
                "What items are you carrying?",
                "Let me see your stuff"
            ],
            "pet": [
                "I want to pet you",
                "Can I pet you?",
                "Give you some pets",
                "Head pat"
            ],
            "play": [
                "Let's play!",
                "Do you want to play?",
                "Want to play?",
                "Feel like playing?"
            ],
            "observe": [
                "What are you doing?",
                "What's happening?",
                "What are you up to?",
                "Let me see what you're doing"
            ],
            "world": [
                "Where are we?",
                "Look around",
                "Describe this place",
                "What's this location?"
            ],
            "go": [
                "Let's go to the meadow",
                "Take me to the forest",
                "Can we go to the park?",
                "Travel to the beach"
            ],
            "give": [
                "Give you an Oran Berry",
                "Here's a berry",
                "Take this Potion",
                "You can have this Pecha Berry"
            ],
            "use": [
                "Use the Oran Berry",
                "Let's use a Potion",
                "Can you use this berry?",
                "Use that medicine"
            ],
            "drop": [
                "Drop the old stick",
                "Remove that item",
                "Get rid of the trash",
                "Throw away the junk"
            ],
            "remember": [
                "Do you remember the park?",
                "What do you remember about yesterday?",
                "Show me your memories",
                "Can you recall what happened?"
            ],
            "timeline": [
                "What did you do while I was gone?",
                "Show me the timeline",
                "What have you been up to?",
                "What happened recently?"
            ],
            "help": [
                "Help",
                "What can I do?",
                "Show me the commands",
                "How do I interact with you?"
            ]
        }
        return examples.get(command, [])
