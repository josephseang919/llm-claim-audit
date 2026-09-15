# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Initial repo scaffold: `Sampler`, `Verifier`/`LLMVerifier`, `ThresholdPolicy`,
  `AuditStore` package skeleton.
- CLI entry point `llm-claim-audit run --config <toml>`.
- CI workflow with unit tests on push; integration tests (`-m integration`)
  deselected from default runs.

## [0.1.0] - Unreleased
- First public release (pending PyPI Trusted Publishing setup).
