#!/usr/bin/env python3
"""
Unified LLM client for Beyond the Code content pipeline.
Supports multiple providers with automatic fallback.
"""

import os
import yaml
from pathlib import Path
from typing import Optional
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text from a prompt."""
        pass


class AnthropicProvider(LLMProvider):
    """Claude API provider."""

    def __init__(self, model: str, max_tokens: int = 4096, temperature: float = 0.7):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = None

    @property
    def client(self):
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.Anthropic()
            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
        return self._client

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": messages,
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text


class GeminiProvider(LLMProvider):
    """Google Gemini API provider."""

    def __init__(self, model: str, max_tokens: int = 4096, temperature: float = 0.7):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = None

    @property
    def client(self):
        if self._client is None:
            try:
                import google.generativeai as genai
                api_key = os.environ.get("GOOGLE_API_KEY")
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY environment variable not set")
                genai.configure(api_key=api_key)
                self._client = genai.GenerativeModel(self.model)
            except ImportError:
                raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
        return self._client

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = self.client.generate_content(
            full_prompt,
            generation_config={
                "max_output_tokens": self.max_tokens,
                "temperature": self.temperature,
            }
        )
        return response.text


class GroqProvider(LLMProvider):
    """Groq API provider for fast Llama inference."""

    def __init__(self, model: str, max_tokens: int = 4096, temperature: float = 0.7):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = None

    @property
    def client(self):
        if self._client is None:
            try:
                from groq import Groq
                self._client = Groq()
            except ImportError:
                raise ImportError("groq package not installed. Run: pip install groq")
        return self._client

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message.content


class OpenAIProvider(LLMProvider):
    """OpenAI API provider (GPT-4, GPT-4o, etc.)."""

    def __init__(self, model: str, max_tokens: int = 4096, temperature: float = 0.7):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = None

    @property
    def client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI()
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")
        return self._client

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message.content


class LLMClient:
    """
    Unified LLM client that routes requests to configured providers.

    Usage:
        client = LLMClient()
        result = client.generate("topic_extraction", "Extract themes from: ...")
    """

    PROVIDER_CLASSES = {
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
        "groq": GroqProvider,
        "openai": OpenAIProvider,
    }

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # Default to config/models.yaml relative to this script
            script_dir = Path(__file__).parent.parent
            config_path = script_dir / "config" / "models.yaml"

        self.config = self._load_config(config_path)
        self._providers = {}

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def _get_provider(self, provider_name: str, model: str) -> LLMProvider:
        """Get or create a provider instance."""
        key = f"{provider_name}:{model}"
        if key not in self._providers:
            provider_class = self.PROVIDER_CLASSES.get(provider_name)
            if not provider_class:
                raise ValueError(f"Unknown provider: {provider_name}")

            provider_settings = self.config.get("providers", {}).get(provider_name, {})
            self._providers[key] = provider_class(
                model=model,
                max_tokens=provider_settings.get("max_tokens", 4096),
                temperature=provider_settings.get("temperature", 0.7),
            )
        return self._providers[key]

    def generate(
        self,
        task: str,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate text for a specific task using the configured provider.

        Args:
            task: Task name (e.g., "topic_extraction", "draft_writing")
            prompt: The user prompt to send
            system_prompt: Optional system prompt for context

        Returns:
            Generated text response

        Raises:
            ValueError: If task is not configured
            Exception: If both primary and fallback providers fail
        """
        model_config = self.config.get("models", {}).get(task)
        if not model_config:
            raise ValueError(f"No configuration found for task: {task}")

        # Try primary provider
        try:
            provider = self._get_provider(
                model_config["provider"],
                model_config["model"]
            )
            return provider.generate(prompt, system_prompt)
        except Exception as primary_error:
            # Try fallback if configured
            fallback = model_config.get("fallback")
            if fallback:
                print(f"Primary provider failed for {task}, trying fallback: {primary_error}")
                try:
                    provider = self._get_provider(
                        fallback["provider"],
                        fallback["model"]
                    )
                    return provider.generate(prompt, system_prompt)
                except Exception as fallback_error:
                    raise Exception(
                        f"Both primary and fallback failed for {task}. "
                        f"Primary: {primary_error}, Fallback: {fallback_error}"
                    )
            raise


# Convenience function for simple usage
_default_client = None


def generate(task: str, prompt: str, system_prompt: Optional[str] = None) -> str:
    """
    Convenience function for generating text without explicitly creating a client.

    Args:
        task: Task name from config (e.g., "topic_extraction")
        prompt: The prompt to send
        system_prompt: Optional system prompt

    Returns:
        Generated text
    """
    global _default_client
    if _default_client is None:
        _default_client = LLMClient()
    return _default_client.generate(task, prompt, system_prompt)


if __name__ == "__main__":
    # Simple test
    import sys

    if len(sys.argv) < 3:
        print("Usage: python llm_client.py <task> <prompt>")
        print("Example: python llm_client.py topic_extraction 'What are the main themes here?'")
        sys.exit(1)

    task = sys.argv[1]
    prompt = sys.argv[2]

    try:
        result = generate(task, prompt)
        print(f"Response:\n{result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
