"""
Always-On Manager for EeveeLLM

Enables continuous runtime where Eevee lives their life 24/7.
Handles background simulation, auto-save, idle detection, and maintenance mode.
"""

from datetime import datetime, timedelta
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class AlwaysOnManager:
    """
    Manages continuous runtime for EeveeLLM.

    Responsibilities:
    - Background activity simulation (every hour)
    - Auto-save state (every 5 minutes)
    - Idle detection (user present vs away)
    - Maintenance mode coordination
    """

    def __init__(self, eevee_state, time_simulator, config: dict = None):
        """
        Initialize AlwaysOnManager.

        Args:
            eevee_state: EeveeState instance
            time_simulator: TimeSimulator instance
            config: Optional configuration dict
        """
        self.eevee_state = eevee_state
        self.time_simulator = time_simulator

        # Configuration (with defaults)
        config = config or {}
        self.simulation_interval = config.get('simulation_interval', 3600)  # 1 hour in seconds
        self.auto_save_interval = config.get('auto_save_interval', 300)     # 5 minutes in seconds
        self.idle_threshold = config.get('idle_threshold', 300)              # 5 minutes in seconds

        # State tracking
        self.last_simulation = datetime.now()
        self.last_save = datetime.now()
        self.last_interaction = datetime.now()
        self.startup_time = datetime.now()

        # Statistics
        self.total_simulations = 0
        self.total_saves = 0

        logger.info(f"AlwaysOnManager initialized with simulation every {self.simulation_interval}s, auto-save every {self.auto_save_interval}s")

    def update(self) -> dict:
        """
        Main update loop - call this every iteration.

        Returns:
            dict with keys:
                - 'simulation_ran': bool
                - 'save_performed': bool
                - 'activities': list of Activity objects (if simulation ran)
        """
        result = {
            'simulation_ran': False,
            'save_performed': False,
            'activities': []
        }

        # Check if we should run background simulation
        sim_result = self._check_background_simulation()
        if sim_result:
            result['simulation_ran'] = True
            result['activities'] = sim_result

        # Check if we should auto-save
        if self._check_auto_save():
            result['save_performed'] = True

        return result

    def _check_background_simulation(self) -> Optional[list]:
        """
        Check if it's time to run background simulation.

        Returns:
            List of Activity objects if simulation ran, None otherwise
        """
        now = datetime.now()
        elapsed_seconds = (now - self.last_simulation).total_seconds()

        if elapsed_seconds >= self.simulation_interval:
            hours_elapsed = elapsed_seconds / 3600

            logger.info(f"Running background simulation for {hours_elapsed:.2f} hours")

            try:
                # Run time simulation
                state_dict = {
                    'hunger': self.eevee_state.hunger,
                    'energy': self.eevee_state.energy,
                    'happiness': self.eevee_state.happiness,
                    'health': self.eevee_state.health,
                    'hours_since_trainer': hours_elapsed
                }

                activities, net_changes, memories, items_found = self.time_simulator.simulate_time_passage(
                    state=state_dict,
                    hours_elapsed=hours_elapsed,
                    last_location=self.eevee_state.location
                )

                # Apply state changes
                self.eevee_state.update_physical_state(
                    hunger=max(0, min(100, self.eevee_state.hunger + net_changes['hunger'])),
                    energy=max(0, min(100, self.eevee_state.energy + net_changes['energy'])),
                    happiness=max(0, min(100, self.eevee_state.happiness + net_changes['happiness'])),
                    health=max(0, min(100, self.eevee_state.health + net_changes['health']))
                )

                # Update location if it changed (from last activity)
                if activities:
                    last_activity = activities[-1]
                    if hasattr(last_activity, 'location'):
                        self.eevee_state.location = last_activity.location

                # Add items to inventory
                for item in items_found:
                    self.eevee_state.add_item(item)

                self.last_simulation = now
                self.total_simulations += 1

                logger.info(f"Background simulation complete: {len(activities)} activities, {len(memories)} memories, {len(items_found)} items")

                return activities

            except Exception as e:
                logger.error(f"Error during background simulation: {e}", exc_info=True)
                # Don't crash - just skip this simulation
                self.last_simulation = now
                return None

        return None

    def _check_auto_save(self) -> bool:
        """
        Check if it's time to auto-save state.

        Returns:
            True if save was performed, False otherwise
        """
        now = datetime.now()
        elapsed_seconds = (now - self.last_save).total_seconds()

        if elapsed_seconds >= self.auto_save_interval:
            try:
                self.eevee_state.save()
                self.last_save = now
                self.total_saves += 1
                logger.debug(f"Auto-save #{self.total_saves} performed")
                return True
            except Exception as e:
                logger.error(f"Error during auto-save: {e}", exc_info=True)
                # Don't crash - just skip this save
                self.last_save = now
                return False

        return False

    def mark_user_interaction(self):
        """Call this whenever the user interacts (types something)."""
        self.last_interaction = datetime.now()
        logger.debug("User interaction marked")

    def is_user_idle(self) -> bool:
        """
        Check if user is currently idle.

        Returns:
            True if user hasn't interacted recently, False otherwise
        """
        now = datetime.now()
        idle_seconds = (now - self.last_interaction).total_seconds()
        return idle_seconds >= self.idle_threshold

    def get_idle_duration(self) -> timedelta:
        """
        Get how long the user has been idle.

        Returns:
            timedelta since last interaction
        """
        return datetime.now() - self.last_interaction

    def get_uptime(self) -> timedelta:
        """
        Get how long the app has been running.

        Returns:
            timedelta since startup
        """
        return datetime.now() - self.startup_time

    def get_stats(self) -> dict:
        """
        Get statistics about always-on operation.

        Returns:
            dict with uptime, simulations, saves, etc.
        """
        uptime = self.get_uptime()
        idle_duration = self.get_idle_duration()

        return {
            'uptime': uptime,
            'uptime_hours': uptime.total_seconds() / 3600,
            'idle_duration': idle_duration,
            'idle_seconds': idle_duration.total_seconds(),
            'is_idle': self.is_user_idle(),
            'total_simulations': self.total_simulations,
            'total_saves': self.total_saves,
            'last_simulation': self.last_simulation,
            'last_save': self.last_save,
            'last_interaction': self.last_interaction
        }

    def get_current_activity_description(self) -> str:
        """
        Generate a description of what Eevee is currently doing based on state.

        This is shown when user checks in after being idle.

        Returns:
            String describing current activity
        """
        state = self.eevee_state

        # Time-based activities
        hour = datetime.now().hour

        # Night time (10 PM - 6 AM)
        if hour >= 22 or hour < 6:
            if state.energy < 40:
                return "sleeping peacefully, curled up in a cozy spot"
            else:
                return "resting quietly, occasionally looking around in the darkness"

        # Morning (6 AM - 12 PM)
        elif hour >= 6 and hour < 12:
            if state.energy > 70:
                return "stretching and enjoying the morning sun"
            elif state.hunger > 60:
                return "looking around for breakfast"
            else:
                return "exploring the area with fresh morning energy"

        # Afternoon (12 PM - 6 PM)
        elif hour >= 12 and hour < 18:
            if state.happiness > 70 and state.energy > 60:
                return "playing happily in the sunshine"
            elif state.energy < 40:
                return "taking a peaceful afternoon nap"
            elif state.hunger > 70:
                return "sniffing around, looking quite hungry"
            else:
                return "lounging contentedly, watching the world go by"

        # Evening (6 PM - 10 PM)
        else:
            if state.energy < 50:
                return "winding down for the evening, yawning occasionally"
            elif state.happiness < 50:
                return "sitting quietly, looking a bit lonely"
            else:
                return "relaxing peacefully as the day comes to an end"
