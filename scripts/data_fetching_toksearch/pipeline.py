"""TokSearch pipeline builder for DIII-D data fetching.

Returns a configured Pipeline object; callers decide how to compute and
store results.  No I/O is performed here.

Usage
-----
    from pipeline import build_pipeline
    from signals import ALL_SCALAR_SIGNALS

    pipeline = build_pipeline(shots=[180000, 180001], signals=ALL_SCALAR_SIGNALS)
    for record in pipeline.compute():
        shot = record["shot"]
        ...

Compute options (caller-controlled):
    pipeline.compute()                          # serial
    pipeline.compute(num_workers=8)             # multiprocessing
    pipeline.compute(backend="ray")             # Ray (requires ray[default])
"""
from __future__ import annotations

from typing import Mapping

from toksearch import Pipeline

from .signals import ALL_SIGNALS


def build_pipeline(
    shots: list[int],
    signals: Mapping | None = None,
) -> Pipeline:
    """Return a Pipeline that fetches *signals* for every shot in *shots*.

    Parameters
    ----------
    shots:
        List of DIII-D shot numbers.
    signals:
        Mapping of fetch_name -> Signal object.  Defaults to ALL_SIGNALS
        (all scalar + video signals).  Pass a subset dict to fetch only
        selected diagnostics.

    Returns
    -------
    toksearch.Pipeline
        Configured pipeline ready for ``.compute()``.  No computation is
        triggered by this call.
    """
    if signals is None:
        signals = ALL_SIGNALS

    pipeline = Pipeline(shots)
    for name, sig in signals.items():
        pipeline = pipeline.fetch(name, sig)
    return pipeline
