#!/usr/bin/env python3
"""
EeveeLLM - Main Entry Point
Your Eevee companion awaits!
"""
import logging
import sys
from typing import Optional

from config import Config
from eevee.state import EeveeState
from eevee.personality import Personality
from eevee.responses import ResponseGenerator
from world.locations import WorldMap
from llm.nanogpt_client import NanoGPTClient
from llm.prompts import PromptBuilder
from ui import TerminalUI

# Set up logging
logging.basicConfig(
    level=logging.INFO if Config.VERBOSE_LOGGING else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EeveeLLM:
    """Main application controller"""

    def __init__(self):
        self.ui = TerminalUI()
        self.eevee_state = EeveeState()
        self.personality = Personality()
        self.world = WorldMap()
        self.llm_client = NanoGPTClient()
        self.response_gen = ResponseGenerator(self.llm_client)
        self.debug_mode = Config.DEBUG_MODE
        self.running = True

    def start(self):
        """Start the application"""
        self.ui.clear_screen()
        self.ui.print_welcome()

        # Show greeting based on time since last interaction
        time_since = self.eevee_state.get_time_since_last_interaction()
        self._show_scene()

        # Generate greeting
        context = self._build_context()
        greeting = self.response_gen.generate_greeting(time_since, context)
        self.ui.print_eevee_response(greeting)

        # Main loop
        self.main_loop()

    def main_loop(self):
        """Main interaction loop"""
        while self.running:
            try:
                user_input = self.ui.get_input()

                if not user_input:
                    continue

                # Process command
                self.process_command(user_input)

            except KeyboardInterrupt:
                print()
                self.ui.print_system_message("Use 'exit' to quit")
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                self.ui.print_error(f"Something went wrong: {e}")

        # Save and exit
        self.shutdown()

    def process_command(self, user_input: str):
        """Process user command"""
        parts = user_input.lower().split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        # Commands
        if command in ["exit", "quit", "q"]:
            self.running = False

        elif command == "help":
            self.ui.print_help()

        elif command == "stats":
            self.show_stats()

        elif command == "world":
            self.show_world()

        elif command == "observe":
            self.observe_eevee()

        elif command == "pet":
            self.pet_eevee()

        elif command == "play":
            self.play_with_eevee()

        elif command == "give":
            if args:
                self.give_item(args)
            else:
                self.ui.print_message("Give what? (e.g., 'give Oran Berry')")

        elif command == "go":
            if args:
                self.travel_to(args)
            else:
                self.ui.print_message("Go where? (e.g., 'go meadow')")

        elif command == "talk":
            if args:
                self.talk_to_eevee(args)
            else:
                self.ui.print_message("What do you want to say?")

        elif command == "debug":
            self.handle_debug_command(args)

        else:
            # Treat unrecognized input as talking to Eevee
            self.talk_to_eevee(user_input)

    def talk_to_eevee(self, message: str):
        """Talk to Eevee"""
        self.ui.print_user_input(message)

        if Config.SHOW_BRAIN_COUNCIL or self.debug_mode:
            self.ui.print_system_message("Brain Council Deliberating...")

        # Generate response
        context = self._build_context()
        response, council_decision = self.response_gen.generate_response(
            message, context, debug=self.debug_mode, world_map=self.world
        )

        # Show brain council debate if enabled
        if council_decision and (Config.SHOW_BRAIN_COUNCIL or self.debug_mode):
            debate_vis = self.response_gen.brain_council.get_debate_visualization(council_decision)
            print("\n" + debate_vis + "\n")

        self.ui.print_eevee_response(response)

        # Update state
        self._update_after_interaction("talk", message, response)

    def pet_eevee(self):
        """Pet Eevee"""
        self.ui.print_user_input("*pets Eevee gently*")

        context = self._build_context()
        response, _ = self.response_gen.generate_response(
            "The trainer pets me gently",
            context,
            debug=self.debug_mode,
            world_map=self.world
        )

        self.ui.print_eevee_response(response)

        # Increase happiness and trust
        self.eevee_state.update_physical_state(
            happiness=min(100, self.eevee_state.happiness + 5)
        )
        self.eevee_state.update_relationship(trust_delta=1)

        self._update_after_interaction("pet", "pet", response)

    def play_with_eevee(self):
        """Play with Eevee"""
        self.ui.print_user_input("*initiates playtime*")

        context = self._build_context()
        response = self.response_gen.describe_action("playing", context)

        self.ui.print_eevee_response(response)

        # Update state based on energy
        if self.eevee_state.energy > 30:
            self.eevee_state.update_physical_state(
                happiness=min(100, self.eevee_state.happiness + 10),
                energy=max(0, self.eevee_state.energy - 10),
                hunger=min(100, self.eevee_state.hunger + 5)
            )
            self.eevee_state.update_relationship(bond_delta=2)
        else:
            self.ui.print_system_message("Eevee seems too tired to play much...")

        self._update_after_interaction("play", "play", response)

    def give_item(self, item: str):
        """Give item to Eevee"""
        self.ui.print_user_input(f"*offers {item}*")

        # Simple item handling
        if "berry" in item.lower() or "food" in item.lower():
            context = self._build_context()
            response, _ = self.response_gen.generate_response(
                f"The trainer offers me {item}",
                context,
                debug=self.debug_mode,
                world_map=self.world
            )
            self.ui.print_eevee_response(response)

            # Reduce hunger, increase happiness
            self.eevee_state.update_physical_state(
                hunger=max(0, self.eevee_state.hunger - 20),
                happiness=min(100, self.eevee_state.happiness + 5)
            )
            self.eevee_state.add_item(item)

        else:
            self.ui.print_eevee_response(f"*Eevee sniffs {item} curiously* Vee?")
            self.eevee_state.add_item(item)

        self._update_after_interaction("give", f"give {item}", f"received {item}")

    def travel_to(self, destination: str):
        """Travel to a location"""
        current_loc = self.world.get_location(self.eevee_state.location)
        target_loc = self.world.get_location_by_name(destination)

        if not target_loc:
            # Try by ID
            target_loc = self.world.get_location(destination)

        if not target_loc:
            self.ui.print_message(f"Unknown location: {destination}")
            return

        if not self.world.can_travel(current_loc.id, target_loc.id):
            self.ui.print_message(f"You can't go directly to {target_loc.name} from here.")
            return

        # Travel
        self.ui.print_system_message(f"Traveling to {target_loc.name}...")
        self.eevee_state._state['current_location'] = target_loc.id

        # Show new location
        self._show_scene()

        # Eevee reacts
        context = self._build_context()
        response, _ = self.response_gen.generate_response(
            f"We arrived at {target_loc.name}",
            context,
            debug=self.debug_mode,
            world_map=self.world
        )
        self.ui.print_eevee_response(response)

        self._update_after_interaction("travel", f"go {target_loc.name}", response)

    def observe_eevee(self):
        """Observe what Eevee is doing"""
        context = self._build_context()
        mood = self.response_gen.interpret_mood(context)
        self.ui.print_message(mood)

        # Show what Eevee is doing based on state
        state = self.eevee_state
        if state.energy < 30:
            action = self.response_gen.describe_action("resting", context)
        elif state.hunger > 70:
            action = "*Eevee sniffs around* Vee... *looking for food*"
        elif state.happiness > 80:
            action = self.response_gen.describe_action("playing", context)
        else:
            action = "*Eevee sits calmly, observing the surroundings* Vee~"

        self.ui.print_eevee_response(action)

    def show_stats(self):
        """Show detailed stats"""
        state = self.eevee_state
        personality = self.personality

        print("\n" + "=" * 60)
        print("EEVEE STATUS")
        print("=" * 60)
        print(f"\nPhysical State:")
        print(f"  Hunger:    {state.hunger}/100")
        print(f"  Energy:    {state.energy}/100")
        print(f"  Health:    {state.health}/100")
        print(f"  Happiness: {state.happiness}/100")

        print(f"\nRelationship:")
        print(f"  Trust:     {state.trust}/100")
        print(f"  Bond:      {state.bond}/100")

        print(f"\nPersonality:")
        print(f"  Curiosity:     {personality.curiosity}/10")
        print(f"  Bravery:       {personality.bravery}/10")
        print(f"  Playfulness:   {personality.playfulness}/10")
        print(f"  Loyalty:       {personality.loyalty}/10")
        print(f"  Independence:  {personality.independence}/10")

        print(f"\nInventory:")
        if state.inventory:
            for item in state.inventory:
                print(f"  - {item}")
        else:
            print("  (empty)")

        print(f"\nInteractions: {state._state['total_interactions']}")
        print("=" * 60 + "\n")

    def show_world(self):
        """Show world/location info"""
        location = self.world.get_location(self.eevee_state.location)
        if location:
            description = self.world.describe_location(location.id)
            self.ui.print_location_description(description)

    def handle_debug_command(self, args: str):
        """Handle debug commands"""
        if args == "on":
            self.debug_mode = True
            Config.DEBUG_MODE = True
            Config.SHOW_BRAIN_COUNCIL = True
            self.ui.print_system_message("Debug mode enabled (includes brain council)")
        elif args == "off":
            self.debug_mode = False
            Config.DEBUG_MODE = False
            Config.SHOW_BRAIN_COUNCIL = False
            self.ui.print_system_message("Debug mode disabled")
        elif args == "brain":
            Config.SHOW_BRAIN_COUNCIL = not Config.SHOW_BRAIN_COUNCIL
            status = "enabled" if Config.SHOW_BRAIN_COUNCIL else "disabled"
            self.ui.print_system_message(f"Brain council visualization {status}")
        elif args == "state":
            self.show_stats()
        else:
            self.ui.print_message("Debug commands: on, off, brain, state")

    def _show_scene(self):
        """Show current scene"""
        location = self.world.get_location(self.eevee_state.location)
        if not location:
            return

        self.ui.print_header(
            location.name,
            self.eevee_state.time_of_day,
            self.eevee_state.weather
        )

        if Config.SHOW_STATS_BAR:
            self.ui.print_stats_bar(
                self.eevee_state.hunger,
                self.eevee_state.energy,
                self.eevee_state.happiness,
                self.eevee_state.health
            )

        self.ui.print_location_description(location.description)

    def _build_context(self):
        """Build context dictionary"""
        return PromptBuilder.build_context_dict(
            self.eevee_state,
            self.personality
        )

    def _update_after_interaction(self, interaction_type: str,
                                  user_input: str, eevee_response: str):
        """Update state after interaction"""
        # Log interaction
        context = self._build_context()
        mood = self.response_gen.interpret_mood(context)

        self.eevee_state.log_interaction(
            interaction_type,
            user_input,
            eevee_response,
            mood,
            significance=5.0
        )

        # Natural state decay
        self.eevee_state.update_physical_state(
            hunger=min(100, self.eevee_state.hunger + 1),
            energy=max(0, self.eevee_state.energy - 1)
        )

        # Save state
        self.eevee_state.save()
        self.personality.save()

    def shutdown(self):
        """Save and shutdown"""
        self.ui.print_goodbye()
        self.eevee_state.save()
        self.personality.save()
        logger.info("Application shutdown complete")


def main():
    """Main entry point"""
    try:
        app = EeveeLLM()
        app.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
