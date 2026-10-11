"""llm-claim-audit: a long-running quality sampler for LLM-extracted claims.

Public API:
    Sampler         - selects which claims/narratives get audited
    Verifier        - protocol any verifier (LLM-backed or otherwise) implements
    LLMVerifier     - reference verifier calling an OpenAI-compatible chat endpoint
    ThresholdPolicy - decides pass/fail/alert based on agreement rate over time
    AuditStore      - sidecar SQLite persistence for audit runs and results
"""

from llm_claim_audit.sampler import Sampler
from llm_claim_audit.verifier import Verifier, LLMVerifier
from llm_claim_audit.threshold import ThresholdPolicy
from llm_claim_audit.store import AuditStore

__all__ = [
    "Sampler",
    "Verifier",
    "LLMVerifier",
    "ThresholdPolicy",
    "AuditStore",
]

__version__ = "0.1.0"
