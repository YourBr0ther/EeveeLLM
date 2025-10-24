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

    def print_eevee_response(self, response: str):
        """Print Eevee's response"""
        if self.use_color:
            print(f"\n{Fore.MAGENTA}Eevee:{Style.RESET_ALL} {response}\n")
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
Available Commands:
  talk [message]        - Speak to Eevee
  observe               - See what Eevee is currently doing
  stats                 - View Eevee's current state
  world                 - See current location and surroundings
  pet                   - Pet Eevee
  play                  - Initiate playtime
  give [item]           - Give Eevee an item
  go [location]         - Travel to a connected location
  help                  - Show this help message
  exit / quit           - Save and quit

Debug Commands:
  debug on/off          - Toggle full debug mode
  debug brain           - Toggle brain council visualization
  debug state           - Show detailed state
        """
        print(help_text)

    def print_welcome(self):
        """Print welcome message"""
        welcome = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    Welcome to EeveeLLM                               ║
║                                                                      ║
║              Your Eevee companion is waiting for you!                ║
║                                                                      ║
║                    Type 'help' for commands                          ║
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
