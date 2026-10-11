"""Sampler: decides which claims/narratives get pulled for audit.

Consumers (e.g. semantic_index) supply the source population and a sampling
strategy; the package stays agnostic to what a "claim" or "narrative" is.
"""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Sequence


@dataclass
class Sampler:
    """Selects a subset of items from a population to audit.

    Attributes:
        population_fn: callable returning the full set of candidate items
            (e.g. narratives produced since the last audit run).
        sample_size: number of items to draw per audit campaign.
        strategy: how to draw the sample. Defaults to "random"; consumers
            may plug in "stratified", "most_recent", etc.
        rng_seed: optional seed for reproducible sampling.
    """

    population_fn: Callable[[], Iterable[Any]]
    sample_size: int
    strategy: str = "random"
    rng_seed: int | None = None
    _extra: dict = field(default_factory=dict)

    def sample(self) -> Sequence[Any]:
        population = list(self.population_fn())
        rng = random.Random(self.rng_seed)
        if self.strategy == "random":
            return rng.sample(population, min(self.sample_size, len(population)))
        else:
            raise ValueError(f"Unknown sampling strategy: {self.strategy!r}")
