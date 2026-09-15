"""Unit tests for ThresholdPolicy. No network calls — pure logic."""

import pytest

from llm_claim_audit import ThresholdPolicy
from llm_claim_audit.threshold import AuditOutcome
from llm_claim_audit.verifier import VerificationResult


def _results(grounded_flags):
    return [VerificationResult(claim=i, grounded=g) for i, g in enumerate(grounded_flags)]


def test_all_grounded_passes():
    policy = ThresholdPolicy(min_agreement_rate=0.8)
    assert policy.evaluate(_results([True, True, True, True])) == AuditOutcome.PASS


def test_low_agreement_fails():
    policy = ThresholdPolicy(min_agreement_rate=0.8)
    assert policy.evaluate(_results([True, False, False, False])) == AuditOutcome.FAIL
