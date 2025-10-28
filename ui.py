"""
Terminal UI for EeveeLLM
Handles display and user interaction
"""
import sys
from typing import Optional
from colorama import init, Fore, Style, Back

from config import Config

# Initialize colorama
init(autoreset=True)


class TerminalUI:
    """Terminal interface for interacting with Eevee"""

    def __init__(self, width: int = None, use_color: bool = None):
        self.width = width or Config.DISPLAY_WIDTH
        self.use_color = use_color if use_color is not None else Config.USE_COLOR

    def clear_screen(self):
        """Clear the terminal screen"""
        print("\033[2J\033[H", end="")

    def print_header(self, location_name: str, time_of_day: str, weather: str):
        """Print the scene header"""
        separator = "=" * self.width

        # Weather emoji
        weather_emoji = {
            'sunny': '☀️',
            'rainy': '🌧️',
            'cloudy': '☁️',
            'stormy': '⛈️',
            'night': '🌙'
        }.get(weather.lower(), '🌤️')

        # Time emoji
        time_emoji = {
            'morning': '🌅',
            'afternoon': '☀️',
            'evening': '🌆',
            'night': '🌙'
        }.get(time_of_day.lower(), '🌤️')

        header = f"🌲 {location_name.upper()} - {time_of_day.upper()} {weather_emoji}"

        if self.use_color:
            print(Fore.CYAN + separator)
            print(Fore.YELLOW + Style.BRIGHT + header.center(self.width))
            print(Fore.CYAN + separator + Style.RESET_ALL)
        else:
            print(separator)
            print(header)
            print(separator)

    def print_stats_bar(self, hunger: int, energy: int, happiness: int, health: int = 100):
        """Print visual stats bar"""
        def make_bar(value: int, length: int = 10) -> str:
            filled = int(value / 10)
            return "█" * filled + "░" * (length - filled)

        stats = (
            f"Energy: {make_bar(energy)} {energy}% | "
            f"Happiness: {make_bar(happiness)} {happiness}% | "
            f"Hunger: {make_bar(hunger)} {hunger}%"
        )

        if self.use_color:
            # Color code based on values
            if energy < 30:
                energy_color = Fore.RED
            elif energy < 60:
                energy_color = Fore.YELLOW
            else:
                energy_color = Fore.GREEN

            if happiness < 30:
                happy_color = Fore.RED
            elif happiness < 60:
                happy_color = Fore.YELLOW
            else:
                happy_color = Fore.GREEN

            if hunger > 70:
                hunger_color = Fore.RED
            elif hunger > 50:
                hunger_color = Fore.YELLOW
            else:
                hunger_color = Fore.GREEN

            print(f"[{energy_color}{make_bar(energy)}{Style.RESET_ALL} {energy}% | "
                  f"{happy_color}{make_bar(happiness)}{Style.RESET_ALL} {happiness}% | "
                  f"{hunger_color}{make_bar(hunger)}{Style.RESET_ALL} {hunger}%]")
        else:
            print(f"[{stats}]")
        print()

    def print_message(self, message: str, prefix: str = ""):
        """Print a message with optional prefix"""
        if prefix:
            if self.use_color:
                print(f"{Fore.CYAN}{prefix}{Style.RESET_ALL} {message}")
            else:
                print(f"{prefix} {message}")
        else:
            print(message)

    def print_user_input(self, text: str):
        """Print user input"""
        if self.use_color:
            print(f"\n{Fore.GREEN}You:{Style.RESET_ALL} {text}")
        else:
            print(f"\nYou: {text}")

    def _format_eevee_response(self, response: str) -> str:
        """
        Format Eevee's response with color-coded actions and speech.

        Actions (in *asterisks*) -> Dim/Gray
        Speech ("quotes" or Vee sounds) -> Bright Cyan
        Regular text -> Default
        """
        if not self.use_color:
            return response

        import re
        formatted = ""
        last_end = 0

        # Pattern to match:
        # 1. Actions in asterisks: *like this*
        # 2. Quoted speech: "like this"
        # 3. Vee sounds: Vee, Veevee, etc.
        pattern = r'(\*[^*]+\*)|("([^"]*)"|\'([^\']*)\')|(\b[Vv]ee+[!?~.]*\b)'

        for match in re.finditer(pattern, response):
            # Add any text before this match (regular text)
            if match.start() > last_end:
                formatted += response[last_end:match.start()]

            matched_text = match.group(0)

            if matched_text.startswith('*') and matched_text.endswith('*'):
                # Actions - dim/gray color
                formatted += f"{Style.DIM}{Fore.WHITE}{matched_text}{Style.RESET_ALL}"
            elif matched_text.startswith('"') or matched_text.startswith("'"):
                # Quoted speech - bright cyan
                formatted += f"{Style.BRIGHT}{Fore.CYAN}{matched_text}{Style.RESET_ALL}"
            elif matched_text.lower().startswith('vee'):
                # Vee sounds - bright cyan
                formatted += f"{Style.BRIGHT}{Fore.CYAN}{matched_text}{Style.RESET_ALL}"
            else:
                formatted += matched_text

            last_end = match.end()

        # Add any remaining text
        if last_end < len(response):
            formatted += response[last_end:]

        return formatted

    def print_eevee_response(self, response: str):
        """Print Eevee's response with color-coded formatting"""
        formatted_response = self._format_eevee_response(response)

        if self.use_color:
            print(f"\n{Fore.MAGENTA}Eevee:{Style.RESET_ALL} {formatted_response}\n")
        else:
            print(f"\nEevee: {response}\n")

    def print_system_message(self, message: str):
        """Print system message"""
        if self.use_color:
            print(f"{Fore.YELLOW}[{message}]{Style.RESET_ALL}")
        else:
            print(f"[{message}]")

    def print_debug(self, message: str):
        """Print debug information"""
        if self.use_color:
            print(f"{Fore.BLUE}DEBUG: {message}{Style.RESET_ALL}")
        else:
            print(f"DEBUG: {message}")

    def print_separator(self):
        """Print separator line"""
        print("=" * self.width)

    def print_location_description(self, description: str):
        """Print location description"""
        print(f"\n{description}\n")

    def get_input(self, prompt: str = "> ") -> str:
        """Get user input"""
        try:
            if self.use_color:
                return input(f"{Fore.WHITE}{Style.BRIGHT}{prompt}{Style.RESET_ALL}").strip()
            else:
                return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return "exit"

    def print_help(self):
        """Print help message"""
        help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                    EeveeLLM - Available Commands                     ║
╚══════════════════════════════════════════════════════════════════════╝

💡 TIP: You can use NATURAL LANGUAGE! No need for exact commands.
   Examples: "How are you?" "What do you have?" "Let's go to the meadow"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 CHECK STATUS
  stats                 - View Eevee's current state
  💬 Try: "How are you?" "Are you okay?" "What's your energy level?"

👀 OBSERVE
  observe               - See what Eevee is currently doing
  💬 Try: "What are you doing?" "What's happening?"

🗺️  WORLD & TRAVEL
  world                 - See current location and surroundings
  💬 Try: "Where are we?" "Look around"

  go [location]         - Travel to a connected location
  💬 Try: "Let's go to the meadow" "Take me to the forest"

🤝 INTERACT
  pet                   - Pet Eevee
  💬 Try: "I want to pet you" "Can I pet you?" "Head pat"

  play                  - Initiate playtime
  💬 Try: "Let's play!" "Want to play?" "Feel like playing?"

  talk [message]        - Speak to Eevee (or just type naturally!)
  💬 Try: "Hello Eevee!" "You're so cute!" "I love you"

🎒 INVENTORY & ITEMS
  inventory             - View Eevee's inventory
  💬 Try: "What do you have?" "Show me your stuff"

  give [item]           - Give Eevee an item
  💬 Try: "Here's an Oran Berry" "Take this Potion"

  use [item]            - Use an item from inventory
  💬 Try: "Use the Oran Berry" "Let's use a Potion"

  drop [item]           - Drop/remove an item from inventory
  💬 Try: "Drop the stick" "Get rid of the trash"

🧠 MEMORY & TIME
  remember [query]      - Browse Eevee's memories
  💬 Try: "Do you remember the park?" "Show me your memories"

  timeline              - View recent autonomous activities
  💬 Try: "What did you do?" "What have you been up to?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  SYSTEM
  help                  - Show this help message
  exit / quit           - Save and quit

🐛 DEBUG COMMANDS
  debug on/off          - Toggle full debug mode
  debug brain           - Toggle brain council visualization
  debug memory          - Toggle memory retrieval visualization
  debug state           - Show detailed state
  debug time [hours]    - Simulate time passage for testing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 For more examples, see: NATURAL_LANGUAGE_COMMANDS.md
        """
        print(help_text)

    def print_welcome(self):
        """Print welcome message"""
        welcome = """
╔══════════════════════════════════════════════════════════════════════╗
║                       Welcome to EeveeLLM! 🌟                        ║
║                                                                      ║
║              Your AI Eevee companion is excited to see you!          ║
║                                                                      ║
║  💬 Just talk naturally! Try:                                        ║
║     "Hello!" • "How are you?" • "Let's play!" • "What do you have?" ║
║                                                                      ║
║  📖 Type 'help' for all commands                                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
        """
        if self.use_color:
            print(Fore.CYAN + Style.BRIGHT + welcome + Style.RESET_ALL)
        else:
            print(welcome)

    def print_goodbye(self):
        """Print goodbye message"""
        goodbye = """
Saving your adventure...

Eevee watches as you prepare to leave.
*Eevee nuzzles your hand one last time* Veee~

Until next time, trainer!
        """
        if self.use_color:
            print(Fore.YELLOW + goodbye + Style.RESET_ALL)
        else:
            print(goodbye)

    def print_error(self, error: str):
        """Print error message"""
        if self.use_color:
            print(f"{Fore.RED}Error: {error}{Style.RESET_ALL}")
        else:
            print(f"Error: {error}")

    def print_thinking(self, message: str):
        """
        Show a thinking/loading indicator.

        This prints on the same line and can be cleared later.
        Used for operations that take 1+ seconds.
        """
        if self.use_color:
            print(f"{Fore.BLUE}{Style.DIM}{message}{Style.RESET_ALL}", end='', flush=True)
        else:
            print(f"{message}", end='', flush=True)

    def clear_thinking(self):
        """Clear the thinking indicator line"""
        # Print spaces to cover the line, then carriage return
        print('\r' + ' ' * 80 + '\r', end='', flush=True)

    def print_warning(self, message: str):
        """Print warning message (yellow with emoji)"""
        if self.use_color:
            print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")
        else:
            print(f"Warning: {message}")

    def print_success(self, message: str):
        """Print success message (green with checkmark)"""
        if self.use_color:
            print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
        else:
            print(f"✓ {message}")

    def print_info(self, message: str):
        """Print info message (blue with info icon)"""
        if self.use_color:
            print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")
        else:
            print(f"Info: {message}")

    def confirm(self, message: str, default: bool = False) -> bool:
        """
        Ask for yes/no confirmation.

        Args:
            message: The question to ask
            default: Default answer if user just presses enter

        Returns:
            True if user confirmed, False otherwise
        """
        default_str = "[Y/n]" if default else "[y/N]"
        prompt = f"{message} {default_str}: "

        try:
            if self.use_color:
                response = input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}").strip().lower()
            else:
                response = input(prompt).strip().lower()

            if not response:
                return default

            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            return False

    def print_stat_bar(self, label: str, value: int, max_value: int = 100,
                       emoji: str = "", reverse: bool = False) -> str:
        """
        Create a visual stat bar with context indicator.

        Args:
            label: Stat name (e.g., "Health", "Hunger")
            value: Current value
            max_value: Maximum value (default 100)
            emoji: Emoji to show before label
            reverse: If True, high values are bad (e.g., hunger)

        Returns:
            Formatted stat bar string
        """
        # Calculate percentage and bar
        percentage = int((value / max_value) * 100)
        bar_length = 20
        filled = int((value / max_value) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Determine color based on value (or reverse for hunger)
        if reverse:
            # High values are bad (hunger)
            if value > 70:
                color = Fore.RED
                context = "(Very hungry!)"
            elif value > 50:
                color = Fore.YELLOW
                context = "(Getting hungry)"
            elif value > 30:
                color = Fore.GREEN
                context = "(Satisfied)"
            else:
                color = Fore.GREEN
                context = "(Full)"
        else:
            # High values are good (health, energy, happiness)
            if value < 30:
                color = Fore.RED
                context = "(Critical!)" if label == "Health" else "(Very low!)"
            elif value < 60:
                color = Fore.YELLOW
                context = "(Low)"
            elif value < 80:
                color = Fore.GREEN
                context = "(Good)"
            else:
                color = Fore.GREEN
                context = "(Excellent!)"

        # Format the line
        if self.use_color:
            return f"  {emoji} {label:10} {color}{bar}{Style.RESET_ALL} {percentage:3}%  {Style.DIM}{context}{Style.RESET_ALL}"
        else:
            return f"  {emoji} {label:10} {bar} {percentage:3}%  {context}"

    def print_detailed_stats(self, state, personality):
        """
        Print beautifully formatted stats display.

        Args:
            state: EeveeState object
            personality: Personality object
        """
        # Header
        separator = "╔" + "═" * 68 + "╗"
        title = "║" + "EEVEE'S STATUS".center(68) + "║"
        separator_bottom = "╚" + "═" * 68 + "╝"

        if self.use_color:
            print(f"\n{Fore.CYAN}{separator}")
            print(f"{Style.BRIGHT}{title}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{separator_bottom}{Style.RESET_ALL}\n")
        else:
            print(f"\n{separator}")
            print(title)
            print(f"{separator_bottom}\n")

        # Physical Health Section
        if self.use_color:
            print(f"{Fore.GREEN}{Style.BRIGHT}💚 PHYSICAL HEALTH{Style.RESET_ALL}")
        else:
            print("💚 PHYSICAL HEALTH")

        print(self.print_stat_bar("Health", state.health, emoji="❤️"))
        print(self.print_stat_bar("Energy", state.energy, emoji="⚡"))
        print(self.print_stat_bar("Happiness", state.happiness, emoji="😊"))
        print(self.print_stat_bar("Hunger", state.hunger, emoji="🍖", reverse=True))

        # Relationship Section
        print()
        if self.use_color:
            print(f"{Fore.MAGENTA}{Style.BRIGHT}🤝 RELATIONSHIP{Style.RESET_ALL}")
        else:
            print("🤝 RELATIONSHIP")

        trust_bar = int((state.trust / 100) * 20)
        bond_bar = int((state.bond / 100) * 20)

        if self.use_color:
            trust_color = Fore.GREEN if state.trust >= 50 else Fore.YELLOW
            bond_color = Fore.GREEN if state.bond >= 50 else Fore.YELLOW
            print(f"  Trust: {trust_color}{'█' * trust_bar}{'░' * (20 - trust_bar)}{Style.RESET_ALL} {state.trust}%  |  "
                  f"Bond: {bond_color}{'█' * bond_bar}{'░' * (20 - bond_bar)}{Style.RESET_ALL} {state.bond}%")
        else:
            print(f"  Trust: {'█' * trust_bar}{'░' * (20 - trust_bar)} {state.trust}%  |  "
                  f"Bond: {'█' * bond_bar}{'░' * (20 - bond_bar)} {state.bond}%")

        # Personality Section
        print()
        if self.use_color:
            print(f"{Fore.YELLOW}{Style.BRIGHT}🌟 PERSONALITY TRAITS{Style.RESET_ALL}")
        else:
            print("🌟 PERSONALITY TRAITS")

        traits = [
            f"Curious {personality.curiosity}/10",
            f"Brave {personality.bravery}/10",
            f"Playful {personality.playfulness}/10",
            f"Loyal {personality.loyalty}/10",
            f"Independent {personality.independence}/10"
        ]
        print("  " + " • ".join(traits))

        # Inventory Preview
        print()
        if self.use_color:
            print(f"{Fore.CYAN}{Style.BRIGHT}🎒 INVENTORY{Style.RESET_ALL}", end="")
        else:
            print("🎒 INVENTORY", end="")

        if state.inventory:
            print(f" ({len(state.inventory)} items)")
            # Show first 3 items as preview
            from world.items import ItemManager
            preview_items = []
            for item_id in state.inventory[:3]:
                item_def = ItemManager.get_item(item_id)
                if item_def:
                    preview_items.append(f"{item_def.emoji} {item_def.name}")
                else:
                    preview_items.append(item_id)

            print("  " + "  •  ".join(preview_items))

            if len(state.inventory) > 3:
                if self.use_color:
                    print(f"  {Style.DIM}...and {len(state.inventory) - 3} more{Style.RESET_ALL}")
                else:
                    print(f"  ...and {len(state.inventory) - 3} more")

            print(f"  {Style.DIM}💡 Type 'inventory' to see all items{Style.RESET_ALL}" if self.use_color else "  💡 Type 'inventory' to see all items")
        else:
            print(" (empty)")

        # Footer
        print()
        if self.use_color:
            print(f"{Style.DIM}📊 Total interactions with trainer: {state._state['total_interactions']}{Style.RESET_ALL}\n")
        else:
            print(f"📊 Total interactions with trainer: {state._state['total_interactions']}\n")

    def print_compact_inventory(self, inventory_items):
        """
        Print compact inventory view (default).

        Args:
            inventory_items: List of item IDs/objects
        """
        from world.items import ItemManager

        if not inventory_items:
            self.print_message("\n📦 Inventory is empty\n")
            return

        # Header
        if self.use_color:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}🎒 Inventory ({len(inventory_items)} items){Style.RESET_ALL}")
        else:
            print(f"\n🎒 Inventory ({len(inventory_items)} items)")

        print("━" * 70)

        # Group items and count quantities
        item_counts = {}
        for item_id in inventory_items:
            if item_id in item_counts:
                item_counts[item_id] += 1
            else:
                item_counts[item_id] = 1

        # Display items compactly
        display_items = []
        for item_id, count in item_counts.items():
            item_def = ItemManager.get_item(item_id)
            if item_def:
                qty_str = f" × {count}" if count > 1 else ""
                display_items.append(f"{item_def.emoji} {item_def.name}{qty_str}")
            else:
                qty_str = f" × {count}" if count > 1 else ""
                display_items.append(f"{item_id}{qty_str}")

        # Print in rows of 3
        for i in range(0, len(display_items), 3):
            row_items = display_items[i:i+3]
            # Pad each item to 22 characters for alignment
            formatted_row = [f"{item:22}" for item in row_items]
            print("  " + "  ".join(formatted_row))

        # Footer with tips
        print("━" * 70)
        if self.use_color:
            print(f"{Style.DIM}💡 'use <item>' to use  •  'drop <item>' to remove  •  'inventory detail' for descriptions{Style.RESET_ALL}\n")
        else:
            print("💡 'use <item>' to use  •  'drop <item>' to remove  •  'inventory detail' for descriptions\n")

    def print_detailed_inventory(self, inventory_items):
        """
        Print detailed inventory view with descriptions.

        Args:
            inventory_items: List of item IDs/objects
        """
        from world.items import ItemManager

        if not inventory_items:
            self.print_message("\n📦 Inventory is empty\n")
            return

        # Header
        if self.use_color:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}🎒 Inventory ({len(inventory_items)} items) - Detailed View{Style.RESET_ALL}")
        else:
            print(f"\n🎒 Inventory ({len(inventory_items)} items) - Detailed View")

        print("━" * 70)

        # Group by type
        items_by_type = {}
        for item_id in inventory_items:
            item_def = ItemManager.get_item(item_id)
            if item_def:
                item_type = item_def.item_type.value
                if item_type not in items_by_type:
                    items_by_type[item_type] = []
                items_by_type[item_type].append(item_def)
            else:
                # Unknown item
                if "unknown" not in items_by_type:
                    items_by_type["unknown"] = []
                items_by_type["unknown"].append(item_id)

        # Display by category
        for category, items in sorted(items_by_type.items()):
            print()
            if self.use_color:
                print(f"{Fore.YELLOW}{Style.BRIGHT}{category.upper()}{Style.RESET_ALL} ({len(items)})")
            else:
                print(f"{category.upper()} ({len(items)})")

            for item in items:
                if isinstance(item, str):
                    # Unknown item
                    self.print_message(f"  • {item}")
                else:
                    # Catalog item
                    consumable_str = "" if item.consumable else " (Keepsake)"
                    if self.use_color:
                        print(f"  {item.emoji} {Style.BRIGHT}{item.name}{Style.RESET_ALL}{consumable_str}")
                        print(f"     {Style.DIM}{item.description}{Style.RESET_ALL}")
                    else:
                        print(f"  {item.emoji} {item.name}{consumable_str}")
                        print(f"     {item.description}")

        # Footer
        print("\n" + "━" * 70)
        if self.use_color:
            print(f"{Style.DIM}💡 'use <item>' to use  •  'drop <item>' to remove  •  'inventory' for compact view{Style.RESET_ALL}\n")
        else:
            print("💡 'use <item>' to use  •  'drop <item>' to remove  •  'inventory' for compact view\n")

    def format_relative_time(self, timestamp_str: str) -> str:
        """
        Convert ISO timestamp to human-friendly relative time.

        Args:
            timestamp_str: ISO format timestamp

        Returns:
            Human-friendly string like "2 hours ago", "Yesterday", etc.
        """
        from datetime import datetime, timedelta

        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            now = datetime.now()
            delta = now - timestamp

            # Less than a minute
            if delta.total_seconds() < 60:
                return "Just now"

            # Less than an hour
            elif delta.total_seconds() < 3600:
                minutes = int(delta.total_seconds() / 60)
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

            # Less than 24 hours
            elif delta.total_seconds() < 86400:
                hours = int(delta.total_seconds() / 3600)
                return f"{hours} hour{'s' if hours != 1 else ''} ago"

            # Yesterday
            elif delta.days == 1:
                return f"Yesterday at {timestamp.strftime('%I:%M %p')}"

            # Less than a week
            elif delta.days < 7:
                return f"{delta.days} days ago"

            # Less than a month
            elif delta.days < 30:
                weeks = delta.days // 7
                return f"{weeks} week{'s' if weeks != 1 else ''} ago"

            # Less than a year
            elif delta.days < 365:
                months = delta.days // 30
                return f"{months} month{'s' if months != 1 else ''} ago"

            # Over a year
            else:
                years = delta.days // 365
                return f"{years} year{'s' if years != 1 else ''} ago"

        except Exception:
            return "Unknown time"

    def format_star_rating(self, relevance: float) -> str:
        """
        Convert relevance score to star rating.

        Args:
            relevance: Relevance score (typically 0.0-1.0+)

        Returns:
            Star rating string like "★★★★☆"
        """
        # Normalize to 0-5 scale (relevance scores can be > 1.0)
        normalized = min(5, max(0, relevance * 5))
        filled_stars = int(normalized)
        empty_stars = 5 - filled_stars

        return "★" * filled_stars + "☆" * empty_stars

    def print_formatted_memories(self, results):
        """
        Print memories with beautiful formatting grouped by type.

        Args:
            results: List of (content, metadata, similarity) tuples
        """
        if not results:
            self.print_warning("No memories found matching that query.")
            return

        # Group by memory type
        memories_by_type = {}
        for content, metadata, similarity in results:
            memory_type = metadata.get('memory_type', 'unknown')
            if memory_type not in memories_by_type:
                memories_by_type[memory_type] = []
            memories_by_type[memory_type].append((content, metadata, similarity))

        # Print header
        if self.use_color:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}🔍 Found {len(results)} memories:{Style.RESET_ALL}")
        else:
            print(f"\n🔍 Found {len(results)} memories:")

        print("━" * 70 + "\n")

        # Emoji mapping for memory types
        type_emojis = {
            'episodic': '📖',
            'semantic': '🧠',
            'emotional': '💙',
            'procedural': '⚙️'
        }

        # Print each type group
        type_order = ['episodic', 'semantic', 'emotional', 'procedural']
        for memory_type in type_order:
            if memory_type not in memories_by_type:
                continue

            memories = memories_by_type[memory_type]
            emoji = type_emojis.get(memory_type, '📝')

            # Type header
            if self.use_color:
                print(f"{Fore.YELLOW}{Style.BRIGHT}{emoji} {memory_type.upper()}{Style.RESET_ALL} (Events & Experiences)" if memory_type == 'episodic' else f"{Fore.YELLOW}{Style.BRIGHT}{emoji} {memory_type.upper()}{Style.RESET_ALL}")
            else:
                print(f"{emoji} {memory_type.upper()}")

            # Print memories of this type
            for i, (content, metadata, similarity) in enumerate(memories, 1):
                timestamp = metadata.get('timestamp', '')
                emotion = metadata.get('primary_emotion', '')
                location = metadata.get('location', '')

                # Memory content
                if self.use_color:
                    print(f"  {i}. {Style.BRIGHT}{content}{Style.RESET_ALL}")
                else:
                    print(f"  {i}. {content}")

                # Metadata line
                details = []

                # Time
                if timestamp:
                    time_str = self.format_relative_time(timestamp)
                    details.append(f"🕐 {time_str}")

                # Emotion emoji
                emotion_emojis = {
                    'joy': '😊',
                    'trust': '💚',
                    'fear': '😨',
                    'surprise': '😲',
                    'sadness': '😢',
                    'disgust': '😖',
                    'anger': '😠',
                    'anticipation': '🤔',
                    'curious': '😊',
                    'excited': '🤩',
                    'calm': '😌'
                }
                if emotion:
                    emotion_emoji = emotion_emojis.get(emotion.lower(), '💭')
                    details.append(f"{emotion_emoji} {emotion.capitalize()}")

                # Star rating
                stars = self.format_star_rating(similarity)
                details.append(f"{stars}")

                # Print metadata
                if self.use_color:
                    print(f"     {Style.DIM}{' • '.join(details)}{Style.RESET_ALL}\n")
                else:
                    print(f"     {' • '.join(details)}\n")

            print()  # Space between types
