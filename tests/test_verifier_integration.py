"""Integration tests for LLMVerifier against real OpenAI-compatible providers.

Marked `integration` — deselected from default CI runs (see pyproject.toml
`addopts = "-m 'not integration'"`). Run explicitly with:

    pytest -m integration

Requires provider API keys in the environment (e.g. ANTHROPIC_API_KEY,
GROQ_API_KEY). Acceptance criteria for the epic requires this to pass
against at least two providers.
"""

import os

import pytest

from llm_claim_audit import LLMVerifier


@pytest.mark.integration
@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="no Anthropic key")
def test_llm_verifier_against_anthropic():
    # TODO: construct an Anthropic-compatible client, build an LLMVerifier,
    # verify a known-grounded claim and a known-fabricated claim, assert
    # grounded is True/False respectively.
    pytest.skip("not yet implemented")


@pytest.mark.integration
@pytest.mark.skipif(not os.environ.get("GROQ_API_KEY"), reason="no Groq key")
def test_llm_verifier_against_groq():
    # TODO: same as above, against a Groq OpenAI-compatible client.
    pytest.skip("not yet implemented")
