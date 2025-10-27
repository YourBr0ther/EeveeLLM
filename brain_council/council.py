"""
Brain Council - Main Orchestrator
Coordinates all brain regions and manages decision-making process
"""
from typing import Dict, Any, List, Optional, Tuple
import logging

from .regions import (
    BrainRegion, PrefrontalCortex, Amygdala, Hippocampus,
    Hypothalamus, BasalGanglia, RegionVote  # Phase 6: Renamed Cerebellum → BasalGanglia
)
from .decision import DecisionEngine, CouncilDecision
from .neuromodulators import NeuromodulatorOrchestrator  # Phase 6

logger = logging.getLogger(__name__)


class BrainCouncil:
    """
    Orchestrates the brain council decision-making process
    """

    def __init__(self):
        # Initialize all brain regions
        self.regions: List[BrainRegion] = [
            PrefrontalCortex(),
            Amygdala(),
            Hippocampus(),
            Hypothalamus(),
            BasalGanglia()  # Phase 6: Renamed from Cerebellum
        ]

        self.decision_engine = DecisionEngine()

        # Phase 6: Neuromodulator systems
        self.neuromodulators = NeuromodulatorOrchestrator()

        logger.info("Brain Council initialized with 5 regions + neuromodulators")

    def deliberate(self, situation: str, context: Dict[str, Any],
                   debug: bool = False) -> CouncilDecision:
        """
        Run the full deliberation process

        Args:
            situation: Description of current situation
            context: Context including state, memories, etc.
            debug: Whether to log detailed debug info

        Returns:
            CouncilDecision with final decision
        """
        if debug:
            logger.info(f"=== Brain Council Deliberation ===")
            logger.info(f"Situation: {situation}")

        # Phase 6: Update neuromodulator levels based on context
        neuromodulator_state = self.neuromodulators.update_all(context)

        if debug:
            logger.info(f"\nNeuromodulator Levels:")
            logger.info(f"  Dopamine: {neuromodulator_state.dopamine:.2f} (reward/motivation)")
            logger.info(f"  Serotonin: {neuromodulator_state.serotonin:.2f} (mood/contentment)")
            logger.info(f"  Norepinephrine: {neuromodulator_state.norepinephrine:.2f} (arousal/alertness)")

        # Phase 6: Emotional contagion - emotions spread between regions
        enable_contagion = context.get('enable_emotional_contagion', True)

        # Collect votes from all regions
        votes_with_weights = []

        for region in self.regions:
            # Get effective weight (can be modified by context)
            effective_weight = region.get_effective_weight(context)

            # Get the region's vote
            vote = region.analyze(situation, context)

            # Phase 6: Apply neuromodulator influence to vote
            self.neuromodulators.apply_modulation_to_vote(vote, neuromodulator_state)

            votes_with_weights.append((vote, effective_weight))

            if debug:
                logger.info(f"\n{region.name} (weight: {effective_weight:.2f}):")
                logger.info(f"  Decision: {vote.decision}")
                logger.info(f"  Reasoning: {vote.reasoning}")
                logger.info(f"  Confidence: {vote.confidence:.2f}")
                logger.info(f"  Emotional weight: {vote.emotional_weight:.2f}")
                logger.info(f"  Primary emotion: {vote.primary_emotion}")
                logger.info(f"  Arousal level: {vote.arousal_level:.2f}")

        # Phase 6: Apply emotional contagion between regions
        if enable_contagion:
            self._apply_emotional_contagion(votes_with_weights, debug)

        # Resolve votes to final decision
        decision = self.decision_engine.resolve_votes(votes_with_weights)

        if debug:
            logger.info(f"\n=== Final Decision ===")
            logger.info(f"Winner: {decision.winning_vote.region_name}")
            logger.info(f"Decision: {decision.winning_vote.decision}")
            logger.info(f"Consensus: {decision.consensus_level:.2f}")
            logger.info(f"Conflict Level (ACC): {decision.conflict_level:.2f}")
            if decision.conflict_detected:
                logger.info(f"⚠️  ACC detected significant conflict!")
            logger.info(f"Summary: {decision.decision_summary}")

        return decision

    def _apply_emotional_contagion(self, votes_with_weights: List[Tuple[Any, float]], debug: bool = False):
        """
        Phase 6: Apply emotional contagion between brain regions

        Emotions spread based on neural connectivity patterns:
        - Amygdala → All regions (emotional center, broadcasts to everyone)
        - Prefrontal Cortex → Hippocampus, Hypothalamus (executive control)
        - Hippocampus → Prefrontal Cortex, Amygdala (memories trigger emotions)
        - Hypothalamus → Amygdala (physical needs influence emotions)
        - Cerebellum → Limited influence (instincts are more isolated)

        Args:
            votes_with_weights: List of (RegionVote, effective_weight) tuples
            debug: Whether to log debug info
        """
        if debug:
            logger.info(f"\n=== Emotional Contagion ===")

        # Extract votes and create region lookup
        votes = [v for v, _ in votes_with_weights]
        region_lookup = {region.name: region for region in self.regions}

        # Define receptivity by region (how susceptible to emotional contagion)
        receptivity = {
            "Prefrontal Cortex": 0.2,  # Logic resists emotion (but not immune)
            "Amygdala": 0.1,  # Emotional center, less influenced by others
            "Hippocampus": 0.4,  # Memory highly influenced by emotion
            "Hypothalamus": 0.3,  # Physical needs moderately influenced
            "Basal Ganglia": 0.25  # Instincts/habits moderately influenced
        }

        # Apply contagion for each region
        for region in self.regions:
            # Get votes from other regions (exclude self)
            other_votes = [v for v in votes if v.region_name != region.name]

            # Special case: Amygdala's emotions are MORE influential
            if any(v.region_name == "Amygdala" for v in other_votes):
                amygdala_vote = next(v for v in other_votes if v.region_name == "Amygdala")
                # Boost amygdala's emotional influence
                amygdala_influence = receptivity[region.name] * 1.5  # 50% boost
                region.receive_emotional_contagion([amygdala_vote], amygdala_influence)

                if debug:
                    logger.info(f"{region.name} receives strong emotional influence from Amygdala")
                    logger.info(f"  New emotional state: {region.current_emotion} "
                              f"(intensity: {region.emotion_intensity:.2f})")

            # General contagion from all other regions
            region.receive_emotional_contagion(other_votes, receptivity[region.name])

    def get_debate_visualization(self, decision: CouncilDecision) -> str:
        """
        Create a visual representation of the debate

        Args:
            decision: The council decision

        Returns:
            Formatted string showing the debate
        """
        output = []
        output.append("=" * 70)
        output.append("BRAIN COUNCIL DELIBERATION")
        output.append("=" * 70)
        output.append("")

        # Show all votes
        for i, vote in enumerate(decision.all_votes, 1):
            score = decision.total_scores.get(vote.region_name, 0)
            winner_mark = " ← WINNER" if i == 1 else ""

            output.append(f"{i}. {vote.region_name}{winner_mark}")
            output.append(f"   Decision: {vote.decision}")
            output.append(f"   Reasoning: {vote.reasoning}")
            output.append(f"   Score: {score:.3f} | Confidence: {vote.confidence:.2f} | "
                         f"Emotional: {vote.emotional_weight:.2f}")
            output.append("")

        # Summary
        confidence_desc = self.decision_engine.get_decision_confidence(decision)
        output.append("-" * 70)
        output.append(f"Consensus Level: {decision.consensus_level:.2f} ({confidence_desc})")
        output.append(f"Dominant Emotion: {self.decision_engine.get_dominant_emotion(decision.all_votes)}")
        output.append("")
        output.append(decision.decision_summary)
        output.append("=" * 70)

        return "\n".join(output)

    def get_quick_summary(self, decision: CouncilDecision) -> str:
        """
        Get a quick one-line summary

        Args:
            decision: The council decision

        Returns:
            Brief summary string
        """
        winner = decision.winning_vote
        return f"[{winner.region_name} leads: {winner.decision}]"

    def get_internal_state_description(self, decision: CouncilDecision) -> str:
        """
        Get description of Eevee's internal state based on decision

        Args:
            decision: The council decision

        Returns:
            Description of internal experience
        """
        emotion = self.decision_engine.get_dominant_emotion(decision.all_votes)
        consensus = decision.consensus_level

        if consensus > 0.8:
            certainty = "certain and clear"
        elif consensus > 0.6:
            certainty = "mostly clear"
        elif consensus > 0.4:
            certainty = "somewhat conflicted"
        else:
            certainty = "very conflicted and uncertain"

        return f"Eevee feels {emotion} and {certainty} about this."

    def enhance_context_with_location(self, context: Dict[str, Any],
                                      world_map) -> Dict[str, Any]:
        """
        Add location safety information to context

        Args:
            context: Current context
            world_map: WorldMap object

        Returns:
            Enhanced context
        """
        location_id = context.get('location', 'trainer_home')
        location = world_map.get_location(location_id)

        if location:
            context['location_safety'] = location.safety_level
            context['location_has_food'] = location.has_food
            context['location_has_shelter'] = location.has_shelter

        return context
