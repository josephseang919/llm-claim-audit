"""Unit tests for Sampler. No network calls — pure logic."""

import pytest

from llm_claim_audit import Sampler


def test_sampler_random_strategy_returns_requested_size():
    population = list(range(100))
    sampler = Sampler(population_fn=lambda: population, sample_size=10, rng_seed=42)

    with pytest.raises(NotImplementedError):
        # TODO: once implemented, assert len(sampler.sample()) == 10
        sampler.sample()


def test_sampler_unknown_strategy_raises():
    sampler = Sampler(population_fn=lambda: [], sample_size=5, strategy="bogus")

    with pytest.raises(NotImplementedError):
        # TODO: once implemented, assert this raises ValueError instead
        sampler.sample()
