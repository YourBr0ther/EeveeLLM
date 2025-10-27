"""
Brain Council - Neuromodulator Systems (Phase 6)
Implements dopamine, serotonin, and other neuromodulators that influence brain regions
"""
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class NeuromodulatorState:
    """Current state of all neuromodulators"""
    dopamine: float = 0.5  # 0.0 to 1.0 (reward/motivation)
    serotonin: float = 0.5  # 0.0 to 1.0 (mood/contentment)
    norepinephrine: float = 0.5  # 0.0 to 1.0 (arousal/alertness)


class DopamineSystem:
    """
    Dopamine system - Reward, motivation, and learning

    Influences:
    - Reward prediction and expectation
    - Motivation to seek goals
    - Learning from positive outcomes
    - Pleasure from achievement
    """

    def __init__(self):
        self.baseline_level = 0.5  # Baseline dopamine
        self.current_level = 0.5
        self.recent_rewards = []  # Track recent reward history

    def process_context(self, context: Dict[str, Any]) -> float:
        """
        Calculate current dopamine level based on context

        Args:
            context: Current state context

        Returns:
            Dopamine level (0.0 to 1.0)
        """
        state = context.get('physical_state', {})
        relationship = context.get('relationship', {})

        happiness = state.get('happiness', 50)
        bond = relationship.get('bond', 0)
        trust = relationship.get('trust', 50)

        # Base dopamine from happiness
        dopamine = happiness / 100.0

        # Strong relationship increases baseline dopamine
        if bond > 70:
            dopamine += 0.15
        elif bond > 50:
            dopamine += 0.1

        # High trust increases dopamine
        if trust > 80:
            dopamine += 0.1

        # Clamp to valid range
        self.current_level = max(0.0, min(1.0, dopamine))
        return self.current_level

    def predict_reward(self, situation: str, context: Dict[str, Any]) -> float:
        """
        Predict expected reward from situation (reward prediction)

        Args:
            situation: Description of situation
            context: Current context

        Returns:
            Predicted reward value (0.0 to 1.0)
        """
        relationship = context.get('relationship', {})
        bond = relationship.get('bond', 0)

        # Predict rewards based on situation
        if "trainer" in situation.lower():
            # Trainer interaction predicted to be rewarding
            return 0.8 + (bond / 500.0)  # Higher bond = higher prediction

        elif "play" in situation.lower():
            # Play predicted to be rewarding
            return 0.7

        elif "food" in situation.lower() or "eat" in situation.lower():
            state = context.get('physical_state', {})
            hunger = state.get('hunger', 50)
            # Food more rewarding when hungry
            return 0.5 + (hunger / 200.0)

        elif "explore" in situation.lower():
            # Exploration moderately rewarding
            return 0.6

        else:
            # Unknown situation, moderate prediction
            return 0.5

    def calculate_reward_prediction_error(self, predicted: float, actual: float) -> float:
        """
        Calculate reward prediction error (RPE)

        Positive RPE = Better than expected (dopamine burst)
        Negative RPE = Worse than expected (dopamine dip)

        Args:
            predicted: Predicted reward
            actual: Actual reward received

        Returns:
            Reward prediction error (-1.0 to 1.0)
        """
        return actual - predicted

    def get_motivational_boost(self, situation: str, context: Dict[str, Any]) -> float:
        """
        Calculate motivational boost from dopamine for this situation

        Args:
            situation: Current situation
            context: Context

        Returns:
            Motivational factor (0.0 to 1.0)
        """
        predicted_reward = self.predict_reward(situation, context)

        # Higher predicted reward = more motivation
        # Current dopamine level also influences motivation
        motivation = (predicted_reward * 0.7) + (self.current_level * 0.3)

        return max(0.0, min(1.0, motivation))


class SerotoninSystem:
    """
    Serotonin system - Mood, contentment, and well-being

    Influences:
    - Overall mood and contentment
    - Social confidence
    - Anxiety regulation (inversely)
    - Long-term satisfaction
    """

    def __init__(self):
        self.baseline_level = 0.5
        self.current_level = 0.5

    def process_context(self, context: Dict[str, Any]) -> float:
        """
        Calculate current serotonin level

        Args:
            context: Current state context

        Returns:
            Serotonin level (0.0 to 1.0)
        """
        state = context.get('physical_state', {})
        relationship = context.get('relationship', {})

        happiness = state.get('happiness', 50)
        health = state.get('health', 100)
        bond = relationship.get('bond', 0)

        # Serotonin from overall well-being
        serotonin = (happiness / 100.0) * 0.5
        serotonin += (health / 100.0) * 0.3
        serotonin += (bond / 100.0) * 0.2

        # Good physical state increases serotonin
        energy = state.get('energy', 50)
        hunger = state.get('hunger', 50)

        if energy > 60 and hunger < 40:
            serotonin += 0.1  # Comfortable = more serotonin

        self.current_level = max(0.0, min(1.0, serotonin))
        return self.current_level

    def get_mood_influence(self) -> str:
        """
        Get current mood based on serotonin level

        Returns:
            Mood description
        """
        if self.current_level > 0.7:
            return "content and positive"
        elif self.current_level > 0.5:
            return "balanced and stable"
        elif self.current_level > 0.3:
            return "somewhat low and unsettled"
        else:
            return "low and uncomfortable"


class NorepinephrineSystem:
    """
    Norepinephrine system - Arousal, alertness, and stress response

    Influences:
    - Alertness and focus
    - Stress response
    - Fight-or-flight activation
    - Attention to threats
    """

    def __init__(self):
        self.baseline_level = 0.5
        self.current_level = 0.5

    def process_context(self, context: Dict[str, Any]) -> float:
        """
        Calculate current norepinephrine level

        Args:
            context: Current state context

        Returns:
            Norepinephrine level (0.0 to 1.0)
        """
        state = context.get('physical_state', {})
        location_safety = context.get('location_safety', 10)

        energy = state.get('energy', 50)
        health = state.get('health', 100)

        # Base level from energy (alertness)
        norepinephrine = energy / 100.0

        # Low health or dangerous location increases norepinephrine
        if health < 50:
            norepinephrine += 0.3  # Stress response
        if location_safety < 5:
            norepinephrine += 0.4  # Threat detection

        self.current_level = max(0.0, min(1.0, norepinephrine))
        return self.current_level


class NeuromodulatorOrchestrator:
    """
    Orchestrates all neuromodulator systems and provides unified influence
    """

    def __init__(self):
        self.dopamine = DopamineSystem()
        self.serotonin = SerotoninSystem()
        self.norepinephrine = NorepinephrineSystem()

    def update_all(self, context: Dict[str, Any]) -> NeuromodulatorState:
        """
        Update all neuromodulator levels based on current context

        Args:
            context: Current state context

        Returns:
            NeuromodulatorState with all current levels
        """
        dopamine_level = self.dopamine.process_context(context)
        serotonin_level = self.serotonin.process_context(context)
        norepinephrine_level = self.norepinephrine.process_context(context)

        return NeuromodulatorState(
            dopamine=dopamine_level,
            serotonin=serotonin_level,
            norepinephrine=norepinephrine_level
        )

    def apply_modulation_to_vote(self, vote, neuromodulator_state: NeuromodulatorState):
        """
        Apply neuromodulator influence to a brain region's vote

        Args:
            vote: RegionVote to modify
            neuromodulator_state: Current neuromodulator levels
        """
        # Dopamine increases confidence and emotional weight for positive decisions
        if "yes" in vote.decision.lower() or "agree" in vote.decision.lower():
            vote.confidence *= (1.0 + (neuromodulator_state.dopamine - 0.5) * 0.2)

        # Serotonin stabilizes emotions (reduces extreme emotional weight)
        if neuromodulator_state.serotonin > 0.6:
            vote.emotional_weight *= 0.9  # Calm, less emotional reactivity
        elif neuromodulator_state.serotonin < 0.4:
            vote.emotional_weight *= 1.1  # Low mood, more emotionally reactive

        # Norepinephrine increases arousal level
        vote.arousal_level *= (1.0 + (neuromodulator_state.norepinephrine - 0.5) * 0.3)

        # Clamp values to valid ranges
        vote.confidence = max(0.0, min(1.0, vote.confidence))
        vote.emotional_weight = max(0.0, min(1.0, vote.emotional_weight))
        vote.arousal_level = max(0.0, min(1.0, vote.arousal_level))
