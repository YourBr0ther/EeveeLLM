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

        # Accessibility settings
        self.simplified_output = Config.SIMPLIFIED_OUTPUT
        self.reduce_emojis = Config.REDUCE_EMOJIS
        self.high_contrast = Config.HIGH_CONTRAST

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

    def get_input(self, prompt: str = "> ", show_hint: bool = False) -> str:
        """
        Get user input with optional natural language hint

        Args:
            prompt: Input prompt to display
            show_hint: Whether to show natural language hint
        """
        try:
            # Enhanced prompt with natural language hint
            if show_hint:
                hint_prompt = f"{prompt} (Talk naturally or type a command) "
            else:
                hint_prompt = prompt

            if self.use_color:
                return input(f"{Fore.WHITE}{Style.BRIGHT}{hint_prompt}{Style.RESET_ALL}").strip()
            else:
                return input(hint_prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return "exit"

    def print_tip(self, tip: str, icon: str = "💡"):
        """Print a helpful tip message"""
        if self.use_color:
            print(f"\n{Fore.CYAN}{Style.DIM}{icon} Tip: {tip}{Style.RESET_ALL}")
        else:
            print(f"\n{icon} Tip: {tip}")

    def celebrate_natural_language(self):
        """Celebrate when user first uses natural language successfully"""
        if self.use_color:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 Hey! I understood that perfectly! 😊{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{Style.DIM}You can always talk to me naturally - no need for exact commands!{Style.RESET_ALL}\n")
        else:
            print(f"\n🎉 Hey! I understood that perfectly! 😊")
            print("You can always talk to me naturally - no need for exact commands!\n")

    def print_help(self, category: str = None):
        """
        Print help message - categorized for easier navigation.

        Args:
            category: Optional category to show (basic, world, items, memory, system, debug, all)
        """
        if not category or category == "all":
            # Show main help with category list
            help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                        EEVEE COMMAND HELP                            ║
╚══════════════════════════════════════════════════════════════════════╝

💡 TIP: Talk naturally! "How are you?" → stats (no table, just chat)
        Type exact command "stats" → shows full stats table + response

📚 HELP CATEGORIES (Type 'help <category>' for details):
   • basic    - Essential commands to get started
   • world    - Exploration and travel
   • items    - Inventory and item management
   • memory   - Memories and timeline (what Eevee remembers)
   • system   - Always-on mode, uptime, maintenance
   • debug    - Developer/testing commands
   • all      - Show everything

🎯 QUICK START:
   "Hello!"            - Greet Eevee
   "How are you?"      - Chat about Eevee's status (natural)
   stats               - Show full stats table
   "Let's play!"       - Play with Eevee
   "Where are we?"     - See current location
   "What do you have?" - Check inventory

✨ ALWAYS-ON MODE:
   EeveeLLM runs continuously - Eevee lives 24/7!
   • Background simulation every hour
   • Auto-save every 5 minutes
   • Check in anytime by typing

📖 For 80+ natural language examples, see: NATURAL_LANGUAGE_COMMANDS.md
            """
            print(help_text)

        elif category == "basic":
            help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                          BASIC COMMANDS                              ║
╚══════════════════════════════════════════════════════════════════════╝

📊 CHECK STATUS
  stats                 - View Eevee's health, energy, happiness, etc.
  💬 Natural: "How are you?" • "Are you okay?" • "Show me your stats"

👀 OBSERVE
  observe               - See what Eevee is currently doing
  💬 Natural: "What are you doing?" • "What's happening?"

🤝 INTERACT
  pet                   - Pet Eevee (increases happiness and trust)
  💬 Natural: "I want to pet you" • "Can I pet you?" • "Head pat"

  play                  - Initiate playtime (increases bond, costs energy)
  💬 Natural: "Let's play!" • "Want to play?" • "Feel like playing?"

  talk [message]        - Speak to Eevee (or just type naturally!)
  💬 Natural: "Hello Eevee!" • "You're so cute!" • "I love you"

💡 Type 'help' to see all categories
            """
            print(help_text)

        elif category == "world":
            help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                      WORLD & EXPLORATION                             ║
╚══════════════════════════════════════════════════════════════════════╝

🗺️  VIEW LOCATION
  world                 - See current location and surroundings
  💬 Natural: "Where are we?" • "Look around" • "Show me the area"

🚶 TRAVEL
  go [location]         - Travel to a connected location
  💬 Natural: "Let's go to the meadow" • "Take me to the forest"

📍 AVAILABLE LOCATIONS:
  • Trainer's Home      - Safe starting point
  • Sunny Garden        - Pleasant garden for playing
  • Wide Meadow         - Open area for running
  • Clear Stream        - Fresh water and berries
  • Forest Edge         - Border of the forest
  • Hidden Den          - Eevee's secret safe space
  • Sunny Hill          - Napping spot with sunset views
  • Deep Forest         - Dangerous but exciting woods

💡 Type 'help' to see all categories
            """
            print(help_text)

        elif category == "items":
            help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                      INVENTORY & ITEMS                               ║
╚══════════════════════════════════════════════════════════════════════╝

🎒 VIEW INVENTORY
  inventory             - View Eevee's inventory (compact)
  inventory detail      - View with full item descriptions
  💬 Natural: "What do you have?" • "Show me your stuff"

🎁 GIVE ITEMS
  give [item]           - Give Eevee an item
  💬 Natural: "Here's an Oran Berry" • "Take this Potion"

⚡ USE ITEMS
  use [item]            - Use an item from inventory
  💬 Natural: "Use the Oran Berry" • "Let's use a Potion"

🗑️  DROP ITEMS
  drop [item]           - Drop/remove an item (asks for confirmation on keepsakes)
  💬 Natural: "Drop the stick" • "Get rid of the trash"

🍊 ITEM TYPES:
  • Berries      - Restore hunger
  • Medicine     - Restore health
  • Toys         - Increase happiness
  • Treasures    - Rare keepsakes (can't be re-found!)

💡 Type 'help' to see all categories
            """
            print(help_text)

        elif category == "memory":
            help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                       MEMORY & TIMELINE                              ║
╚══════════════════════════════════════════════════════════════════════╝

🧠 SEARCH MEMORIES
  remember              - Show memory statistics
  remember [query]      - Search memories for specific topic
  💬 Natural: "Do you remember the park?" • "Show me your memories"

📖 MEMORY TYPES:
  • Episodic      - Events and experiences
  • Semantic      - Facts and knowledge (your name, preferences, etc.)
  • Emotional     - Feelings and associations
  • Procedural    - Learned behaviors

📅 VIEW TIMELINE
  timeline              - View summary of recent activities (compact)
  timeline detail       - View detailed day-by-day timeline
  💬 Natural: "What did you do?" • "What have you been up to?"

💡 Eevee remembers significant moments (6.0+/10 significance)
   Use "remember" keyword for important facts: "Remember, my name is Chris"

💡 Type 'help' to see all categories
            """
            print(help_text)

        elif category == "system":
            help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                       SYSTEM & ALWAYS-ON MODE                        ║
╚══════════════════════════════════════════════════════════════════════╝

✨ ALWAYS-ON MODE (Phase 7):
  EeveeLLM runs continuously - Eevee lives 24/7!
  • Background simulation every hour (Eevee explores, sleeps, plays)
  • Auto-save every 5 minutes (never lose progress)
  • Check in anytime by typing

📊 UPTIME & STATS
  uptime                - Show how long Eevee has been living
                         • Total uptime (days, hours, minutes)
                         • Background simulations run
                         • Auto-saves performed
                         • How long since last interaction
                         • What Eevee is currently doing

🔧 SHUTDOWN & MAINTENANCE
  maintenance           - Gracefully shut down EeveeLLM
  shutdown              - Same as maintenance

  ⚠️  This is the ONLY way to exit in always-on mode!
      Shows session stats and asks for confirmation.

  exit / quit           - Suggests using 'maintenance' instead

💡 USAGE EXAMPLE:
  > uptime
  📊 Always-On Stats:
     Uptime: 2 hours, 15 minutes
     Background simulations: 2
     Auto-saves: 27
     Idle for: 5 minutes
     Current activity: napping peacefully in the garden

  > maintenance
  ⚠️  Entering maintenance mode will shut down EeveeLLM...
  Are you sure? (y/n):

💡 Type 'help' to see all categories
            """
            print(help_text)

        elif category == "debug":
            help_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                          DEBUG COMMANDS                              ║
╚══════════════════════════════════════════════════════════════════════╝

🐛 DEBUGGING TOOLS
  debug on              - Enable full debug mode
  debug off             - Disable full debug mode

  debug brain           - Toggle brain council visualization
                         (Shows internal deliberation process)

  debug memory          - Toggle memory retrieval visualization
                         (Shows memory formation in real-time)

  debug state           - Show detailed internal state
                         (Full dump of Eevee's internal state)

  debug time [hours]    - Simulate time passage for testing
                         Example: 'debug time 48' simulates 2 days

⚠️  These commands are for developers and testing

💡 Type 'help system' for always-on mode & uptime commands
💡 Type 'help' to see all categories
            """
            print(help_text)

        else:
            # Unknown category
            self.print_warning(f"Unknown help category: '{category}'")
            print("\n📚 Available categories: basic, world, items, memory, system, debug, all")
            print("💡 Type 'help' to see the main help menu")

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
            print(f"{Fore.BLUE}{Style.DIM}{message}...{Style.RESET_ALL}", end='', flush=True)
        else:
            print(f"{message}...", end='', flush=True)

    def print_progress(self, message: str, icon: str = "⏳"):
        """
        Show progress with an animated icon

        Args:
            message: Progress message to display
            icon: Animated icon (defaults to hourglass)
        """
        if self.use_color:
            print(f"{Fore.CYAN}{Style.DIM}{icon} {message}...{Style.RESET_ALL}", end='', flush=True)
        else:
            print(f"{icon} {message}...", end='', flush=True)

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

    def toggle_accessibility_mode(self, enabled: bool = True):
        """
        Toggle accessibility mode for better screen reader compatibility

        Args:
            enabled: Whether to enable accessibility mode
        """
        self.simplified_output = enabled
        self.reduce_emojis = enabled
        if enabled:
            self.use_color = False  # Disable colors in accessibility mode

        # Update global config
        Config.SIMPLIFIED_OUTPUT = enabled
        Config.REDUCE_EMOJIS = enabled
        if enabled:
            Config.USE_COLOR = False

    def get_emoji(self, emoji: str, fallback: str = "") -> str:
        """
        Get emoji with accessibility fallback

        Args:
            emoji: The emoji to display
            fallback: Text fallback for accessibility mode

        Returns:
            Emoji or fallback text based on accessibility settings
        """
        if self.reduce_emojis:
            return fallback if fallback else ""
        return emoji

    def print_stat_bar(self, label: str, value: int, max_value: int = 100,
                       emoji: str = "", reverse: bool = False) -> None:
        """
        Print a visual stat bar with context indicator.

        Args:
            label: Stat name (e.g., "Health", "Hunger")
            value: Current value
            max_value: Maximum value (default 100)
            emoji: Emoji to show before label
            reverse: If True, high values are bad (e.g., hunger)
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

        # Format and print the line
        if self.use_color:
            line = f"  {emoji} {label:10} {color}{bar}{Style.RESET_ALL} {percentage:3}%  {Style.DIM}{context}{Style.RESET_ALL}"
        else:
            line = f"  {emoji} {label:10} {bar} {percentage:3}%  {context}"

        print(line)

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

        self.print_stat_bar("Health", state.health, emoji="❤️")
        self.print_stat_bar("Energy", state.energy, emoji="⚡")
        self.print_stat_bar("Happiness", state.happiness, emoji="😊")
        self.print_stat_bar("Hunger", state.hunger, emoji="🍖", reverse=True)

        # Relationship Section
        print()
        if self.use_color:
            print(f"{Fore.MAGENTA}{Style.BRIGHT}🤝 RELATIONSHIP{Style.RESET_ALL}")
        else:
            print("🤝 RELATIONSHIP")

        # Use consistent stat bar format for relationship stats
        self.print_stat_bar("Trust", state.trust, emoji="🤝")
        self.print_stat_bar("Bond", state.bond, emoji="💕")

        # Visual separator for better section hierarchy
        print()
        if self.use_color:
            print(f"{Fore.CYAN}{Style.DIM}{'─' * 68}{Style.RESET_ALL}")
        else:
            print('─' * 68)

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
            # Show first 3 items as preview with import safety
            try:
                from world.items import ItemManager
                preview_items = []
                for item_id in state.inventory[:3]:
                    # Validate item_id type
                    if not isinstance(item_id, str):
                        preview_items.append(f"[Invalid: {type(item_id).__name__}]")
                        continue

                    try:
                        item_def = ItemManager.get_item(item_id)
                        if item_def:
                            preview_items.append(f"{item_def.emoji} {item_def.name}")
                        else:
                            preview_items.append(item_id)
                    except Exception:
                        preview_items.append(f"{item_id} (error)")

                if preview_items:
                    print("  " + "  •  ".join(preview_items))
            except ImportError:
                # Fallback if ItemManager can't be imported
                preview_items = []
                for item_id in state.inventory[:3]:
                    if isinstance(item_id, str):
                        preview_items.append(item_id)
                    else:
                        preview_items.append(f"[{type(item_id).__name__}]")
                if preview_items:
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
        if not inventory_items:
            self.print_message("\n📦 Inventory is empty\n")
            return

        # Try importing ItemManager with fallback
        try:
            from world.items import ItemManager
            has_item_manager = True
        except ImportError:
            ItemManager = None
            has_item_manager = False

        # Enhanced header with better design
        if self.use_color:
            print(f"\n╔{'═' * 68}╗")
            print(f"║{f'🎒 INVENTORY ({len(inventory_items)} items)'.center(68)}║")
            print(f"╚{'═' * 68}╝")
        else:
            print(f"\n╔{'═' * 68}╗")
            print(f"║{f'🎒 INVENTORY ({len(inventory_items)} items)'.center(68)}║")
            print(f"╚{'═' * 68}╝")

        # Group items by type for better organization
        items_by_type = {}
        item_counts = {}
        invalid_items = []

        for item_id in inventory_items:
            # Check if item_id is hashable before using as dict key
            try:
                if item_id in item_counts:
                    item_counts[item_id] += 1
                else:
                    item_counts[item_id] = 1
            except TypeError:
                # Unhashable type (like dict, list) - add to invalid items
                invalid_items.append(item_id)

        # Categorize items for better display
        for item_id, count in item_counts.items():
            # Validate item_id type
            if not isinstance(item_id, str):
                continue

            if has_item_manager:
                try:
                    item_def = ItemManager.get_item(item_id)
                    if item_def:
                        try:
                            item_type = item_def.item_type.value if hasattr(item_def, 'item_type') else 'misc'
                        except AttributeError:
                            item_type = 'misc'

                        if item_type not in items_by_type:
                            items_by_type[item_type] = []

                        qty_str = f" × {count}" if count > 1 else ""
                        items_by_type[item_type].append(f"{item_def.emoji} {item_def.name}{qty_str}")
                    else:
                        # Unknown item
                        if 'misc' not in items_by_type:
                            items_by_type['misc'] = []
                        qty_str = f" × {count}" if count > 1 else ""
                        items_by_type['misc'].append(f"{item_id}{qty_str}")
                except Exception:
                    # Error getting item
                    if 'misc' not in items_by_type:
                        items_by_type['misc'] = []
                    qty_str = f" × {count}" if count > 1 else ""
                    items_by_type['misc'].append(f"{item_id} (error){qty_str}")
            else:
                # Fallback without ItemManager
                if 'items' not in items_by_type:
                    items_by_type['items'] = []
                qty_str = f" × {count}" if count > 1 else ""
                items_by_type['items'].append(f"{item_id}{qty_str}")

        # Display items by category for better organization
        category_emojis = {
            'food': '🍎',
            'medicine': '💊',
            'toy': '🎾',
            'treasure': '💎',
            'misc': '📦',
            'items': '📋'
        }

        for category, items in sorted(items_by_type.items()):
            emoji = category_emojis.get(category, '📦')

            print()
            if self.use_color:
                print(f"{Fore.YELLOW}{Style.BRIGHT}{emoji} {category.upper()}{Style.RESET_ALL}")
            else:
                print(f"{emoji} {category.upper()}")

            # Print items in rows of 3
            for i in range(0, len(items), 3):
                row_items = items[i:i+3]
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
        if not inventory_items:
            self.print_message("\n📦 Inventory is empty\n")
            return

        # Try importing ItemManager with fallback
        try:
            from world.items import ItemManager
            has_item_manager = True
        except ImportError:
            ItemManager = None
            has_item_manager = False

        # Header
        if self.use_color:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}🎒 Inventory ({len(inventory_items)} items) - Detailed View{Style.RESET_ALL}")
        else:
            print(f"\n🎒 Inventory ({len(inventory_items)} items) - Detailed View")

        print("━" * 70)

        # Group by type with safe ItemManager usage
        items_by_type = {}
        for item_id in inventory_items:
            # Validate item_id type
            if not isinstance(item_id, str):
                if "invalid" not in items_by_type:
                    items_by_type["invalid"] = []
                items_by_type["invalid"].append(f"[{type(item_id).__name__}]")
                continue

            if has_item_manager:
                try:
                    item_def = ItemManager.get_item(item_id)
                    if item_def:
                        try:
                            item_type = item_def.item_type.value
                        except AttributeError:
                            item_type = "unknown"
                        if item_type not in items_by_type:
                            items_by_type[item_type] = []
                        items_by_type[item_type].append(item_def)
                    else:
                        # Unknown item
                        if "unknown" not in items_by_type:
                            items_by_type["unknown"] = []
                        items_by_type["unknown"].append(item_id)
                except Exception:
                    # Error getting item
                    if "error" not in items_by_type:
                        items_by_type["error"] = []
                    items_by_type["error"].append(f"{item_id} (error)")
            else:
                # Fallback without ItemManager
                if "items" not in items_by_type:
                    items_by_type["items"] = []
                items_by_type["items"].append(item_id)

        # Display by category
        for category, items in sorted(items_by_type.items()):
            print()
            if self.use_color:
                print(f"{Fore.YELLOW}{Style.BRIGHT}{category.upper()}{Style.RESET_ALL} ({len(items)})")
            else:
                print(f"{category.upper()} ({len(items)})")

            for item in items:
                if isinstance(item, str):
                    # Unknown item or string item
                    self.print_message(f"  • {item}")
                else:
                    # Catalog item - safe access to attributes
                    try:
                        name = getattr(item, 'name', 'Unknown Item')
                        emoji = getattr(item, 'emoji', '•')
                        description = getattr(item, 'description', 'No description available')
                        consumable = getattr(item, 'consumable', True)

                        consumable_str = "" if consumable else " (Keepsake)"
                        if self.use_color:
                            print(f"  {emoji} {Style.BRIGHT}{name}{Style.RESET_ALL}{consumable_str}")
                            print(f"     {Style.DIM}{description}{Style.RESET_ALL}")
                        else:
                            print(f"  {emoji} {name}{consumable_str}")
                            print(f"     {description}")
                    except Exception as e:
                        self.print_message(f"  • Error displaying item: {e}")

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
        import logging

        # Validate input
        if timestamp_str is None:
            logging.warning("format_relative_time received None timestamp")
            return "Unknown time"

        if not isinstance(timestamp_str, str):
            logging.warning(f"format_relative_time expected string, got {type(timestamp_str)}")
            return "Unknown time"

        try:
            timestamp = datetime.fromisoformat(timestamp_str)
        except (ValueError, TypeError) as e:
            logging.warning(f"Invalid timestamp format '{timestamp_str}': {e}")
            return "Unknown time"

        try:
            now = datetime.now()
            delta = now - timestamp

            # Handle future timestamps
            if delta.total_seconds() < 0:
                return "In the future"

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

        except Exception as e:
            # This should never happen - if it does, we want to know!
            logging.error(f"Unexpected error in time calculation: {e}", exc_info=True)
            return "Unknown time"

    def format_star_rating(self, relevance: float) -> str:
        """
        Convert relevance score to star rating.

        Args:
            relevance: Relevance score (typically 0.0-1.0+)

        Returns:
            Star rating string like "★★★★☆"
        """
        import logging

        # Validate input
        if relevance is None:
            logging.warning("Star rating received None relevance")
            return "☆☆☆☆☆"  # All empty stars

        try:
            relevance = float(relevance)  # Convert if needed
        except (ValueError, TypeError) as e:
            logging.warning(f"Invalid relevance value '{relevance}': {e}")
            return "☆☆☆☆☆"

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
        for item in results:
            # Validate tuple structure
            if not isinstance(item, (tuple, list)) or len(item) != 3:
                continue

            content, metadata, similarity = item

            # Validate each component
            if content is None:
                continue

            if metadata is None:
                metadata = {}  # Use empty dict as fallback

            if similarity is None:
                similarity = 0.0  # Use 0.0 as fallback

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

    def print_timeline_summary(self, activities, hours_elapsed, net_changes, items_found):
        """
        Print compact timeline summary (default view).

        Shows key highlights without overwhelming detail.

        Args:
            activities: List of Activity objects
            hours_elapsed: Total hours that passed
            net_changes: Dict of state changes
            items_found: List of item IDs found
        """
        if not activities:
            self.print_info("No significant activities occurred while you were away.")
            return

        # Validate input types to prevent crashes
        if not isinstance(activities, list):
            self.print_error("Timeline data format error - invalid activities list")
            return

        if not isinstance(hours_elapsed, (int, float)) or hours_elapsed < 0:
            self.print_error("Timeline data format error - invalid time duration")
            return

        days = hours_elapsed / 24

        # Enhanced header with better visual hierarchy
        if self.use_color:
            print(f"\n╔{'═' * 68}╗")
            print(f"║{f'📅 TIMELINE: Last {hours_elapsed:.0f} hours ({days:.1f} days)'.center(68)}║")
            print(f"╚{'═' * 68}╝\n")
        else:
            print(f"\n╔{'═' * 68}╗")
            print(f"║{f'📅 TIMELINE: Last {hours_elapsed:.0f} hours ({days:.1f} days)'.center(68)}║")
            print(f"╚{'═' * 68}╝\n")

        # Count activities by type with defensive checks
        activity_counts = {}
        for activity in activities:
            # Validate activity object has required attributes
            if not hasattr(activity, 'type'):
                continue  # Skip malformed activities
            activity_type = getattr(activity, 'type', 'unknown')
            activity_counts[activity_type] = activity_counts.get(activity_type, 0) + 1

        # Activity type emojis
        type_emojis = {
            'needs': '🍖',
            'exploration': '🌍',
            'rest': '😴',
            'play': '🎮',
            'emotional': '💙',
            'social': '👋',
            'survival': '🛡️'
        }

        # Show summary with better visual organization
        if self.use_color:
            print(f"{Fore.YELLOW}{Style.BRIGHT}🎯 ACTIVITY SUMMARY{Style.RESET_ALL}")
        else:
            print("🎯 ACTIVITY SUMMARY")

        if self.use_color:
            print(f"{Style.DIM}While you were away, Eevee:{Style.RESET_ALL}")
        else:
            print("While you were away, Eevee:")

        for activity_type, count in sorted(activity_counts.items()):
            emoji = type_emojis.get(activity_type, '•')
            type_name = activity_type.replace('_', ' ').title()
            if self.use_color:
                print(f"  {emoji} {Style.DIM}{type_name}:{Style.RESET_ALL} {count} time{'s' if count != 1 else ''}")
            else:
                print(f"  {emoji} {type_name}: {count} time{'s' if count != 1 else ''}")

        # Visual separator
        print()
        if self.use_color:
            print(f"{Fore.CYAN}{Style.DIM}{'─' * 50}{Style.RESET_ALL}")
        else:
            print('─' * 50)

        # State changes
        print()
        if self.use_color:
            print(f"{Fore.YELLOW}{Style.BRIGHT}📊 STATE CHANGES{Style.RESET_ALL}")
        else:
            print("📊 STATE CHANGES")

        for stat, delta in net_changes.items():
            if delta == 0:
                continue

            # Color based on good/bad change
            if stat == 'hunger':
                # Hunger increase is bad
                color = Fore.RED if delta > 0 else Fore.GREEN
                sign = "+" if delta > 0 else ""
            else:
                # Other stats: increase is good
                color = Fore.GREEN if delta > 0 else Fore.RED
                sign = "+" if delta > 0 else ""

            if self.use_color:
                print(f"  {stat.capitalize():12} {color}{sign}{delta:3}{Style.RESET_ALL}")
            else:
                print(f"  {stat.capitalize():12} {sign}{delta:3}")

        # Items found
        if items_found:
            print()
            if self.use_color:
                print(f"{Fore.YELLOW}{Style.BRIGHT}🎁 Items Found:{Style.RESET_ALL}")
            else:
                print("🎁 Items Found:")

            try:
                from world.items import ItemManager
                item_counts = {}
                for item_id in items_found:
                    item_counts[item_id] = item_counts.get(item_id, 0) + 1

                for item_id, count in item_counts.items():
                    try:
                        item_def = ItemManager.get_item(item_id)
                        if item_def:
                            qty_str = f" × {count}" if count > 1 else ""
                            print(f"  {item_def.emoji} {item_def.name}{qty_str}")
                        else:
                            qty_str = f" × {count}" if count > 1 else ""
                            print(f"  {item_id}{qty_str}")
                    except Exception:
                        qty_str = f" × {count}" if count > 1 else ""
                        print(f"  {item_id}{qty_str}")
            except ImportError:
                # Fallback if ItemManager can't be imported
                for item_id in items_found:
                    print(f"  {item_id}")

        # Memorable moments (significant activities) with defensive checks
        try:
            significant_activities = [
                a for a in activities
                if hasattr(a, 'significance') and
                isinstance(getattr(a, 'significance', 0), (int, float)) and
                getattr(a, 'significance', 0) > 7.0
            ]
            if significant_activities:
                print()
                if self.use_color:
                    print(f"{Fore.YELLOW}{Style.BRIGHT}💭 Memorable Moments:{Style.RESET_ALL}")
                else:
                    print("💭 Memorable Moments:")

                # Show top 3 most significant with safe sorting
                try:
                    sorted_activities = sorted(
                        significant_activities,
                        key=lambda a: getattr(a, 'significance', 0),
                        reverse=True
                    )
                    for activity in sorted_activities[:3]:
                        description = getattr(activity, 'description', 'Unknown activity')
                        if self.use_color:
                            print(f"  • {Style.DIM}{description}{Style.RESET_ALL}")
                        else:
                            print(f"  • {description}")
                except Exception as e:
                    print(f"  • Error displaying memorable moments: {e}")
        except Exception as e:
            print(f"  • Error processing significant activities: {e}")

        # Footer
        print("\n" + "━" * 70)
        if self.use_color:
            print(f"{Style.DIM}💡 Type 'timeline detail' to see all activities{Style.RESET_ALL}\n")
        else:
            print("💡 Type 'timeline detail' to see all activities\n")

    def print_timeline_detail(self, activities, hours_elapsed):
        """
        Print detailed timeline with all activities.

        Args:
            activities: List of Activity objects
            hours_elapsed: Total hours that passed
        """
        if not activities:
            self.print_info("No significant activities occurred while you were away.")
            return

        # Validate input types to prevent crashes
        if not isinstance(activities, list):
            self.print_error("Timeline data format error - invalid activities list")
            return

        if not isinstance(hours_elapsed, (int, float)) or hours_elapsed < 0:
            self.print_error("Timeline data format error - invalid time duration")
            return

        days = hours_elapsed / 24

        # Header
        if self.use_color:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}📅 DETAILED TIMELINE: Last {hours_elapsed:.0f} hours ({days:.1f} days){Style.RESET_ALL}")
        else:
            print(f"\n📅 DETAILED TIMELINE: Last {hours_elapsed:.0f} hours ({days:.1f} days)")

        print("━" * 70 + "\n")

        # Group by day with defensive checks
        from datetime import datetime
        activities_by_day = {}
        for activity in activities:
            # Validate activity has timestamp attribute
            if not hasattr(activity, 'timestamp'):
                continue  # Skip activities without timestamp

            try:
                timestamp = getattr(activity, 'timestamp', None)
                if timestamp is None:
                    continue

                day_key = timestamp.strftime("%B %d, %Y")  # "October 28, 2025"
                if day_key not in activities_by_day:
                    activities_by_day[day_key] = []
                activities_by_day[day_key].append(activity)
            except (AttributeError, ValueError) as e:
                continue  # Skip activities with invalid timestamps

        # Print each day
        for day_key in sorted(activities_by_day.keys()):
            if self.use_color:
                print(f"{Fore.YELLOW}{Style.BRIGHT}{day_key}{Style.RESET_ALL}")
            else:
                print(day_key)

            day_activities = activities_by_day[day_key]

            # Sort activities with defensive key function
            try:
                sorted_activities = sorted(
                    day_activities,
                    key=lambda a: getattr(a, 'timestamp', datetime.min)
                )
            except Exception:
                sorted_activities = day_activities  # Use unsorted if sorting fails

            for activity in sorted_activities:
                try:
                    timestamp = getattr(activity, 'timestamp', None)
                    if timestamp is None:
                        time_str = "Unknown time"
                    else:
                        time_str = timestamp.strftime("%I:%M %p")

                    # Safely get significance
                    significance = getattr(activity, 'significance', 0)
                    if isinstance(significance, (int, float)) and significance > 7.0:
                        significant_marker = "⭐ "
                    else:
                        significant_marker = "   "

                    # Safely get description
                    description = getattr(activity, 'description', 'Unknown activity')

                    if self.use_color:
                        print(f"  {significant_marker}{Style.DIM}{time_str}{Style.RESET_ALL} - {description}")
                    else:
                        print(f"  {significant_marker}{time_str} - {description}")

                    # Show state changes if any with defensive checks
                    if hasattr(activity, 'state_changes') and activity.state_changes:
                        try:
                            changes = []
                            for stat, delta in activity.state_changes.items():
                                if delta != 0:
                                    sign = "+" if delta > 0 else ""
                                    changes.append(f"{stat} {sign}{delta}")

                            if changes:
                                if self.use_color:
                                    print(f"           {Style.DIM}({', '.join(changes)}){Style.RESET_ALL}")
                                else:
                                    print(f"           ({', '.join(changes)})")
                        except Exception:
                            pass  # Skip state changes display if it fails

                except Exception as e:
                    # If any activity processing fails, show a safe fallback
                    print(f"  • Error displaying activity: {e}")

            print()  # Space between days

        # Footer
        print("━" * 70)
        if self.use_color:
            print(f"{Style.DIM}💡 Type 'timeline' for summary view{Style.RESET_ALL}\n")
        else:
            print("💡 Type 'timeline' for summary view\n")
