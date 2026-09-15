"""Verifier protocol + reference LLM-backed implementation.

`Verifier` is intentionally minimal so consumers can implement non-LLM
verifiers (rule-based, human-in-the-loop, etc.) if they want to.

`LLMVerifier` is the reference implementation: it calls any
OpenAI-compatible chat completions endpoint. The client and prompt
template are consumer-supplied — this class never hardcodes a claim shape
or a specific provider.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass
class VerificationResult:
    """Outcome of verifying a single claim against its source material."""

    claim: Any
    grounded: bool
    confidence: float | None = None
    rationale: str | None = None
    raw_response: Any = None


@runtime_checkable
class Verifier(Protocol):
    """Anything that can check a claim against source material implements this."""

    def verify(self, claim: Any, source: Any) -> VerificationResult:
        ...


@dataclass
class LLMVerifier:
    """Reference Verifier backed by an OpenAI-compatible chat completions client.

    Attributes:
        client: a pre-configured OpenAI-compatible client (OpenAI, Anthropic,
            Groq SDK, etc. — anything exposing a compatible chat completions
            call). Supplied by the consumer.
        model: model identifier to pass to the client.
        prompt_template: callable that renders (claim, source) into the
            verifier prompt. Consumer-supplied — the package ships no
            built-in prompts for specific claim shapes.
        parse_response: callable that turns the raw model response into a
            VerificationResult.
    """

    client: Any
    model: str
    prompt_template: Any  # Callable[[Any, Any], str]
    parse_response: Any  # Callable[[Any, Any], VerificationResult]

    def verify(self, claim: Any, source: Any) -> VerificationResult:
        """Call the configured LLM to verify `claim` against `source`."""
        prompt = self.prompt_template(claim, source)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return self.parse_response(response, claim)

    

