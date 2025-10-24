"""
Brain Council - Individual Brain Regions
Each region represents a different aspect of decision-making
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class RegionVote:
    """Represents a brain region's vote on a decision"""
    region_name: str
    decision: str
    reasoning: str
    confidence: float  # 0.0 to 1.0
    emotional_weight: float  # 0.0 to 1.0


class BrainRegion(ABC):
    """Base class for brain regions"""

    def __init__(self, name: str, base_weight: float):
        self.name = name
        self.base_weight = base_weight

    @abstractmethod
    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """
        Analyze situation and return a vote

        Args:
            situation: Description of current situation
            context: Context including state, memories, etc.

        Returns:
            RegionVote with decision and reasoning
        """
        pass

    @abstractmethod
    def get_role_description(self) -> str:
        """Get description of this region's role"""
        pass

    def get_effective_weight(self, context: Dict[str, Any]) -> float:
        """
        Calculate effective weight based on context

        Args:
            context: Current state context

        Returns:
            Modified weight
        """
        return self.base_weight


class PrefrontalCortex(BrainRegion):
    """Logic, planning, and long-term thinking"""

    def __init__(self):
        super().__init__("Prefrontal Cortex", 0.25)

    def get_role_description(self) -> str:
        return "Logic & Planning - Evaluates long-term consequences and trainer relationship"

    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Analyze from logical and planning perspective"""
        state = context.get('physical_state', {})
        relationship = context.get('relationship', {})

        # Consider energy levels for planning
        energy = state.get('energy', 50)
        trust = relationship.get('trust', 50)

        # Logical assessment
        if "explore" in situation.lower() or "adventure" in situation.lower():
            if energy > 40:
                decision = "agree_cautiously"
                reasoning = "Exploring builds experience and strengthens our bond with trainer. But we should stay alert."
                confidence = 0.7 + (trust / 200)  # Higher trust = more confidence
            else:
                decision = "suggest_rest_first"
                reasoning = "Logic suggests we rest before exploring. Low energy could be dangerous."
                confidence = 0.8
        elif "play" in situation.lower():
            if energy > 30:
                decision = "agree"
                reasoning = "Playing strengthens bond with trainer. It's a good use of energy."
                confidence = 0.8
            else:
                decision = "suggest_later"
                reasoning = "We should conserve energy. Perhaps after rest?"
                confidence = 0.7
        elif "food" in situation.lower() or "eat" in situation.lower():
            decision = "agree"
            reasoning = "Meeting basic needs is logical and necessary."
            confidence = 0.9
        else:
            decision = "consider_options"
            reasoning = "Let's think about the consequences before acting."
            confidence = 0.6

        return RegionVote(
            region_name=self.name,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            emotional_weight=0.3
        )


class Amygdala(BrainRegion):
    """Emotion and survival instincts"""

    def __init__(self):
        super().__init__("Amygdala", 0.30)

    def get_role_description(self) -> str:
        return "Emotion & Survival - Processes fear, joy, and excitement"

    def get_effective_weight(self, context: Dict[str, Any]) -> float:
        """Amygdala weight increases under stress or strong emotion"""
        state = context.get('physical_state', {})
        location_safety = context.get('location_safety', 10)

        # Increase weight in dangerous situations
        if location_safety < 5:
            return 0.60  # Survival instinct takes over
        elif state.get('health', 100) < 30:
            return 0.50  # Fear from being hurt

        return self.base_weight

    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Analyze from emotional perspective"""
        state = context.get('physical_state', {})
        relationship = context.get('relationship', {})
        location_safety = context.get('location_safety', 10)

        happiness = state.get('happiness', 50)
        trust = relationship.get('trust', 50)

        # Emotional reactions
        if "trainer" in situation.lower() and trust > 60:
            decision = "enthusiastic_yes"
            reasoning = "TRAINER! My favorite person! This makes me so happy!"
            confidence = 0.95
            emotional_weight = 1.0

        elif "explore" in situation.lower():
            if location_safety > 7 and trust > 60:
                decision = "excited_agree"
                reasoning = "Adventure with trainer! Exciting but safe with them!"
                confidence = 0.8
                emotional_weight = 0.9
            elif location_safety < 5:
                decision = "fear_disagree"
                reasoning = "Scary... Unknown places make me nervous. Too dangerous!"
                confidence = 0.9
                emotional_weight = 1.0
            else:
                decision = "cautious_maybe"
                reasoning = "Nervous but curious... Stay close to trainer?"
                confidence = 0.6
                emotional_weight = 0.7

        elif "play" in situation.lower():
            if happiness > 50:
                decision = "joyful_yes"
                reasoning = "YES! Playing is the BEST! So much joy!"
                confidence = 0.9
                emotional_weight = 1.0
            else:
                decision = "subdued_yes"
                reasoning = "Playing might make me feel better..."
                confidence = 0.6
                emotional_weight = 0.5

        elif "alone" in situation.lower() or "leave" in situation.lower():
            decision = "sad_protest"
            reasoning = "Don't go! Being alone is scary and lonely!"
            confidence = 0.8
            emotional_weight = 0.9

        else:
            decision = "curious"
            reasoning = "Interesting... How do I feel about this?"
            confidence = 0.5
            emotional_weight = 0.6

        return RegionVote(
            region_name=self.name,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            emotional_weight=emotional_weight
        )


class Hippocampus(BrainRegion):
    """Memory and context"""

    def __init__(self):
        super().__init__("Hippocampus", 0.20)

    def get_role_description(self) -> str:
        return "Memory - Recalls past experiences and identifies patterns"

    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Analyze based on memories and patterns"""
        memories = context.get('recent_memories', [])
        relationship = context.get('relationship', {})

        # Check for relevant memories
        relevant_memory = None
        for memory in memories[:5]:  # Check recent memories
            if any(word in memory.lower() for word in situation.lower().split()):
                relevant_memory = memory
                break

        if relevant_memory:
            # We have relevant experience
            if "positive" in relevant_memory or "fun" in relevant_memory or "happy" in relevant_memory:
                decision = "remember_positive"
                reasoning = f"I remember: {relevant_memory}. That was good!"
                confidence = 0.8
            elif "scary" in relevant_memory or "bad" in relevant_memory or "hurt" in relevant_memory:
                decision = "remember_negative"
                reasoning = f"I remember: {relevant_memory}. That was scary..."
                confidence = 0.8
            else:
                decision = "remember_neutral"
                reasoning = f"I remember something similar: {relevant_memory}"
                confidence = 0.6
        else:
            # New experience
            if relationship.get('bond', 0) > 50:
                decision = "trust_pattern"
                reasoning = "No direct memory, but past experiences with trainer have been mostly positive."
                confidence = 0.6
            else:
                decision = "no_pattern"
                reasoning = "This is new. No past experience to guide us."
                confidence = 0.4

        return RegionVote(
            region_name=self.name,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            emotional_weight=0.4
        )


class Hypothalamus(BrainRegion):
    """Physical needs and drives"""

    def __init__(self):
        super().__init__("Hypothalamus", 0.15)

    def get_role_description(self) -> str:
        return "Needs & Drives - Monitors hunger, energy, comfort, and physical state"

    def get_effective_weight(self, context: Dict[str, Any]) -> float:
        """Weight increases when needs are urgent"""
        state = context.get('physical_state', {})

        hunger = state.get('hunger', 50)
        energy = state.get('energy', 50)

        # Urgent needs increase weight
        if hunger > 80 or energy < 20:
            return 0.35  # Needs become more important
        elif hunger > 60 or energy < 40:
            return 0.25

        return self.base_weight

    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Analyze based on physical needs"""
        state = context.get('physical_state', {})

        hunger = state.get('hunger', 50)
        energy = state.get('energy', 50)
        health = state.get('health', 100)

        # Check if situation addresses needs
        if "food" in situation.lower() or "eat" in situation.lower() or "berry" in situation.lower():
            if hunger > 50:
                decision = "urgent_need"
                reasoning = "HUNGRY! Need food now!"
                confidence = 0.95
            else:
                decision = "accept"
                reasoning = "Food is always good, even if not urgent."
                confidence = 0.7

        elif "rest" in situation.lower() or "sleep" in situation.lower() or "nap" in situation.lower():
            if energy < 30:
                decision = "urgent_need"
                reasoning = "So tired... Need rest badly."
                confidence = 0.95
            else:
                decision = "not_needed"
                reasoning = "Not particularly tired right now."
                confidence = 0.6

        elif "play" in situation.lower() or "explore" in situation.lower():
            if energy < 30:
                decision = "too_tired"
                reasoning = "Too exhausted for this. Need energy first."
                confidence = 0.9
            elif hunger > 70:
                decision = "too_hungry"
                reasoning = "Too hungry to focus. Need food first."
                confidence = 0.85
            elif health < 50:
                decision = "too_hurt"
                reasoning = "Not feeling well. Should rest."
                confidence = 0.9
            else:
                decision = "acceptable"
                reasoning = "Physical state is adequate for this activity."
                confidence = 0.7

        else:
            # General assessment
            if hunger > 70:
                decision = "distracted_hungry"
                reasoning = "Hard to focus... so hungry..."
                confidence = 0.7
            elif energy < 25:
                decision = "distracted_tired"
                reasoning = "Having trouble staying alert... need rest..."
                confidence = 0.7
            else:
                decision = "fine"
                reasoning = "Physical needs are manageable."
                confidence = 0.6

        return RegionVote(
            region_name=self.name,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            emotional_weight=0.2
        )


class Cerebellum(BrainRegion):
    """Instinct and coordination"""

    def __init__(self):
        super().__init__("Cerebellum", 0.10)

    def get_role_description(self) -> str:
        return "Instinct & Coordination - Species-specific behaviors and automatic responses"

    def analyze(self, situation: str, context: Dict[str, Any]) -> RegionVote:
        """Analyze based on instinct"""
        personality = context.get('personality', {})
        state = context.get('physical_state', {})

        playfulness = personality.get('playfulness', 5)
        energy = state.get('energy', 50)

        # Instinctive Eevee behaviors
        if "play" in situation.lower():
            if energy > 40 and playfulness > 6:
                decision = "instinct_yes"
                reasoning = "*tail wagging intensifies* Eevee instincts say PLAY!"
                confidence = 0.8
            else:
                decision = "instinct_mild"
                reasoning = "*ears perk up* Play instinct triggered but subdued."
                confidence = 0.6

        elif "danger" in situation.lower() or "threat" in situation.lower():
            decision = "fight_or_flight"
            reasoning = "*fur bristles* Survival instinct activated!"
            confidence = 0.9

        elif "trainer" in situation.lower():
            decision = "bond_response"
            reasoning = "*automatic tail wag* Pack bond instinct!"
            confidence = 0.85

        elif "explore" in situation.lower():
            curiosity = personality.get('curiosity', 5)
            if curiosity > 6:
                decision = "explore_instinct"
                reasoning = "*nose twitching* Natural curiosity activated!"
                confidence = 0.7
            else:
                decision = "cautious_instinct"
                reasoning = "*ears swivel* Proceed with caution."
                confidence = 0.6

        elif "food" in situation.lower():
            decision = "approach_food"
            reasoning = "*nose sniffing* Food-seeking behavior engaged!"
            confidence = 0.8

        else:
            decision = "observe"
            reasoning = "*alert posture* Monitoring situation instinctively."
            confidence = 0.5

        return RegionVote(
            region_name=self.name,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            emotional_weight=0.3
        )
