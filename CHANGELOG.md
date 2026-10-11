# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- `Sampler` with seedable random sampling; handles populations smaller than the sample size.
- `Verifier` protocol and reference `LLMVerifier` for OpenAI-compatible chat clients.
- `ThresholdPolicy` returning PASS, ALERT, or FAIL from a batch's agreement rate.
- `AuditStore`, a sidecar SQLite store for campaigns and per-claim results.
- CLI: `llm-claim-audit run --config <toml>` runs one audit campaign end to end.
- Unit tests for the sampler and threshold policy; integration tests for
  `LLMVerifier` (marked `integration`, skipped by default, need provider API keys).

### Known limitations
- Only the `"random"` sampling strategy is implemented.
- `ThresholdPolicy` judges each campaign on its own; the `window` setting is
  accepted but not used yet, so rolling trend detection is not in v0.
- The CLI passes no separate `source` to the verifier.

## [0.1.0] - Unreleased
- First public release (pending PyPI Trusted Publishing setup).
