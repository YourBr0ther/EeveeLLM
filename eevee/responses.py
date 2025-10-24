"""
Eevee Response Generation
Handles generating responses using LLM and Brain Council
"""
from typing import Dict, Any, Optional
import logging

from llm.nanogpt_client import NanoGPTClient
from llm.prompts import PromptBuilder
from brain_council.council import BrainCouncil

logger = logging.getLogger(__name__)


class ResponseGenerator:
    """Generates Eevee responses"""

    def __init__(self, llm_client: Optional[NanoGPTClient] = None,
                 use_brain_council: bool = True):
        self.llm = llm_client or NanoGPTClient()
        self.use_brain_council = use_brain_council
        if self.use_brain_council:
            self.brain_council = BrainCouncil()
        else:
            self.brain_council = None

    def generate_response(self, user_input: str, context: Dict[str, Any],
                         debug: bool = False, world_map=None) -> tuple:
        """
        Generate response to user input

        Args:
            user_input: What the user said/did
            context: Current state context
            debug: Whether to show debug info
            world_map: WorldMap for location context

        Returns:
            Tuple of (response, council_decision or None)
        """
        try:
            council_decision = None

            # Use brain council if enabled
            if self.use_brain_council and self.brain_council:
                # Enhance context with location info
                if world_map:
                    context = self.brain_council.enhance_context_with_location(
                        context, world_map
                    )

                # Get council decision
                council_decision = self.brain_council.deliberate(
                    user_input, context, debug=debug
                )

                if debug:
                    debug_vis = self.brain_council.get_debate_visualization(council_decision)
                    logger.info(f"\n{debug_vis}")

                # Build prompt using council decision
                winning_vote = council_decision.winning_vote
                brain_context = {
                    'decision': winning_vote.decision,
                    'reasoning': winning_vote.reasoning,
                    'emotion': self.brain_council.decision_engine.get_dominant_emotion(
                        council_decision.all_votes
                    )
                }

                prompt = PromptBuilder.build_response_with_council(
                    user_input, context, brain_context
                )
            else:
                # Simple response without council
                prompt = PromptBuilder.build_simple_response_prompt(
                    user_input, context
                )

            if debug:
                logger.info(f"Final Prompt: {prompt}")

            # Generate response
            response = self.llm.generate(
                prompt,
                max_tokens=100,
                temperature=0.85
            )

            return (response or "*Eevee looks at you curiously* Vee?", council_decision)

        except Exception as e:
            logger.error(f"Error generating response: {e}", exc_info=True)
            return ("*Eevee tilts head* Vee? *seems confused*", None)

    def generate_greeting(self, time_since_last: float,
                         context: Dict[str, Any]) -> str:
        """
        Generate greeting based on time elapsed

        Args:
            time_since_last: Hours since last interaction
            context: Current state context

        Returns:
            Greeting message
        """
        state = context.get('physical_state', {})
        happiness = state.get('happiness', 50)

        if time_since_last < 0.1:  # Just saw them
            return "*Eevee looks up at you* Vee? *tilts head curiously*"

        elif time_since_last < 2:  # Within a couple hours
            return "*Eevee perks up* Vee! *tail wagging*"

        elif time_since_last < 12:  # Same day
            if happiness > 70:
                return "*Eevee bounds towards you excitedly* Veevee! *jumps up happily*"
            else:
                return "*Eevee walks over slowly* Vee... *nuzzles your hand*"

        elif time_since_last < 48:  # 1-2 days
            return "*Eevee SPRINTS towards you* VEE! VEEVEE! *tackles you with enthusiasm, licking your face*"

        else:  # Multiple days
            return "*Eevee stands frozen for a moment, ears perked up* ...VEE!! *RACES towards you at full speed, crying with joy* VEEVEE!! *nuzzles you desperately, tail wagging so hard their whole body shakes*"

    def describe_action(self, action: str, context: Dict[str, Any]) -> str:
        """
        Generate description of Eevee performing an action

        Args:
            action: Action being performed
            context: Current state context

        Returns:
            Action description
        """
        state = context.get('physical_state', {})
        energy = state.get('energy', 50)
        happiness = state.get('happiness', 50)

        # Modify action description based on state
        if action == "playing":
            if energy > 60 and happiness > 60:
                return "*Eevee runs in excited circles, pouncing on their own tail* Vee vee! *absolutely bursting with energy*"
            elif energy < 30:
                return "*Eevee tries to play but seems tired* Vee... *halfhearted bounce*"
            else:
                return "*Eevee plays happily* Veevee! *chasing leaves in the wind*"

        elif action == "resting":
            if energy < 30:
                return "*Eevee curls up into a tight ball* *soft breathing* *already dozing off*"
            else:
                return "*Eevee lies down comfortably* *watching you with sleepy eyes* Veee~"

        elif action == "exploring":
            if happiness > 70:
                return "*Eevee sniffs around excitedly* Vee! *discovering new scents and sights*"
            else:
                return "*Eevee explores cautiously* *ears twitching at every sound*"

        elif action == "eating":
            if state.get('hunger', 50) > 70:
                return "*Eevee devours the food eagerly* *munch munch* Vee! *so hungry*"
            else:
                return "*Eevee nibbles contentedly* *happy satisfied sounds*"

        else:
            return f"*Eevee {action}* Vee!"

    def interpret_mood(self, context: Dict[str, Any]) -> str:
        """
        Interpret and describe Eevee's current mood

        Args:
            context: Current state context

        Returns:
            Mood description
        """
        state = context.get('physical_state', {})
        hunger = state.get('hunger', 50)
        energy = state.get('energy', 50)
        happiness = state.get('happiness', 50)

        mood_parts = []

        # Happiness
        if happiness > 80:
            mood_parts.append("very happy and content")
        elif happiness > 60:
            mood_parts.append("cheerful")
        elif happiness > 40:
            mood_parts.append("calm")
        elif happiness > 20:
            mood_parts.append("a bit down")
        else:
            mood_parts.append("sad and lonely")

        # Energy
        if energy > 80:
            mood_parts.append("full of energy")
        elif energy < 30:
            mood_parts.append("quite tired")

        # Hunger
        if hunger > 70:
            mood_parts.append("very hungry")
        elif hunger > 50:
            mood_parts.append("getting hungry")

        mood = "Eevee seems " + ", ".join(mood_parts) + "."
        return mood
