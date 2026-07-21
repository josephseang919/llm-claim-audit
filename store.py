"""AuditStore: sidecar SQLite persistence for audit campaigns and results.

Local-only, no hosted dashboards or telemetry (out of scope for v0 per the
extract-llm-claim-audit-v0 epic).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from llm_claim_audit.threshold import AuditOutcome
from llm_claim_audit.verifier import VerificationResult


@dataclass
class AuditStore:
    """SQLite-backed store for audit campaign history.

    Attributes:
        db_path: path to the sqlite file. Created if it doesn't exist.
    """

    db_path: Path

    def __post_init__(self) -> None:
        # TODO: open connection, run schema migration if the db is new.
        # Suggested schema:
        #   campaigns(id, started_at, sample_size, outcome, agreement_rate)
        #   results(id, campaign_id, claim_repr, grounded, confidence, rationale)
        raise NotImplementedError

    def record_campaign(
        self, results: Sequence[VerificationResult], outcome: AuditOutcome
    ) -> int:
        """Persist one audit campaign and its results. Returns campaign id.

        TODO: implement insert.
        """
        raise NotImplementedError

    def history(self, limit: int = 20) -> Sequence[dict]:
        """Return the most recent campaigns, most recent first.

        TODO: implement query.
        """
        raise NotImplementedError
