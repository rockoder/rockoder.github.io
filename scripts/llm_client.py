#!/usr/bin/env python3
"""
Unified LLM client for Beyond the Code content pipeline.
Supports multiple providers with automatic fallback.
"""

import os
import subprocess
import tempfile
import yaml
from pathlib import Path
from typing import Optional
from abc import ABC, abstractmethod

# One-shot CLI calls shouldn't hang forever; generous enough for slow drafts.
CLI_TIMEOUT_SECONDS = 600


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text from a prompt."""
        pass


class ClaudeCodeProvider(LLMProvider):
    """Writes via the local Claude Code CLI (subscription-based, no per-token billing)."""

    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        cmd = [
            "claude", "-p", prompt,
            "--output-format", "text",
            "--model", self.model,
            "--tools", "",  # pure text completion: no Bash/Edit/file access
        ]
        if system_prompt:
            cmd += ["--system-prompt", system_prompt]

        # This machine has both a work and a personal Claude Code subscription.
        # Force the personal one explicitly (mirrors the `cldp` shell function) —
        # never rely on whatever CLAUDE_CONFIG_DIR happens to be ambient.
        env = {**os.environ, "CLAUDE_CONFIG_DIR": os.path.expanduser("~/.claude-personal")}

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=CLI_TIMEOUT_SECONDS,
            stdin=subprocess.DEVNULL,
            env=env,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"claude CLI failed (exit {result.returncode}): "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )
        return result.stdout.strip()


class CodexProvider(LLMProvider):
    """Critiques via the local Codex CLI (free ChatGPT plan, no per-token billing)."""

    def __init__(self, model: Optional[str] = None):
        self.model = model  # None -> let `codex exec` use its own default

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tf:
            out_path = tf.name

        try:
            cmd = [
                "codex", "exec", full_prompt,
                "--sandbox", "read-only",
                "--skip-git-repo-check",
                "-o", out_path,
            ]
            if self.model:
                cmd += ["-m", self.model]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=CLI_TIMEOUT_SECONDS,
                stdin=subprocess.DEVNULL,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"codex CLI failed (exit {result.returncode}): "
                    f"{result.stderr.strip() or result.stdout.strip()}"
                )
            with open(out_path, "r") as f:
                return f.read().strip()
        finally:
            os.unlink(out_path)


class LLMClient:
    """
    Unified LLM client that routes requests to configured providers.

    Usage:
        client = LLMClient()
        result = client.generate("topic_extraction", "Extract themes from: ...")
    """

    PROVIDER_CLASSES = {
        "claude_code": ClaudeCodeProvider,
        "codex": CodexProvider,
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

    def _get_provider(self, provider_name: str, model: Optional[str]) -> LLMProvider:
        """Get or create a provider instance."""
        key = f"{provider_name}:{model}"
        if key not in self._providers:
            provider_class = self.PROVIDER_CLASSES.get(provider_name)
            if not provider_class:
                raise ValueError(f"Unknown provider: {provider_name}")

            self._providers[key] = provider_class(model=model)
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
        primary_provider = model_config["provider"]
        primary_model = model_config.get("model")  # None -> provider's own default
        print(f"  [LLM] {task} → {primary_provider}/{primary_model or 'default'}", end="", flush=True)
        try:
            provider = self._get_provider(primary_provider, primary_model)
            result = provider.generate(prompt, system_prompt)
            print(" ✓")
            return result
        except Exception as primary_error:
            print(" ✗")
            # Try fallback if configured
            fallback = model_config.get("fallback")
            if fallback:
                fallback_provider = fallback["provider"]
                fallback_model = fallback["model"]
                print(f"  [LLM] Fallback: {primary_provider}/{primary_model} failed → trying {fallback_provider}/{fallback_model}")
                print(f"        Error: {primary_error}")
                print(f"  [LLM] {task} → {fallback_provider}/{fallback_model}", end="", flush=True)
                try:
                    provider = self._get_provider(fallback_provider, fallback_model)
                    result = provider.generate(prompt, system_prompt)
                    print(" ✓")
                    return result
                except Exception as fallback_error:
                    print(" ✗")
                    raise Exception(
                        f"Both providers failed for {task}.\n"
                        f"  Primary ({primary_provider}/{primary_model}): {primary_error}\n"
                        f"  Fallback ({fallback_provider}/{fallback_model}): {fallback_error}"
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
