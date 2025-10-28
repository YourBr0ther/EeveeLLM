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

# Phase 3: Memory system
from memory import VectorMemoryStore, MemoryRetriever, MemoryConsolidator

# Phase 4: Time passage system
from world.activities import ActivityGenerator
from world.time_simulation import TimeSimulator

# Natural language processing
from nlp.intent_parser import IntentParser

# Set up logging
logging.basicConfig(
    level=logging.INFO if Config.VERBOSE_LOGGING else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EeveeLLM:
    """Main application controller"""

    def __init__(self):
        """Initialize EeveeLLM application with comprehensive error handling"""
        try:
            self.ui = TerminalUI()
        except Exception as e:
            print(f"Fatal: Failed to initialize UI: {e}")
            raise

        try:
            self.eevee_state = EeveeState()
        except Exception as e:
            print(f"Fatal: Failed to initialize Eevee state (database error?): {e}")
            raise

        try:
            self.personality = Personality()
        except Exception as e:
            logger.error(f"Failed to load personality, using defaults: {e}")
            self.personality = None

        try:
            self.world = WorldMap()
        except Exception as e:
            logger.error(f"Failed to load world map: {e}")
            raise

        try:
            self.llm_client = NanoGPTClient()
            self.response_gen = ResponseGenerator(self.llm_client)
        except Exception as e:
            logger.warning(f"LLM client initialization failed (will use fallback mode): {e}")
            self.llm_client = None
            self.response_gen = ResponseGenerator(None)

        self.debug_mode = Config.DEBUG_MODE
        self.running = True
        self.last_timeline = None  # Phase 4: Store last timeline for replay

        # Phase 3: Initialize memory system
        try:
            self.vector_store = VectorMemoryStore()
            self.memory_retriever = MemoryRetriever(
                vector_store=self.vector_store,
                config=Config.__dict__
            )
            self.memory_consolidator = MemoryConsolidator(
                vector_store=self.vector_store,
                config=Config.__dict__
            )

            # Integrate memory retriever with Hippocampus
            if self.response_gen.brain_council:
                for region in self.response_gen.brain_council.regions:
                    if region.name == "Hippocampus":
                        region.memory_retriever = self.memory_retriever
                        logger.info("Memory system integrated with Hippocampus")
                        break

            logger.info("Phase 3 memory system initialized successfully")
        except Exception as e:
            logger.warning(f"Memory system initialization failed (will use fallback): {e}")
            self.vector_store = None
            self.memory_retriever = None
            self.memory_consolidator = None

        # Phase 4: Initialize time passage system
        try:
            # Build personality traits dict using to_dict() method
            personality_traits = self.personality.to_dict()

            self.activity_generator = ActivityGenerator(
                personality=personality_traits,
                world_map=self.world
            )
            self.time_simulator = TimeSimulator(
                activity_generator=self.activity_generator,
                memory_consolidator=self.memory_consolidator,
                config=Config.__dict__
            )
            logger.info("Phase 4 time simulation system initialized successfully")
        except Exception as e:
            logger.warning(f"Time simulation initialization failed: {e}")
            self.activity_generator = None
            self.time_simulator = None

        # Initialize natural language intent parser
        try:
            self.intent_parser = IntentParser()
            logger.info("Natural language intent parser initialized")
        except Exception as e:
            logger.warning(f"Intent parser initialization failed: {e}")
            self.intent_parser = None

    def start(self):
        """Start the application"""
        self.ui.clear_screen()
        self.ui.print_welcome()

        # Phase 4: Handle time passage if user was away
        time_since = self.eevee_state.get_time_since_last_interaction()
        timeline_summary = None

        if time_since >= 2.0 and self.time_simulator:
            # Simulate autonomous activities
            try:
                logger.info(f"Running time simulation for {time_since:.1f} hours")

                # Inform user if simulation will be capped
                max_sim_hours = 168  # 7 days (matches time_simulation.py)
                if time_since > max_sim_hours:
                    self.ui.print_system_message(
                        f"Note: You were away for {time_since:.1f} hours ({time_since/24:.1f} days). "
                        f"Simulating the last {max_sim_hours} hours ({max_sim_hours/24:.0f} days) for performance."
                    )

                # Get current state before simulation
                state_dict = {
                    'hunger': self.eevee_state.hunger,
                    'energy': self.eevee_state.energy,
                    'happiness': self.eevee_state.happiness,
                    'health': self.eevee_state.health,
                    'hours_since_trainer': time_since
                }

                # Run simulation (Phase 5: Now returns items_found)
                activities, net_changes, memories, items_found = self.time_simulator.simulate_time_passage(
                    state=state_dict,
                    hours_elapsed=time_since,
                    last_location=self.eevee_state.location
                )

                # Apply net state changes
                self.eevee_state.update_physical_state(
                    hunger=max(0, min(100, self.eevee_state.hunger + net_changes['hunger'])),
                    energy=max(0, min(100, self.eevee_state.energy + net_changes['energy'])),
                    happiness=max(0, min(100, self.eevee_state.happiness + net_changes['happiness'])),
                    health=max(0, min(100, self.eevee_state.health + net_changes['health']))
                )

                # Phase 5: Add found items to inventory
                for item_id in items_found:
                    self.eevee_state.add_item(item_id)

                # Store timeline data for 'timeline' command (both summary and detail)
                self.last_timeline_data = {
                    'activities': activities,
                    'hours_elapsed': time_since,
                    'net_changes': net_changes,
                    'items_found': items_found
                }

                logger.info(f"Time simulation complete: {len(activities)} activities, {len(memories)} memories")

            except Exception as e:
                logger.error(f"Error during time simulation: {e}", exc_info=True)
                timeline_summary = None

        # Show current scene
        self._show_scene()

        # Generate greeting (with timeline if available)
        context = self._build_context()
        greeting = self.response_gen.generate_greeting(time_since, context, timeline_summary)
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
        """Process user command (with natural language support)"""

        # Try to parse natural language intent first
        intent = None
        if self.intent_parser:
            intent = self.intent_parser.parse(user_input)

        # If intent detected, use it; otherwise fall back to exact command parsing
        if intent:
            command = intent.command
            args = intent.args
            if Config.VERBOSE_LOGGING:
                logger.info(f"Natural language detected: '{user_input}' → {command} {args}")
        else:
            # Fall back to exact command parsing
            parts = user_input.lower().split(maxsplit=1)
            command = parts[0]
            args = parts[1] if len(parts) > 1 else ""

        # Commands
        if command in ["exit", "quit", "q"]:
            self.running = False

        elif command == "help":
            # Categorized help system
            self.ui.print_help(category=args if args else None)

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
                self.ui.print_info("Give what item?\n💡 Try: 'give Oran Berry' or just say 'Here's a berry'")

        elif command == "use":
            # Phase 5: Use item command
            if args:
                self.use_item(args)
            else:
                self.ui.print_info("Use what item?\n💡 Try: 'use Oran Berry' or 'inventory' to see what you have")

        elif command == "inventory":
            # Phase 5: View inventory (compact by default, detailed if args)
            detailed = args and "detail" in args.lower()
            self.show_inventory(detailed=detailed)

        elif command in ["drop", "remove"]:
            # Phase 5: Drop/remove item from inventory
            if args:
                self.drop_item(args)
            else:
                self.ui.print_info("Drop what item?\n💡 Try: 'drop Oran Berry' or 'inventory' to see what you have")

        elif command == "go":
            if args:
                self.travel_to(args)
            else:
                self.ui.print_info("Go where?\n💡 Try: 'go meadow' or 'world' to see available locations")

        elif command == "talk":
            if args:
                self.talk_to_eevee(args)
            else:
                self.ui.print_info("What do you want to say?\n💡 Just type naturally! You don't need the 'talk' command")

        elif command == "debug":
            self.handle_debug_command(args)

        elif command == "remember":
            # Phase 3: Memory browser command
            self.browse_memories(args)

        elif command == "timeline":
            # Phase 4: Timeline viewer command (summary by default, detailed if args)
            detailed = args and "detail" in args.lower()
            self.show_timeline(detailed=detailed)

        else:
            # Treat unrecognized input as talking to Eevee
            self.talk_to_eevee(user_input)

    def talk_to_eevee(self, message: str):
        """Talk to Eevee"""
        self.ui.print_user_input(message)

        # Show loading indicator
        if not (Config.SHOW_BRAIN_COUNCIL or self.debug_mode):
            self.ui.print_thinking("🧠 Thinking...")

        if Config.SHOW_BRAIN_COUNCIL or self.debug_mode:
            self.ui.print_system_message("Brain Council Deliberating...")

        # Generate response
        context = self._build_context()
        response, council_decision = self.response_gen.generate_response(
            message, context, debug=self.debug_mode, world_map=self.world
        )

        # Clear loading indicator
        if not (Config.SHOW_BRAIN_COUNCIL or self.debug_mode):
            self.ui.clear_thinking()

        # Show brain council debate if enabled
        if council_decision and (Config.SHOW_BRAIN_COUNCIL or self.debug_mode):
            debate_vis = self.response_gen.brain_council.get_debate_visualization(council_decision)
            print("\n" + debate_vis + "\n")

        self.ui.print_eevee_response(response)

        # Update state
        self._update_after_interaction("talk", message, response)

        # Phase 3: Form memories from this interaction
        self._form_memory(
            user_input=message,
            eevee_response=response,
            context=context,
            council_decision=council_decision
        )

    def pet_eevee(self):
        """Pet Eevee"""
        try:
            self.ui.print_user_input("*pets Eevee gently*")

            # Show loading indicator
            self.ui.print_thinking("💭 Responding...")

            context = self._build_context()
            response, _ = self.response_gen.generate_response(
                "The trainer pets me gently",
                context,
                debug=self.debug_mode,
                world_map=self.world
            )

            # Clear loading indicator
            self.ui.clear_thinking()

            self.ui.print_eevee_response(response)

            # Increase happiness and trust
            self.eevee_state.update_physical_state(
                happiness=min(100, self.eevee_state.happiness + 5)
            )
            self.eevee_state.update_relationship(trust_delta=1)

            self._update_after_interaction("pet", "pet", response)

        except Exception as e:
            logger.error(f"Error petting Eevee: {e}", exc_info=True)
            self.ui.print_error(f"Something went wrong: {e}")

    def play_with_eevee(self):
        """Play with Eevee"""
        try:
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

        except Exception as e:
            logger.error(f"Error playing with Eevee: {e}", exc_info=True)
            self.ui.print_error(f"Something went wrong: {e}")

    def give_item(self, item: str):
        """Give item to Eevee (Phase 5: Enhanced with item catalog)"""
        try:
            from world.items import ItemManager

            self.ui.print_user_input(f"*offers {item}*")

            # Check if this is a catalog item
            item_def = ItemManager.get_item(item)
            if not item_def:
                item_def = ItemManager.get_item_by_name(item)

            if item_def:
                # Known catalog item
                self.ui.print_eevee_response(
                    f"*Eevee's eyes light up* Vee! *happily accepts the {item_def.name}* {item_def.emoji}"
                )
                self.eevee_state.add_item(item_def.id)
                self.eevee_state.update_physical_state(
                    happiness=min(100, self.eevee_state.happiness + 5)
                )
            else:
                # Unknown item - add anyway
                self.ui.print_eevee_response(f"*Eevee sniffs {item} curiously* Vee?")
                self.eevee_state.add_item(item)

        except Exception as e:
            logger.error(f"Error giving item: {e}", exc_info=True)
            self.ui.print_error(f"Failed to give item: {e}")

    def use_item(self, item: str):
        """Use an item from inventory (Phase 5)"""
        try:
            self.ui.print_user_input(f"*uses {item}*")

            success, new_state, message = self.eevee_state.use_item(item)

            if success:
                self.ui.print_success(message)

                # Show state changes
                if new_state:
                    changes = []
                    old_state = {
                        'hunger': new_state['hunger'],
                        'energy': new_state['energy'],
                        'happiness': new_state['happiness'],
                        'health': new_state['health']
                    }
                    # Note: State already applied, just show message

                # Update after interaction
                self._update_after_interaction("use_item", item, message)
            else:
                # Item not found or can't be used
                self.ui.print_warning(message)
                self.ui.print_info("💡 Type 'inventory' to see what you have")

        except Exception as e:
            logger.error(f"Error using item: {e}", exc_info=True)
            self.ui.print_error(f"Failed to use item: {e}")

    def show_inventory(self, detailed: bool = False):
        """
        Show Eevee's inventory.

        Args:
            detailed: If True, show detailed view with descriptions
        """
        try:
            inventory = self.eevee_state.inventory

            # Use compact or detailed view
            if detailed:
                self.ui.print_detailed_inventory(inventory)
            else:
                self.ui.print_compact_inventory(inventory)

            # Eevee reacts to showing inventory (only if inventory not empty)
            if inventory:
                try:
                    self.ui.print_thinking("💭 Responding...")

                    context = self._build_context()
                    item_count = len(inventory)
                    response, _ = self.response_gen.generate_response(
                        f"The trainer is looking at my {item_count} item{'s' if item_count != 1 else ''}",
                        context,
                        debug=self.debug_mode,
                        world_map=self.world
                    )

                    self.ui.clear_thinking()
                    self.ui.print_eevee_response(response)

                    self._update_after_interaction("inventory", "check inventory", response)
                except Exception as e:
                    logger.error(f"Error generating inventory response: {e}")

        except Exception as e:
            logger.error(f"Error showing inventory: {e}", exc_info=True)
            self.ui.print_error(f"Failed to show inventory: {e}")

    def drop_item(self, item: str):
        """Drop/remove an item from inventory (Phase 5)"""
        try:
            from world.items import ItemManager

            # Check if item is in inventory (by ID or as unknown item)
            if not self.eevee_state.has_item(item):
                # Try to find by name
                item_def = ItemManager.get_item_by_name(item)
                if item_def and self.eevee_state.has_item(item_def.id):
                    item = item_def.id
                else:
                    self.ui.print_warning(f"You don't have '{item}' in your inventory.")
                    self.ui.print_info("💡 Type 'inventory' to see what you have")
                    return

            # Get item definition for display (if it exists)
            item_def = ItemManager.get_item(item)
            if not item_def:
                item_def = ItemManager.get_item_by_name(item)

            # Check if item is valuable (keepsake/treasure) and ask for confirmation
            if item_def and not item_def.consumable:
                self.ui.print_warning(
                    f"'{item_def.name}' {item_def.emoji} is a keepsake and cannot be recovered once dropped."
                )
                if not self.ui.confirm("Are you sure you want to drop it?", default=False):
                    self.ui.print_info(f"Kept the {item_def.name}.")
                    return

            # Remove the item
            success = self.eevee_state.remove_item(item)

            if success:
                if item_def:
                    self.ui.print_user_input(f"*drops {item_def.name}*")
                    self.ui.print_success(f"Dropped {item_def.emoji} {item_def.name}")
                else:
                    self.ui.print_user_input(f"*drops {item}*")
                    self.ui.print_success(f"Dropped {item}")

                logger.info(f"Dropped item: {item}")
            else:
                self.ui.print_error(f"Failed to drop '{item}'")

        except Exception as e:
            logger.error(f"Error dropping item: {e}", exc_info=True)
            self.ui.print_error(f"Failed to drop item: {e}")

    def travel_to(self, destination: str):
        """Travel to a location"""
        try:
            current_loc = self.world.get_location(self.eevee_state.location)
            target_loc = self.world.get_location_by_name(destination)

            if not target_loc:
                # Try by ID
                target_loc = self.world.get_location(destination)

            if not target_loc:
                self.ui.print_message(f"Unknown location: {destination}")
                return

            if not current_loc:
                logger.error(f"Current location not found: {self.eevee_state.location}")
                self.ui.print_error("Error: Current location is invalid")
                return

            if not self.world.can_travel(current_loc.id, target_loc.id):
                # Show available locations
                available = [loc.name for loc in self.world.get_connected_locations(current_loc.id)]
                self.ui.print_warning(f"You can't go directly to {target_loc.name} from {current_loc.name}.")
                if available:
                    self.ui.print_info(f"From here, you can go to:\n   • " + "\n   • ".join(available))
                else:
                    self.ui.print_info("Type 'world' to see the map.")
                return

            # Travel
            self.ui.print_system_message(f"Traveling to {target_loc.name}...")
            self.eevee_state.update_location(target_loc.id)

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

        except Exception as e:
            logger.error(f"Error during travel: {e}", exc_info=True)
            self.ui.print_error(f"Failed to travel: {e}")

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
        """Show detailed stats with beautiful visual display"""
        state = self.eevee_state
        personality = self.personality

        # Use new detailed stats display
        self.ui.print_detailed_stats(state, personality)

        # Eevee reacts to being checked
        try:
            self.ui.print_thinking("💭 Responding...")

            context = self._build_context()
            response, _ = self.response_gen.generate_response(
                "The trainer is checking how I'm doing",
                context,
                debug=self.debug_mode,
                world_map=self.world
            )

            self.ui.clear_thinking()
            self.ui.print_eevee_response(response)

            self._update_after_interaction("stats", "check stats", response)
        except Exception as e:
            logger.error(f"Error generating stats response: {e}")

    def show_world(self):
        """Show world/location info with Eevee's perspective"""
        location = self.world.get_location(self.eevee_state.location)
        if location:
            description = self.world.describe_location(location.id)
            self.ui.print_location_description(description)

            # Eevee comments on the surroundings
            try:
                context = self._build_context()
                response, _ = self.response_gen.generate_response(
                    f"Looking around {location.name}",
                    context,
                    debug=self.debug_mode,
                    world_map=self.world
                )
                self.ui.print_eevee_response(response)

                self._update_after_interaction("world", "look around", response)
            except Exception as e:
                logger.error(f"Error generating world response: {e}")

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
        elif args == "memory":
            Config.SHOW_MEMORY_RETRIEVAL = not Config.SHOW_MEMORY_RETRIEVAL
            status = "enabled" if Config.SHOW_MEMORY_RETRIEVAL else "disabled"
            self.ui.print_system_message(f"Memory retrieval visualization {status}")
        elif args.startswith("time "):
            # Phase 4: Simulate time passage for testing
            try:
                hours = float(args.split()[1])
                self.simulate_time_for_debug(hours)
            except (ValueError, IndexError):
                self.ui.print_message("Usage: debug time <hours>")
        else:
            self.ui.print_message("Debug commands: on, off, brain, state, memory, time <hours>")

    def browse_memories(self, query: str):
        """
        Phase 3: Browse stored memories

        Args:
            query: Search query (or empty for stats)
        """
        if not self.memory_retriever or not self.vector_store:
            self.ui.print_message("Memory system not available")
            return

        try:
            if not query:
                # Show memory stats
                stats = self.vector_store.get_stats()
                self.ui.print_message("\n=== Memory Statistics ===")
                self.ui.print_message(f"Total memories: {stats['total_memories']}")
                for mem_type, count in stats['by_type'].items():
                    self.ui.print_message(f"  {mem_type.capitalize()}: {count}")
                self.ui.print_message("\nUse 'remember <query>' to search memories")
                return

            # Search memories
            self.ui.print_thinking(f"📚 Searching memories for '{query}'...")

            results = self.memory_retriever.search_memories(query, limit=10)

            # Clear loading indicator
            self.ui.clear_thinking()

            # Use new formatted memory display
            self.ui.print_formatted_memories(results)

        except Exception as e:
            logger.error(f"Error browsing memories: {e}")
            self.ui.print_error(f"Error browsing memories: {e}")

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
        """Build context dictionary with working memory"""
        context = PromptBuilder.build_context_dict(
            self.eevee_state,
            self.personality
        )

        # Phase 3 Fix: Add working memory (recent conversation) to context
        if self.memory_retriever:
            context['recent_memories'] = self.memory_retriever.working_memory.memories
            context['working_memory_context'] = self.memory_retriever.get_working_memory_context()

        return context

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

    def _form_memory(self, user_input: str, eevee_response: str,
                    context: dict, council_decision=None):
        """
        Phase 3: Form long-term memories from significant interactions

        Args:
            user_input: What the user said
            eevee_response: How Eevee responded
            context: Full context dict
            council_decision: Brain council decision (if available)
        """
        if not self.memory_consolidator or not self.memory_retriever:
            return  # Memory system not available

        try:
            # Add to working memory (short-term)
            interaction_summary = f"{user_input[:50]}... -> {eevee_response[:50]}..."
            self.memory_retriever.add_to_working_memory(interaction_summary)

            # Process for long-term memory formation
            memories = self.memory_consolidator.process_interaction(
                user_input=user_input,
                eevee_response=eevee_response,
                context=context,
                council_decision=council_decision
            )

            # Show memory formation in debug mode
            if memories and (self.debug_mode or Config.SHOW_MEMORY_RETRIEVAL):
                self.ui.print_system_message(
                    f"Formed {len(memories)} long-term memor{'y' if len(memories) == 1 else 'ies'}"
                )
                for memory in memories:
                    logger.info(f"Memory stored: {memory.memory_type.value} - {memory.content[:60]}...")

        except Exception as e:
            logger.error(f"Error forming memory: {e}")

    def show_timeline(self, detailed: bool = False):
        """
        Show recent autonomous activities.

        Args:
            detailed: If True, show detailed view with all activities
        """
        if not hasattr(self, 'last_timeline_data') or not self.last_timeline_data:
            self.ui.print_info("No recent timeline available.\n💡 Come back after being away for a while!")
            return

        data = self.last_timeline_data

        # Use summary or detailed view
        if detailed:
            self.ui.print_timeline_detail(
                activities=data['activities'],
                hours_elapsed=data['hours_elapsed']
            )
        else:
            self.ui.print_timeline_summary(
                activities=data['activities'],
                hours_elapsed=data['hours_elapsed'],
                net_changes=data['net_changes'],
                items_found=data['items_found']
            )

    def simulate_time_for_debug(self, hours: float):
        """
        Phase 4: Simulate time passage for testing purposes

        Args:
            hours: Number of hours to simulate
        """
        if not self.time_simulator:
            self.ui.print_message("Time simulation system not available")
            return

        if hours <= 0 or hours > 168:
            self.ui.print_message("Please specify hours between 0 and 168 (1 week)")
            return

        try:
            self.ui.print_system_message(f"Simulating {hours:.1f} hours of time passage...")

            # Get current state
            state_dict = {
                'hunger': self.eevee_state.hunger,
                'energy': self.eevee_state.energy,
                'happiness': self.eevee_state.happiness,
                'health': self.eevee_state.health,
                'hours_since_trainer': hours
            }

            # Run simulation (Phase 5: Now returns items_found)
            activities, net_changes, memories, items_found = self.time_simulator.simulate_time_passage(
                state=state_dict,
                hours_elapsed=hours,
                last_location=self.eevee_state.location
            )

            # Apply state changes
            self.eevee_state.update_physical_state(
                hunger=max(0, min(100, self.eevee_state.hunger + net_changes['hunger'])),
                energy=max(0, min(100, self.eevee_state.energy + net_changes['energy'])),
                happiness=max(0, min(100, self.eevee_state.happiness + net_changes['happiness'])),
                health=max(0, min(100, self.eevee_state.health + net_changes['health']))
            )

            # Phase 5: Add found items to inventory
            for item_id in items_found:
                self.eevee_state.add_item(item_id)

            # Generate and display timeline
            timeline_summary = self.time_simulator.generate_timeline_summary(
                activities=activities,
                hours_elapsed=hours
            )

            # Store for 'timeline' command
            self.last_timeline = timeline_summary

            # Display
            print(timeline_summary)
            self.ui.print_system_message(
                f"Simulation complete: {len(activities)} activities, {len(memories)} memories formed, {len(items_found)} items found"
            )

            # Show updated stats
            self.show_stats()

        except Exception as e:
            logger.error(f"Error during debug time simulation: {e}", exc_info=True)
            self.ui.print_error(f"Time simulation failed: {e}")

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
