# llm-claim-audit

A small, long-running quality framework for projects that ship LLM-extracted
claims and need a defensible audit trail — without building the verifier
scaffolding themselves.

## Mission

Any project that has an LLM extract claims from source material (narratives
from a corpus, structured data from digitized artifacts, summaries of
records) eventually needs to answer: *how do we know these claims are still
grounded, and how do we track that over time?*

`llm-claim-audit` can help: a **sampler** +
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

sampler = Sampler(population_fn=my_claims, sample_size=25)

verifier = LLMVerifier(
    client=my_openai_compatible_client,
    model="your-model-name",
    prompt_template=my_prompt, # (claim, source) - prompt text
    parse_response=my_parser,  # (response, claim) -> VerificationResult
)

policy = ThresholdPolicy(min_agreement_rate=0.85, alert_agreement_rate=0.7)
store = AuditStore(db_path="audit.sqlite3")

claims = sampler.sample()
results = [verifier.verify(claim, my_source_for(claim)) for claim in claims]
outcome = policy.evaluate(results) #Pass, alert, or fail
store.record_campaign(results, outcome)
```
### Running from the command line

```bash
llm-claim-audit run --config audit-campaign.toml
```
The command prints a one-line summary and exits with code `0` on PASS, or `1`
on ALERT or FAIL, so it can gate a script or CI job.

Example `audit.toml`:

```toml
[sampler]
population = "mypackage.data:get_claims"    # "module:name" of a function returning claims
sample_size = 25
strategy = "random"
rng_seed = 1    #optional

[verifier]
client = "mypackage.clients:client"     # "module:name" of a ready-to-use client object
model = "your-model-name"
prompt_template = "mypackage.prompts:build_prompt"
parse_response = "mypackage.prompts:parse_response"

[threshold]
min_agreement_rate = 0.85
alert_agreement_rate = 0.7  #optional

[store]
db_path = "audit.sqlite3"
```
The CLI calls the verifier with no separate `source`, so each item your
population function returns should carry any source context your
`prompt_template` needs.


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
| [DeepEval](https://github.com/confident-ai/deepeval) | Pytest-style evaluation of LLM apps (RAG, agents, multi-turn) | Scores a defined test set, typically before release. Tracking results across runs lives in its separate hosted platform, not the open-source library |persistence or rolling threshold policy across campaigns |
| [Ragas](https://docs.ragas.io/) | RAG-focused metric library (faithfulness, context precision and recall) | Scores a dataset and returns the numbers; sampling a live pipeline, storing results, and applying a threshold per campaign is left to you |

## License

Apache 2.0. See `LICENSE`.
