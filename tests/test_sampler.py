"""Unit tests for Sampler. No network calls — pure logic."""

import pytest

from llm_claim_audit import Sampler

def test_sampler_random_strategy_returns_requested_size():
    population = list(range(100))
    sampler = Sampler(population_fn=lambda: population, sample_size=10, rng_seed=42)

    result = sampler.sample()
    assert len(result) == 10


def test_sampler_returns_unique_items():
    population = list(range(100))
    sampler = Sampler(population_fn=lambda: population, sample_size=10, rng_seed=42)

    result = sampler.sample()
    assert len(set(result)) == len(result)


def test_sampler_seed_is_reproducible():
    population = list(range(100))
    sampler_a = Sampler(population_fn=lambda: population, sample_size=10, rng_seed=42)
    sampler_b = Sampler(population_fn=lambda: population, sample_size=10, rng_seed=42)

    assert sampler_a.sample() == sampler_b.sample()


def test_sampler_handles_population_smaller_than_sample_size():
    population = [1, 2, 3]
    sampler = Sampler(population_fn=lambda: population, sample_size=10)

    result = sampler.sample()
    assert len(result) == 3


def test_sampler_unknown_strategy_raises():
    sampler = Sampler(population_fn=lambda: [], sample_size=5, strategy="bogus")

    with pytest.raises(ValueError):
        sampler.sample()