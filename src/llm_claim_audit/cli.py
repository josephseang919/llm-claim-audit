"""CLI entry point: `llm-claim-audit run --config config.toml`.

Runs a one-shot audit campaign from a TOML config describing the sampler,
verifier, and threshold policy to use.
"""

from __future__ import annotations
from llm_claim_audit.sampler import Sampler
from llm_claim_audit.verifier import LLMVerifier
from llm_claim_audit.threshold import ThresholdPolicy, AuditOutcome
from llm_claim_audit.store import AuditStore

import importlib
import argparse
import tomllib
import sys
from pathlib import Path

def _load(dotted_path: str):
    """Import module.submodule:attribute and return the attribute"""
    module_path, _, attr_name = dotted_path.partition(":")
    module = importlib.import_module(module_path)
    return getattr(module, attr_name)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-claim-audit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a one-shot audit campaign")
    run_parser.add_argument(
        "--config", type=Path, required=True, help="Path to campaign TOML config"
    )

    return parser


def run_campaign(config_path: Path) -> int:
    """Load config, build Sampler/Verifier/ThresholdPolicy, run"""
    if str(Path.cwd()) not in sys.path:
        sys.path.insert(0, str(Path.cwd()))  # allow relative imports from cwd

    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    sampler_cfg = config["sampler"]
    sampler = Sampler(
        population_fn = _load(sampler_cfg["population"]),
        sample_size = sampler_cfg["sample_size"],
        strategy = sampler_cfg.get("strategy", "random"),
        rng_seed = sampler_cfg.get("rng_seed"),  
    )

    verifier_cfg = config["verifier"]
    verifier = LLMVerifier(
        client = _load(verifier_cfg["client"]),
        model = verifier_cfg["model"],
        prompt_template = _load(verifier_cfg["prompt_template"]),
        parse_response = _load(verifier_cfg["parse_response"]),
    )

    threshold_cfg = config["threshold"]
    policy = ThresholdPolicy(
        min_agreement_rate = threshold_cfg["min_agreement_rate"],
        alert_agreement_rate = threshold_cfg.get("alert_agreement_rate"),
)

    store = AuditStore(db_path = Path(config["store"]["db_path"]))

    claims = sampler.sample()
    results = [verifier.verify(claim, source = None) for claim in claims]
    outcome = policy.evaluate(results)
    campaign_id = store.record_campaign(results, outcome)

    grounded = sum(1 for r in results if r.grounded)
    print(f"Campaign #{campaign_id}: {grounded}/{len(results)} grounded -> {outcome.value.upper()}")

    return 0 if outcome == AuditOutcome.PASS else 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        return run_campaign(args.config)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
