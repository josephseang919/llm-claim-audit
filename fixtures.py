"""Fake stand-ins for testing the CLI without a real AI API."""

from llm_claim_audit.verifier import VerificationResult


def get_claims():
    return ["The sky is blue.", "Cats can fly.", "Water boils at 100C."]


class FakeClient:
    class chat:
        class completions:
            @staticmethod
            def create(model, messages):
                return messages[0]["content"]

def build_prompt(claim, source):
    return claim


def parse_response(response, claim):
    grounded = "fly" not in response
    return VerificationResult(claim=claim, grounded=grounded, confidence=1.0, rationale="fake check")