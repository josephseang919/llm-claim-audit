# llm-claim-audit

A small, long-running quality framework for projects that ship LLM-extracted
claims and need a defensible audit trail — without building the verifier
scaffolding themselves.

## Mission

Any project that has an LLM extract claims from source material (narratives
from a corpus, structured data from digitized artifacts, summaries of
records) eventually needs to answer: *how do we know these claims are still
grounded, and how do we track that over time?*

`llm-claim-audit` is the framework half of that answer: a **sampler** +
**sidecar SQLite store** + **threshold policy**. It ships no built-in
verifier prompts or claim shapes — those are consumer-supplied, because
what counts as a "claim" and how to check it is domain-specific. What the
package gives you is the reusable plumbing around that: sampling a
population, running verification, recording results, and deciding
pass/fail/alert against a threshold, campaign after campaign.

This pattern originated in [WXYC](https://wxyc.org)'s `semantic_index`
project auditing LLM-extracted DJ-show narratives against a source review
corpus, and generalized cleanly to other claim shapes (vinyl-scan
extractions, flowsheet-digitization reconciliation outputs). This package
is v0 of that generalized framework.

## Install

```bash
pip install llm-claim-audit
```

## Quick start

```python
from llm_claim_audit import Sampler, LLMVerifier, ThresholdPolicy, AuditStore

sampler = Sampler(population_fn=my_narrative_source, sample_size=25)

verifier = LLMVerifier(
    client=my_openai_compatible_client,
    model="claude-...",
    prompt_template=my_verifier_prompt,
    parse_response=my_response_parser,
)

policy = ThresholdPolicy(min_agreement_rate=0.85)
store = AuditStore(db_path="audit.sqlite3")
```

Or run a one-shot campaign from the CLI:

```bash
llm-claim-audit run --config audit-campaign.toml
```

## What this is (and isn't)

**In scope for v0:** sampler, verifier protocol + reference OpenAI-compatible
`LLMVerifier`, threshold policy, sidecar SQLite store, one-shot CLI runner.

**Out of scope for v0:** a TS port, built-in verifier prompts for specific
claim shapes, hosted dashboards or telemetry (local SQLite is the only
persistence).

## Comparison to adjacent tools

No existing tool directly targets this "long-running sampled audit trail
for LLM-extracted claims against source material" niche. The closest
adjacent projects, and why they're not a direct substitute:

| Tool | Focus | Why it's not a substitute |
|---|---|---|
| [LangChain evaluation](https://python.langchain.com/) | Ad hoc eval chains for LLM app development | Built for one-off eval runs during development, not a persistent sampled audit trail over a live claim-producing pipeline |
| [DeepEval](https://github.com/confident-ai/deepeval) | LLM output testing framework (unit-test style) | Test-suite oriented; no built-in sidecar persistence or rolling threshold policy across campaigns |
| [Ragas](https://github.com/explodinggradients/ragas) | RAG-specific evaluation metrics | Scoped to RAG retrieval/generation quality metrics, not general claim-vs-source grounding audits |

## License

Apache 2.0. See `LICENSE`.
