"""
Brain Council - Decision Making System
Handles voting, conflict resolution, and final decision selection
"""
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

from .regions import RegionVote


@dataclass
class CouncilDecision:
    """Final decision from brain council"""
    winning_vote: RegionVote
    all_votes: List[RegionVote]
    total_scores: Dict[str, float]
    decision_summary: str
    consensus_level: float  # 0.0 to 1.0, how unified was the decision
    conflict_level: float = 0.0  # Phase 6: 0.0 to 1.0, how much conflict detected (ACC)
    conflict_detected: bool = False  # Phase 6: Whether ACC detected significant conflict
    retrieved_memories: List[Tuple[str, Dict[str, Any], float]] = None  # Retrieved memories from Hippocampus


class DecisionEngine:
    """Processes brain region votes and makes final decisions"""

    def __init__(self):
        # Phase 6: ACC (Anterior Cingulate Cortex) - monitors conflict
        self.acc_conflict_threshold = 0.6  # Threshold for detecting significant conflict

    def calculate_vote_score(self, vote: RegionVote, region_weight: float) -> float:
        """
        Calculate weighted score for a vote

        Args:
            vote: The region's vote
            region_weight: The region's effective weight

        Returns:
            Weighted score
        """
        # Base score from weight and confidence
        base_score = region_weight * vote.confidence

        # Emotional weight influences the score
        emotional_factor = 1.0 + (vote.emotional_weight * 0.5)

        return base_score * emotional_factor

    def resolve_votes(self, votes: List[Tuple[RegionVote, float]]) -> CouncilDecision:
        """
        Resolve votes from all brain regions

        Args:
            votes: List of (RegionVote, effective_weight) tuples

        Returns:
            CouncilDecision with winning vote and analysis
        """
        if not votes:
            raise ValueError("No votes to resolve")

        # Calculate scores for each vote
        vote_scores = []
        for vote, weight in votes:
            score = self.calculate_vote_score(vote, weight)
            vote_scores.append((vote, score))

        # Sort by score (highest first)
        vote_scores.sort(key=lambda x: x[1], reverse=True)

        # Get winning vote
        winning_vote, winning_score = vote_scores[0]

        # Calculate total scores by region for analysis
        total_scores = {
            vote.region_name: score
            for vote, score in vote_scores
        }

        # Calculate consensus level
        consensus = self._calculate_consensus(vote_scores)

        # Phase 6: ACC - Calculate conflict level
        conflict_level = self._acc_detect_conflict(vote_scores)
        conflict_detected = conflict_level > self.acc_conflict_threshold

        # Generate decision summary (include conflict info if detected)
        summary = self._generate_summary(vote_scores, consensus, conflict_level, conflict_detected)

        # Extract retrieved memories from ALL votes (not just winning vote)
        # Hippocampus often doesn't win but still has the memories!
        retrieved_memories = None
        for vote, _ in vote_scores:
            if hasattr(vote, 'retrieved_memories') and vote.retrieved_memories:
                retrieved_memories = vote.retrieved_memories
                break  # Found memories, use them

        return CouncilDecision(
            winning_vote=winning_vote,
            all_votes=[vote for vote, _ in vote_scores],
            total_scores=total_scores,
            decision_summary=summary,
            consensus_level=consensus,
            conflict_level=conflict_level,
            conflict_detected=conflict_detected,
            retrieved_memories=retrieved_memories
        )

    def _calculate_consensus(self, vote_scores: List[Tuple[RegionVote, float]]) -> float:
        """
        Calculate how unified the decision was

        Args:
            vote_scores: List of (vote, score) tuples sorted by score

        Returns:
            Consensus level (0.0 = split, 1.0 = unanimous)
        """
        if len(vote_scores) < 2:
            return 1.0

        # Compare top vote to others
        top_score = vote_scores[0][1]
        second_score = vote_scores[1][1] if len(vote_scores) > 1 else 0

        # Calculate ratio
        if top_score == 0:
            return 0.5

        ratio = 1.0 - (second_score / top_score)

        # Check for decision agreement (similar decisions)
        top_decision = vote_scores[0][0].decision
        agreeing_votes = sum(
            1 for vote, _ in vote_scores
            if self._decisions_agree(top_decision, vote.decision)
        )

        agreement_factor = agreeing_votes / len(vote_scores)

        # Combine ratio and agreement
        consensus = (ratio * 0.6) + (agreement_factor * 0.4)

        return max(0.0, min(1.0, consensus))

    def _decisions_agree(self, decision1: str, decision2: str) -> bool:
        """Check if two decisions are in agreement"""
        # Normalize decisions
        d1 = decision1.lower()
        d2 = decision2.lower()

        # Agreement groups
        positive_decisions = ['agree', 'yes', 'enthusiastic', 'excited', 'joyful', 'accept']
        negative_decisions = ['disagree', 'no', 'protest', 'fear', 'too_']
        caution_decisions = ['cautious', 'careful', 'maybe', 'consider']

        # Check if both in same group
        if any(term in d1 for term in positive_decisions) and any(term in d2 for term in positive_decisions):
            return True
        if any(term in d1 for term in negative_decisions) and any(term in d2 for term in negative_decisions):
            return True
        if any(term in d1 for term in caution_decisions) and any(term in d2 for term in caution_decisions):
            return True

        return False

    def _acc_detect_conflict(self, vote_scores: List[Tuple[RegionVote, float]]) -> float:
        """
        Phase 6: ACC (Anterior Cingulate Cortex) - Detect conflict between regions

        The ACC monitors for disagreement and competing responses, which signals
        the need for increased cognitive control and conflict resolution.

        Args:
            vote_scores: List of (vote, score) tuples sorted by score

        Returns:
            Conflict level (0.0 = no conflict, 1.0 = maximum conflict)
        """
        if len(vote_scores) < 2:
            return 0.0

        # Measure conflict using multiple signals:
        # 1. Score competition (how close are top scores?)
        top_score = vote_scores[0][1]
        second_score = vote_scores[1][1]

        if top_score == 0:
            score_conflict = 0.5
        else:
            # Higher ratio = less conflict (clear winner)
            # Lower ratio = more conflict (tight competition)
            score_conflict = second_score / top_score

        # 2. Decision disagreement (are decisions opposing?)
        top_decision = vote_scores[0][0].decision
        opposing_votes = sum(
            1 for vote, _ in vote_scores
            if not self._decisions_agree(top_decision, vote.decision)
        )
        decision_conflict = opposing_votes / len(vote_scores)

        # 3. Emotional conflict (are emotions clashing?)
        top_emotion = vote_scores[0][0].primary_emotion
        emotion_variety = len(set(vote.primary_emotion for vote, _ in vote_scores))
        emotion_conflict = min(1.0, emotion_variety / 5.0)  # More variety = more conflict

        # Weighted combination
        total_conflict = (
            score_conflict * 0.4 +
            decision_conflict * 0.4 +
            emotion_conflict * 0.2
        )

        return max(0.0, min(1.0, total_conflict))

    def _generate_summary(self, vote_scores: List[Tuple[RegionVote, float]],
                         consensus: float, conflict_level: float = 0.0,
                         conflict_detected: bool = False) -> str:
        """Generate human-readable summary"""
        winning_vote = vote_scores[0][0]

        # Phase 6: ACC modifies tone based on conflict detection
        if conflict_detected:
            tone = "After significant internal conflict, the council decides:"
        elif consensus > 0.8:
            tone = "The council unanimously agrees:"
        elif consensus > 0.6:
            tone = "The council generally agrees:"
        elif consensus > 0.4:
            tone = "The council is leaning towards:"
        else:
            tone = "After debate, the council decides:"

        summary = f"{tone} {winning_vote.decision}\n"
        summary += f"Primary reasoning: {winning_vote.reasoning}"

        # Add notable dissenting opinions
        if consensus < 0.7 and len(vote_scores) > 1:
            second_vote = vote_scores[1][0]
            if not self._decisions_agree(winning_vote.decision, second_vote.decision):
                summary += f"\n(Note: {second_vote.region_name} suggests: {second_vote.decision})"

        # Phase 6: Add conflict warning if ACC detected significant conflict
        if conflict_detected:
            summary += f"\n(ACC Warning: High internal conflict detected - {conflict_level:.2f})"

        return summary

    def get_dominant_emotion(self, votes: List[RegionVote]) -> str:
        """
        Determine dominant emotion from votes

        Args:
            votes: List of all votes

        Returns:
            Emotion string
        """
        # Find vote with highest emotional weight
        emotional_vote = max(votes, key=lambda v: v.emotional_weight)

        # Extract emotion from decision
        decision = emotional_vote.decision.lower()

        if 'joy' in decision or 'happy' in decision or 'excited' in decision:
            return "joyful"
        elif 'fear' in decision or 'scary' in decision or 'afraid' in decision:
            return "fearful"
        elif 'sad' in decision or 'lonely' in decision:
            return "sad"
        elif 'angry' in decision or 'frustrated' in decision:
            return "frustrated"
        elif 'curious' in decision or 'interested' in decision:
            return "curious"
        elif 'cautious' in decision or 'nervous' in decision:
            return "cautious"
        else:
            return "calm"

    def get_decision_confidence(self, decision: CouncilDecision) -> str:
        """Get text description of confidence level"""
        if decision.consensus_level > 0.8:
            return "very confident"
        elif decision.consensus_level > 0.6:
            return "confident"
        elif decision.consensus_level > 0.4:
            return "somewhat confident"
        else:
            return "uncertain"
