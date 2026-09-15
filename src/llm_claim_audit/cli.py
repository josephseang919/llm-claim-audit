"""CLI entry point: `llm-claim-audit run --config config.toml`.

Runs a one-shot audit campaign from a TOML config describing the sampler,
verifier, and threshold policy to use.
"""

from __future__ import annotations

import importlib
import argparse
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
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    sampler_cfg = config["sampler"]
    sampler = Sampler(
        
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        return run_campaign(args.config)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
