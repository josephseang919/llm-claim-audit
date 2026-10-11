"""CLI entry point: `llm-claim-audit run --config config.toml`.

Runs a one-shot audit campaign from a TOML config describing the sampler,
verifier, and threshold policy to use.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-claim-audit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a one-shot audit campaign")
    run_parser.add_argument(
        "--config", type=Path, required=True, help="Path to campaign TOML config"
    )

    return parser


def run_campaign(config_path: Path) -> int:
    """Load config, build Sampler/Verifier/ThresholdPolicy, run, persist, report.

    TODO:
      1. Parse TOML config (sampler settings, verifier/client settings,
         threshold settings, sqlite path).
      2. Construct Sampler, LLMVerifier (or consumer-specified verifier),
         ThresholdPolicy, AuditStore.
      3. sample = Sampler.sample(); results = [verifier.verify(c, s) for ...]
      4. outcome = policy.evaluate(results); store.record_campaign(...)
      5. Print a summary; return non-zero exit code on FAIL/ALERT.
    """
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        return run_campaign(args.config)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
