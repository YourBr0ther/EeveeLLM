"""
Time Simulation Engine

Handles autonomous time passage when the user is away.
Generates activities, applies state changes, and creates memories.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

from world.activities import ActivityGenerator, Activity, ActivityType
from memory.consolidation import MemoryConsolidator

logger = logging.getLogger(__name__)


@dataclass
class TimelineEntry:
    """
    A single entry in the timeline shown to the user

    Combines multiple activities into digestible narrative chunks
    """
    timestamp: datetime
    summary: str
    activities: List[Activity]
    net_state_change: Dict[str, int]
    significant: bool = False


class TimeSimulator:
    """
    Simulates autonomous time passage

    When the user returns after being away, this generates:
    1. Timeline of activities Eevee performed
    2. State changes from those activities
    3. Memories formed during time away

    Activity generation follows realistic patterns:
    - Every 2-4 hours: Generate an activity
    - Urgent needs override other activities
    - Personality influences exploration/play
    - Emotional state changes with time
    """

    def __init__(
        self,
        activity_generator: ActivityGenerator,
        memory_consolidator: Optional[MemoryConsolidator] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize time simulator

        Args:
            activity_generator: ActivityGenerator instance
            memory_consolidator: MemoryConsolidator for creating memories
            config: Configuration dict
        """
        self.activity_generator = activity_generator
        self.memory_consolidator = memory_consolidator
        self.config = config or {}

        # Simulation parameters
        self.min_activity_interval = 2.0  # Minimum hours between activities
        self.max_activity_interval = 4.0  # Maximum hours between activities
        self.max_simulation_hours = 168  # 7 days max (prevent excessive simulation)

    def simulate_time_passage(
        self,
        state: Dict[str, Any],
        hours_elapsed: float,
        last_location: str
    ) -> Tuple[List[Activity], Dict[str, int], List[str], List[str]]:
        """
        Simulate time passage and generate activities

        Args:
            state: Current Eevee state dict
            hours_elapsed: Hours since last interaction
            last_location: Last known location

        Returns:
            Tuple of (activities, net_state_changes, memories_formed, items_found)
        """
        if hours_elapsed <= 0:
            return [], {}, [], []

        # Cap simulation at max hours to prevent performance issues
        if hours_elapsed > self.max_simulation_hours:
            logger.warning(f"Capping simulation at {self.max_simulation_hours} hours (was {hours_elapsed:.1f})")
            hours_elapsed = self.max_simulation_hours

        logger.info(f"Simulating {hours_elapsed:.1f} hours of autonomous time passage")

        activities: List[Activity] = []
        current_state = self._copy_state(state)
        current_location = last_location
        current_time = datetime.now() - timedelta(hours=hours_elapsed)

        # Track state changes
        net_changes = {
            'hunger': 0,
            'energy': 0,
            'happiness': 0,
            'health': 0
        }

        memories_formed = []
        items_found = []  # Phase 5: Track items found during activities

        # Generate activities across the time period
        hours_simulated = 0.0

        while hours_simulated < hours_elapsed:
            # Determine next activity interval (2-4 hours)
            import random
            interval = random.uniform(self.min_activity_interval, self.max_activity_interval)

            # Don't overshoot elapsed time
            if hours_simulated + interval > hours_elapsed:
                interval = hours_elapsed - hours_simulated

            hours_simulated += interval
            activity_time = current_time + timedelta(hours=hours_simulated)

            # Apply passive state decay during this interval
            self._apply_passive_decay(current_state, interval)

            # Generate activity based on current state
            activity = self.activity_generator.generate_activity(
                state=current_state,
                elapsed_hours=interval,
                current_time=activity_time,
                last_location=current_location
            )

            activities.append(activity)

            # Apply activity's state changes
            current_state['hunger'] = max(0, min(100, current_state.get('hunger', 50) + activity.hunger_delta))
            current_state['energy'] = max(0, min(100, current_state.get('energy', 50) + activity.energy_delta))
            current_state['happiness'] = max(0, min(100, current_state.get('happiness', 70) + activity.happiness_delta))
            current_state['health'] = max(0, min(100, current_state.get('health', 100) + activity.health_delta))

            # Track net changes
            net_changes['hunger'] += activity.hunger_delta
            net_changes['energy'] += activity.energy_delta
            net_changes['happiness'] += activity.happiness_delta
            net_changes['health'] += activity.health_delta

            # Update location if activity moved Eevee
            current_location = activity.location

            # Update hours since trainer (for emotional state)
            current_state['hours_since_trainer'] = hours_elapsed - hours_simulated

            # Phase 5: Check if item was found during this activity
            if 'found_item' in activity.details:
                items_found.append(activity.details['found_item'])

            # Check if this activity should become a memory
            if activity.significance >= 7.0 and self.memory_consolidator:
                memory_description = self._create_autonomous_memory(activity)
                memories_formed.append(memory_description)

                # Store memory in vector database
                # Note: We'll create a simplified memory without council decision
                try:
                    from memory.memory_types import EpisodicMemory, MemoryType, EmotionType
                    import uuid

                    # Map emotion string to EmotionType
                    emotion_mapping = {
                        'fear': EmotionType.FEAR,
                        'joy': EmotionType.JOY,
                        'loneliness': EmotionType.LONELINESS,
                        'sadness': EmotionType.SADNESS,
                        'contentment': EmotionType.CONTENTMENT,
                        'curiosity': EmotionType.CURIOSITY,
                        'anxiety': EmotionType.FEAR,
                        'peace': EmotionType.CONTENTMENT,
                        'gratitude': EmotionType.GRATITUDE
                    }

                    primary_emotion = emotion_mapping.get(activity.emotion.lower())

                    autonomous_memory = EpisodicMemory(
                        memory_id=str(uuid.uuid4()),
                        memory_type=MemoryType.EPISODIC,
                        content=activity.description,
                        timestamp=activity.timestamp,
                        significance=activity.significance,
                        primary_emotion=primary_emotion,
                        emotion_intensity=activity.emotion_intensity,
                        location=activity.location,
                        participants=[],  # Solo activity
                        tags=["autonomous", activity.activity_type.value],
                        event_type=activity.activity_type.value,
                        outcome=None
                    )

                    self.memory_consolidator.vector_store.store_memory(autonomous_memory)
                    logger.info(f"Stored autonomous memory: {activity.description[:50]}...")

                except Exception as e:
                    logger.error(f"Failed to store autonomous memory: {e}")

        logger.info(f"Generated {len(activities)} activities over {hours_elapsed:.1f} hours")
        logger.info(f"Net state changes: {net_changes}")
        logger.info(f"Memories formed: {len(memories_formed)}")
        logger.info(f"Items found: {len(items_found)}")  # Phase 5

        return activities, net_changes, memories_formed, items_found

    def _copy_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create a working copy of state for simulation"""
        return {
            'hunger': state.get('hunger', 50),
            'energy': state.get('energy', 50),
            'happiness': state.get('happiness', 70),
            'health': state.get('health', 100),
            'hours_since_trainer': 0
        }

    def _apply_passive_decay(self, state: Dict[str, Any], hours: float):
        """
        Apply passive state decay during time passage

        Eevee gets hungrier and more tired naturally over time
        """
        # Hunger increases by ~5 per hour
        hunger_increase = hours * 5.0
        state['hunger'] = min(100, state.get('hunger', 50) + hunger_increase)

        # Energy decreases by ~3 per hour (unless sleeping)
        energy_decrease = hours * 3.0
        state['energy'] = max(0, state.get('energy', 50) - energy_decrease)

        # Happiness slowly decreases when alone (~1 per hour)
        happiness_decrease = hours * 1.0
        state['happiness'] = max(0, state.get('happiness', 70) - happiness_decrease)

    def _create_autonomous_memory(self, activity: Activity) -> str:
        """
        Create memory description for autonomous activity

        Args:
            activity: Activity that should become a memory

        Returns:
            str: Human-readable memory description
        """
        timestamp_str = activity.timestamp.strftime("%I:%M %p on %B %d")
        return f"[{timestamp_str}] {activity.description}"

    def generate_timeline_summary(
        self,
        activities: List[Activity],
        hours_elapsed: float
    ) -> str:
        """
        Generate human-readable timeline summary

        Args:
            activities: List of activities performed
            hours_elapsed: Total hours elapsed

        Returns:
            str: Formatted timeline for display
        """
        if not activities:
            return "No significant activities occurred."

        # Group activities by time period
        timeline_entries = self._group_activities_by_period(activities, hours_elapsed)

        # Build summary
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"  TIMELINE: What Eevee did while you were away")
        lines.append(f"  ({hours_elapsed:.1f} hours / {hours_elapsed/24:.1f} days)")
        lines.append(f"{'='*60}\n")

        for entry in timeline_entries:
            timestamp_str = entry.timestamp.strftime("%I:%M %p, %B %d")

            if entry.significant:
                lines.append(f"  ⭐ [{timestamp_str}]")
            else:
                lines.append(f"  • [{timestamp_str}]")

            lines.append(f"     {entry.summary}")

            # Show state changes if significant
            if abs(sum(entry.net_state_change.values())) > 20:
                changes = []
                for stat, delta in entry.net_state_change.items():
                    if delta != 0:
                        sign = "+" if delta > 0 else ""
                        changes.append(f"{stat} {sign}{delta}")

                if changes:
                    lines.append(f"     ({', '.join(changes)})")

            lines.append("")  # Blank line

        lines.append(f"{'='*60}\n")

        return "\n".join(lines)

    def _group_activities_by_period(
        self,
        activities: List[Activity],
        hours_elapsed: float
    ) -> List[TimelineEntry]:
        """
        Group activities into timeline entries

        For short absences (<6 hours), show all activities
        For longer absences, group by time period
        """
        if hours_elapsed <= 6:
            # Show all activities individually
            entries = []
            for activity in activities:
                entries.append(TimelineEntry(
                    timestamp=activity.timestamp,
                    summary=activity.description,
                    activities=[activity],
                    net_state_change={
                        'hunger': activity.hunger_delta,
                        'energy': activity.energy_delta,
                        'happiness': activity.happiness_delta,
                        'health': activity.health_delta
                    },
                    significant=(activity.significance >= 7.0)
                ))
            return entries

        else:
            # Group by 6-hour periods for longer absences
            # This prevents overwhelming the user with too many activities
            entries = []

            # Sort activities by time
            sorted_activities = sorted(activities, key=lambda a: a.timestamp)

            # Group into 6-hour chunks
            chunk_duration = timedelta(hours=6)
            current_chunk_start = sorted_activities[0].timestamp if sorted_activities else datetime.now()
            current_chunk: List[Activity] = []

            for activity in sorted_activities:
                # Check if this activity belongs to current chunk
                if activity.timestamp < current_chunk_start + chunk_duration:
                    current_chunk.append(activity)
                else:
                    # Save current chunk and start new one
                    if current_chunk:
                        entries.append(self._summarize_chunk(current_chunk, current_chunk_start))

                    current_chunk = [activity]
                    current_chunk_start = activity.timestamp

            # Don't forget last chunk
            if current_chunk:
                entries.append(self._summarize_chunk(current_chunk, current_chunk_start))

            return entries

    def _summarize_chunk(
        self,
        activities: List[Activity],
        chunk_start: datetime
    ) -> TimelineEntry:
        """
        Summarize a chunk of activities into a single timeline entry

        Args:
            activities: Activities in this time period
            chunk_start: Start time of this chunk

        Returns:
            TimelineEntry summarizing the chunk
        """
        # Calculate net state changes
        net_change = {
            'hunger': sum(a.hunger_delta for a in activities),
            'energy': sum(a.energy_delta for a in activities),
            'happiness': sum(a.happiness_delta for a in activities),
            'health': sum(a.health_delta for a in activities)
        }

        # Find most significant activity
        most_significant = max(activities, key=lambda a: a.significance)

        # Build summary
        summary_parts = []

        # Count activity types
        type_counts = {}
        for activity in activities:
            activity_type = activity.activity_type.value
            type_counts[activity_type] = type_counts.get(activity_type, 0) + 1

        # Mention most significant event first
        summary_parts.append(most_significant.description)

        # Add context if multiple activities
        if len(activities) > 1:
            other_types = [t for t in type_counts.keys() if type_counts[t] > 1]
            if other_types:
                summary_parts.append(f"(Also: {', '.join(other_types)})")

        return TimelineEntry(
            timestamp=chunk_start,
            summary=" ".join(summary_parts),
            activities=activities,
            net_state_change=net_change,
            significant=(most_significant.significance >= 7.0)
        )
