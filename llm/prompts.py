"""
Prompt Templates for EeveeLLM
Manages prompt construction for different contexts
"""
from typing import Dict, Any, List, Optional


class PromptBuilder:
    """Builds prompts for different LLM interactions"""

    @staticmethod
    def build_brain_region_prompt(region_name: str, context: Dict[str, Any],
                                   situation: str) -> str:
        """
        Build prompt for a specific brain region

        Args:
            region_name: Name of brain region
            context: Current state context
            situation: Current situation/stimulus

        Returns:
            Formatted prompt
        """
        state = context.get('physical_state', {})
        location = context.get('location', 'unknown')
        memories = context.get('recent_memories', [])

        memory_str = ""
        if memories:
            memory_str = "Recent memories:\n"
            for memory in memories[:3]:
                memory_str += f"- {memory}\n"

        prompt = f"""You are simulating Eevee's {region_name} in a brain council decision-making system.

Context:
- Eevee's current state: Hunger={state.get('hunger', 50)}/100, Energy={state.get('energy', 50)}/100, Happiness={state.get('happiness', 50)}/100
- Location: {location}
{memory_str}
Situation: {situation}

As the {region_name}, analyze this situation from your perspective and propose a response.
Respond in first-person as this brain region, explaining your reasoning.

{PromptBuilder._get_region_role(region_name)}

Keep your response concise (2-3 sentences) and focused on your region's concerns."""

        return prompt

    @staticmethod
    def _get_region_role(region_name: str) -> str:
        """Get role description for brain region"""
        roles = {
            "Prefrontal Cortex": "Focus on logic, planning, and long-term consequences. Consider the trainer relationship and goal-directed behavior.",
            "Amygdala": "Focus on emotions and survival. Process fear, excitement, joy. Assess threats and safety.",
            "Hippocampus": "Focus on memories and patterns. Recall relevant past experiences. Provide context from history.",
            "Hypothalamus": "Focus on physical needs and drives. Monitor hunger, thirst, energy, comfort. Generate motivation for basic needs.",
            "Cerebellum": "Focus on instincts and coordination. Consider species-specific Eevee behaviors and automatic responses."
        }
        return roles.get(region_name, "Provide your perspective on this situation.")

    @staticmethod
    def build_response_synthesis_prompt(brain_votes: Dict[str, str],
                                        winning_decision: str,
                                        context: Dict[str, Any]) -> str:
        """
        Build prompt for synthesizing final response

        Args:
            brain_votes: Dictionary of brain region votes
            winning_decision: The winning decision
            context: Current state context

        Returns:
            Formatted prompt
        """
        votes_str = "Brain council perspectives:\n"
        for region, vote in brain_votes.items():
            votes_str += f"- {region}: {vote}\n"

        state = context.get('physical_state', {})
        personality = context.get('personality', {})

        personality_str = ""
        if personality:
            traits = []
            for trait, value in personality.items():
                if value >= 7:
                    traits.append(trait)
            if traits:
                personality_str = f"Dominant traits: {', '.join(traits)}"

        prompt = f"""You are Eevee, a curious and loyal Pokemon companion.

{votes_str}

Winning decision: {winning_decision}

Current state:
- Happiness: {state.get('happiness', 50)}/100
- Energy: {state.get('energy', 50)}/100
- Hunger: {state.get('hunger', 50)}/100
{personality_str}

Generate Eevee's response as natural dialogue and action.
- Use Pokemon sounds ("Vee!", "Veevee!", etc.)
- Include body language and physical actions in *asterisks*
- Keep it authentic to a curious, energetic Eevee
- Show emotion through actions and sounds
- Keep response to 2-4 sentences

Response:"""

        return prompt

    @staticmethod
    def build_response_with_council(user_input: str, context: Dict[str, Any],
                                    brain_context: Dict[str, Any]) -> str:
        """
        Build response prompt using brain council decision

        Args:
            user_input: User's input
            context: Current state context
            brain_context: Brain council decision context

        Returns:
            Formatted prompt
        """
        state = context.get('physical_state', {})
        decision = brain_context.get('decision', 'neutral')
        reasoning = brain_context.get('reasoning', '')
        emotion = brain_context.get('emotion', 'calm')

        prompt = f"""You are Eevee, a curious and loyal Pokemon companion.

Situation: "{user_input}"

Your internal decision: {decision}
Your reasoning: {reasoning}
Your emotional state: {emotion}

Current state:
- Happiness: {state.get('happiness', 50)}/100
- Energy: {state.get('energy', 50)}/100
- Hunger: {state.get('hunger', 50)}/100

Based on your internal decision and emotional state, respond naturally:
- Use Pokemon sounds ("Vee!", "Veevee!", "Eevee!", etc.)
- Include body language in *asterisks* (e.g., *tail wagging*, *ears droop*)
- Show the emotion: {emotion}
- Reflect the decision: {decision}
- Keep response to 2-4 sentences
- Be authentic and genuine

Eevee's response:"""

        return prompt

    @staticmethod
    def build_simple_response_prompt(user_input: str,
                                     context: Dict[str, Any]) -> str:
        """
        Build simple response prompt (without brain council)

        Args:
            user_input: User's input
            context: Current state context

        Returns:
            Formatted prompt
        """
        state = context.get('physical_state', {})
        location = context.get('location', 'unknown')
        relationship = context.get('relationship', {})

        prompt = f"""You are Eevee, a curious and loyal Pokemon companion.

Current situation:
- Location: {location}
- Happiness: {state.get('happiness', 50)}/100
- Energy: {state.get('energy', 50)}/100
- Trust in trainer: {relationship.get('trust', 50)}/100

User says: "{user_input}"

Respond as Eevee would:
- Use Pokemon sounds ("Vee!", "Veevee!", "Eevee!", etc.)
- Include body language in *asterisks* (e.g., *tail wagging*, *perks up*)
- Show genuine emotion and personality
- React authentically based on current state
- Keep response to 2-4 sentences

Eevee's response:"""

        return prompt

    @staticmethod
    def build_activity_generation_prompt(hours_passed: int,
                                        current_state: Dict[str, Any]) -> str:
        """
        Build prompt for generating autonomous activities

        Args:
            hours_passed: Hours since last interaction
            current_state: Eevee's current state

        Returns:
            Formatted prompt
        """
        state = current_state.get('physical_state', {})
        location = current_state.get('location', 'unknown')

        prompt = f"""Generate a realistic timeline of activities for Eevee over the past {hours_passed} hours.

Starting state:
- Location: {location}
- Hunger: {state.get('hunger', 50)}/100
- Energy: {state.get('energy', 50)}/100
- Happiness: {state.get('happiness', 50)}/100

Generate {min(hours_passed // 2, 10)} activities that Eevee would naturally do:
- Needs-based activities (eating, sleeping, exploring)
- Emotional moments (missing trainer, feeling lonely, finding joy)
- Random encounters or discoveries
- Natural Pokemon behaviors

Format each activity as:
[Time offset]h: [Brief activity description with emotional note]

Activities:"""

        return prompt

    @staticmethod
    def build_memory_summary_prompt(interaction: str,
                                   emotional_context: str) -> str:
        """
        Build prompt for summarizing memory

        Args:
            interaction: Description of interaction
            emotional_context: Emotional context

        Returns:
            Formatted prompt
        """
        prompt = f"""Summarize this memory from Eevee's perspective.

Interaction: {interaction}
Emotional state: {emotional_context}

Create a brief, first-person memory (1 sentence) that captures the essence and emotion.

Memory:"""

        return prompt

    @staticmethod
    def build_context_dict(eevee_state, personality: Optional[Any] = None,
                          memories: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Build context dictionary from state objects

        Args:
            eevee_state: EeveeState object
            personality: Personality object
            memories: List of recent memories

        Returns:
            Context dictionary
        """
        context = eevee_state.to_dict()

        if personality:
            context['personality'] = personality.to_dict()

        if memories:
            context['recent_memories'] = memories

        return context
