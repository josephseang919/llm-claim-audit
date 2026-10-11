"""ThresholdPolicy: turns a stream of verification results into a
pass / fail / alert decision, tracked over time via the AuditStore.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from llm_claim_audit.verifier import VerificationResult


class AuditOutcome(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    ALERT = "alert"  # e.g. agreement rate degrading but not yet below hard fail


@dataclass
class ThresholdPolicy:
    """Decides audit outcome from a batch of verification results.

    Attributes:
        min_agreement_rate: fraction of claims that must be grounded to pass.
        alert_agreement_rate: fraction below which to raise ALERT
            (but above min_agreement_rate, i.e. min_agreement_rate <=
            alert_agreement_rate).
        window: how many past campaign results to consider alongside the
            current one when deciding (e.g. rolling trend detection).
    """

    min_agreement_rate: float
    alert_agreement_rate: float | None = None
    window: int = 1

    def evaluate(self, results: Sequence[VerificationResult]) -> AuditOutcome:
        """Compute the outcome for one audit campaign's results.

        TODO: compute agreement rate = grounded / total, compare against
        min_agreement_rate and alert_agreement_rate, optionally factoring
        in the rolling `window` via the AuditStore's history.
        """
        raise NotImplementedError
