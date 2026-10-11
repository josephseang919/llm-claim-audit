"""AuditStore: sidecar SQLite persistence for audit campaigns and results.

Local-only, no hosted dashboards or telemetry (out of scope for v0 per the
extract-llm-claim-audit-v0 epic).
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone


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
        self.db_path = Path(self.db_path) 
        self._conn = sqlite3.connect(self.db_path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                sample_size INTEGER NOT NULL,
                outcome TEXT NOT NULL,
                agreement_rate REAL NOT NULL
            )
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                claim_repr TEXT NOT NULL,
                grounded INTEGER NOT NULL,
                confidence REAL,
                rationale TEXT,
                FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
            )
            """
        )
        self._conn.commit()

    def record_campaign(
        self, results: Sequence[VerificationResult], outcome: AuditOutcome
    ) -> int:
        """Persist one audit campaign and its results. Returns campaign id."""
        total = len(results)
        grounded = sum(1 for r in results if r.grounded)
        agreement_rate = grounded / total if total > 0 else 0.0

        cursor = self._conn.execute(
            """
            INSERT INTO campaigns (started_at, sample_size, outcome, agreement_rate)
            VALUES (?, ?, ?, ?)
            """,
            (datetime.now(timezone.utc).isoformat(), total, outcome.value, agreement_rate),
        )
        campaign_id = cursor.lastrowid

        for r in results:
            self._conn.execute(
            """
            INSERT INTO results (campaign_id, claim_repr, grounded, confidence, rationale)
            VALUES (?, ?, ?, ?, ?)
            """,
            (campaign_id, repr(r.claim), int(r.grounded), r.confidence, r.rationale)
            )

            self._conn.commit()
            return campaign_id


    def history(self, limit: int = 20) -> Sequence[dict]:
        """Return the most recent campaigns, most recent first."""
        cursor = self._conn.execute(
            """
            SELECT id, started_at, sample_size, outcome, agreement_rate
            FROM campaigns
            ORDER BY started_at DESC
            LIMIT ?
            """,
            (limit,),
        )
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
