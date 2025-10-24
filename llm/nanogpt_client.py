"""
NanoGPT API Client
Handles communication with NanoGPT API for text generation
"""
import requests
from typing import Optional, Dict, Any
import logging

from config import Config

logger = logging.getLogger(__name__)


class NanoGPTClient:
    """Client for NanoGPT API interactions"""

    def __init__(self, api_key: Optional[str] = None,
                 endpoint: Optional[str] = None,
                 model: Optional[str] = None):
        """
        Initialize NanoGPT client

        Args:
            api_key: API key (defaults to Config.NANOGPT_API_KEY)
            endpoint: API endpoint (defaults to Config.NANOGPT_ENDPOINT)
            model: Model name (defaults to Config.NANOGPT_MODEL)
        """
        self.api_key = api_key or Config.NANOGPT_API_KEY
        self.endpoint = endpoint or Config.NANOGPT_ENDPOINT
        self.model = model or Config.NANOGPT_MODEL

        if not self.api_key:
            logger.warning("NanoGPT API key not set. Using fallback mode.")
            self.fallback_mode = True
        else:
            self.fallback_mode = False

    def generate(self, prompt: str,
                 max_tokens: Optional[int] = None,
                 temperature: Optional[float] = None,
                 stop_sequences: Optional[list] = None) -> str:
        """
        Generate text from prompt using OpenAI-compatible chat completions

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stop_sequences: Sequences that stop generation

        Returns:
            Generated text
        """
        if self.fallback_mode:
            return self._fallback_generate(prompt)

        max_tokens = max_tokens or Config.NANOGPT_MAX_TOKENS
        temperature = temperature or Config.NANOGPT_TEMPERATURE

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # NanoGPT uses OpenAI-compatible chat completions format
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature
            }

            if stop_sequences:
                payload["stop"] = stop_sequences

            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            # Extract generated text from OpenAI-compatible response
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                # Handle both 'message' (chat) and 'text' (completion) formats
                if "message" in choice:
                    return choice["message"].get("content", "").strip()
                elif "text" in choice:
                    return choice["text"].strip()
            elif "text" in data:
                return data["text"].strip()

            logger.error(f"Unexpected API response format: {data}")
            return self._fallback_generate(prompt)

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return self._fallback_generate(prompt)
        except Exception as e:
            logger.error(f"Unexpected error in generate: {e}")
            return self._fallback_generate(prompt)

    def _fallback_generate(self, prompt: str) -> str:
        """
        Fallback text generation when API is unavailable
        Uses simple template-based responses
        """
        logger.info("Using fallback response generation")

        # Simple pattern matching for basic interactions
        prompt_lower = prompt.lower()

        if "greeting" in prompt_lower or "hello" in prompt_lower or "hey" in prompt_lower:
            return "*Eevee perks up excitedly* Vee! Veevee! *bounces happily*"

        elif "explore" in prompt_lower or "adventure" in prompt_lower:
            return "*Eevee's ears perk up with interest* Vee? *looks at you curiously, tail wagging*"

        elif "play" in prompt_lower or "game" in prompt_lower:
            return "*Eevee runs in excited circles* Vee vee! *pounces playfully*"

        elif "food" in prompt_lower or "hungry" in prompt_lower or "berry" in prompt_lower:
            return "*Eevee's nose twitches* Vee! *looks hopefully at you*"

        elif "pet" in prompt_lower or "cuddle" in prompt_lower or "hug" in prompt_lower:
            return "*Eevee nuzzles against you affectionately* Veeee~ *purrs contentedly*"

        elif "scared" in prompt_lower or "afraid" in prompt_lower:
            return "*Eevee's ears droop, tail between legs* Vee... *huddles close to you for safety*"

        elif "tired" in prompt_lower or "sleep" in prompt_lower or "nap" in prompt_lower:
            return "*Eevee yawns widely* Veee... *curls up in a cozy ball*"

        elif "happy" in prompt_lower or "joy" in prompt_lower:
            return "*Eevee bounces energetically* Vee vee vee! *tail wagging so hard entire body wiggles*"

        elif "memory" in prompt_lower or "remember" in prompt_lower:
            return "*Eevee tilts head thoughtfully* Vee... *looks distant, as if remembering*"

        else:
            # Generic response
            return "*Eevee looks at you attentively* Vee? *tilts head curiously*"

    def generate_with_context(self, system_prompt: str, user_prompt: str,
                             context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate with system and user prompts

        Args:
            system_prompt: System-level instructions
            user_prompt: User input
            context: Additional context information

        Returns:
            Generated response
        """
        # Combine prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        if context:
            context_str = "\nContext:\n"
            for key, value in context.items():
                context_str += f"- {key}: {value}\n"
            full_prompt = f"{system_prompt}{context_str}\n{user_prompt}"

        return self.generate(full_prompt)

    def test_connection(self) -> bool:
        """Test if API is accessible"""
        if self.fallback_mode:
            return False

        try:
            response = self.generate("Test", max_tokens=5)
            return bool(response)
        except Exception:
            return False

    def __repr__(self):
        status = "Fallback Mode" if self.fallback_mode else "API Mode"
        return f"<NanoGPTClient: {status}, Model={self.model}>"
