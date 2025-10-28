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
