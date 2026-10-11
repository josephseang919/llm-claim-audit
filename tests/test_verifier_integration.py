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
from openai import OpenAI

from llm_claim_audit import LLMVerifier
from llm_claim_audit.verifier import VerificationResult

def _prompt_templete(claim, source):
    return (
        f"Source material: {source}\n\n"
        f:"Claim: {claim}\n\n"
        "Does the source material support this claim? "
        "Answer with exactly one word: YES or NO."
    )

def _parse_response(response, claim):
    text = response.choices[0].message.content.strip().upper()
    grounded = text.startswith("YES") #returns true if claim is grounded 
    return VerificationResult(claim=claim, grounded=grounded, raw_response=response) #makes an instant of class from verifier

@pytest.mark.integration # Run with: pytest -m integration
@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="no Anthropic key") #conditional skip if no key is found in env
def test_llm_verifier_against_anthropic():
    client = OpenAI(
        api_key = os.environ["ANTHROPIC_API_KEY"],
        base_url = "https://api.anthropic.com/v1/",
    )
    verifier = LLMVerifier( #builds verifier object
        client = client,
        model = "claude-sonnet-4-6",
        prompt_template = _prompt_templete,
        parse_response = _parse_response,
    )

    grounded_result = verifier.verify( #calls LLMVerifier.verify()
        claim = "The sky is blue during the day",
        source = "The sky appears blue due to Rayleigh scattering of sunlight.",   
    )
    assert grounded_result.grounded is True #if AI says yes, grounded is true

    fabricated_result = verifier.verify(
        claim = "The sky is purple at noon.",
        source = "The sky appears blue due to Rayleigh scattering of sunlight.",
    )
    assert fabricated_result.grounded is False

@pytest.mark.integration 
@pytest.mark.skipif(not os.environ.get("GROQ_API_KEY"), reason="no Groq key")
def test_llm_verifier_against_groq():
    client = OpenAI(
        api_key = os.environ["GROQ_API_KEY"],
        base_url = "https://api.groq.com/openai/v1",
    )
    verifier = LLMVerifier(
        client = client,
        model = "llama-3.3-70b-versatile",
        prompt_template = _prompt_templete,
        parse_response = _parse_response,
    )

    grounded_result = verifier.verify(
        claim = "The sky is blue during the day",
        source = "The sky appears blue due to Rayleigh scattering of sunlight.",   
    )
    assert grounded_result.grounded is True

    fabricated_result = verifier.verify(
        claim = "The sky is purple at noon.",
        source = "The sky appears blue due to Rayleigh scattering of sunlight.",
    )
    assert fabricated_result.grounded is False
