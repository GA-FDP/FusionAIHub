# ImasSignal / ImasComposer — Deficiencies for Full DIII-D Signal Coverage

This document records the specific gaps and design issues that prevent `ImasSignal`/`ImasComposer`
from being a viable primary interface for the signals targeted by this pipeline. Intended as a
reference for when the IMAS situation at DIII-D improves and a re-evaluation is warranted.

---

## 1. Coverage Gaps — Most Diagnostics Have No IMAS IDS

The majority of signals in this pipeline have no IMAS IDS representation at DIII-D via FDP/OSDF.
`ImasSignal` cannot substitute for `MdsSignal` for any of:

- CER (charge exchange recombination — arguably the most important ion diagnostic)
- MSE (motional Stark effect)
- SXR arrays (10 arrays, 330 channels)
- Bolometry raw voltage
- Visible bremsstrahlung / Zeff
- Filterscopes (PMT arrays, FS01–08)
- Divertor spectroscopy (DIVSPRED)
- ECH (12 gyrotrons — geometry, power, status)
- ICH
- Gas injection (11 valves)
- I-coil toroidal harmonics
- MHD mode amplitudes (N1RMS, N2RMS)
- AOT shape parameters
- Most PtData signals (MPI coils, BES, TPLANG, C-coils, limiter angles, scalars)

This alone makes a full IMAS-based replacement impossible without a substantial increase in
IMAS population at DIII-D. Any hybrid approach requires maintaining both MdsSignal and
ImasSignal pipelines in parallel.

---

## 2. NBI Coverage Is Incomplete

`ImasSignal("nbi.unit.power_launched.data")` returns total injected power per NBI unit (8 units).
The omega script fetches ~70 nodes per beam: BEAMTARGET parameters, OANB geometry, per-beam
current/voltage/efficiency/modulation/timing, and injection scalars. None of these are covered by
the current `nbi` IDS at DIII-D. A full NBI → IMAS migration would require either:

- Populating the `nbi` IDS with all diagnostic nodes (not currently done), or
- Keeping MDS for all NBI nodes except total power, creating a split that is harder to maintain
  than the pure-MDS approach.

---

## 3. Hardcoded Tree Assumptions

`ImasComposer` hardcodes tree names that limit portability:

| Parameter | Default | Issue |
|---|---|---|
| `efit_tree` | `"EFIT01"` | Only `efit01` tree is available via FDP Pelican; EFIT02 etc. are not |
| `profiles_tree` | `"ZIPFIT01"` | ZIPFIT01 may not be populated for all shots or all campaigns |
| `efit_run_id` | `""` | No mechanism to handle run IDs without re-instantiating the composer |
| `profiles_run_id` | `""` | Same |

Passing a different equilibrium reconstruction (e.g., kinetic EFIT) requires constructing a
separate ImasComposer instance. There is no per-shot override.

---

## 4. PTData JSON Index Cap (~Shot 201,299)

`PtDataSignal("pinj")` (total NBI injected power) returns "Invalid shot number" for shots above
the PTData JSON index ceiling (approximately shot 201,299). This is a known limitation documented
in the `toksearch_d3d` module docstring. The recommended workaround is `ImasSignal("nbi.unit.power_launched.data")`,
but this only covers total power (see §2 above) and itself hits the shot-range availability
problem: magnetics and TF ptdata are not indexed for recent shots (e.g., shot 202161 is absent
from the magnetics index; tests fall back to shot 200000 for those signals).

The core problem is that IMAS population at DIII-D does not have uniform coverage across the full
shot range, so no single access path is reliable for all shots.

---

## 5. Silent Exception Suppression Makes Debugging Painful

All three dimension-fetch methods in `ImasSignal` catch bare `Exception` and silently return
`None` or skip the dimension:

- `_fetch_dim()` (returns `None` on any exception)
- `_fetch_all_dims()` (omits the dimension from the result dict)
- `_split_by_channel()` (skips per-channel dim with `except Exception: pass`)

A fetch that fails due to a misconfigured tree path, a missing IDS field, or a transient network
error is indistinguishable from a shot where the data legitimately does not exist. This makes
large-scale batch fetching opaque — silent partial results are worse than loud failures for
archival pipelines where completeness matters.

---

## 6. Multi-Round-Trip Compose Cycle Adds Latency Per Shot

`ImasSignal.fetch()` runs a resolve → fetch → compose loop of up to `max_resolve_iterations=10`
iterations before composing the result. Each iteration may trigger additional MDSplus or PtData
fetches. For a pipeline fetching ~1,800 signals across thousands of shots, this overhead
compounds. Direct `MdsSignal` and `PtDataSignal` calls are single-trip.

If the resolve loop does not converge within `max_resolve_iterations`, the code proceeds to
compose with incomplete `raw_data` without raising an error — silently producing wrong or
partial results.

---

## 7. Heterogeneous Record Structures Break Uniform HDF5 Writing

`ImasSignal` can return three structurally different record objects depending on usage:

| Mode | Record structure |
|---|---|
| Default (leaf path) | `{"data": ndarray, "times": ndarray}` |
| `split_by="channel"` | `{"ch_0": {"data": ndarray, "times": ndarray, ...}, "ch_1": {...}, ...}` |
| Prefix path | `{"field_a": {"data": ..., "times": ...}, "field_b": {...}, ...}` |
| Ragged data with xarray | Raises `NotImplementedError` |

The split-by-channel output breaks the uniform `data` + `dim0` schema used by the existing
HDF5 writer and the downstream Princeton pipeline. Supporting all three modes would require
branching logic in the storage layer and a non-backward-compatible HDF5 schema for channel-indexed
diagnostics.

---

## 8. Shared Composer Required but Architecturally Awkward

For efficiency, all `ImasSignal` instances in a pipeline should share a single `ImasComposer`
so that the tree connection and resolve state are reused. This requires that signal objects be
constructed with a reference to a pre-existing composer rather than being purely declarative.
This breaks the simple catalog pattern (a flat dict of `name → Signal`) used by the rest of this
pipeline: the catalog can no longer be defined at module import time and must be rebuilt at
pipeline construction time after the composer is instantiated.

---

## 9. Time Unit Convention Is a Latent Bug Source

IMAS stores times in seconds. `ImasSignal` applies a default `dim_scales={"times": 1000.0}`
to convert to milliseconds for toksearch convention. This is invisible to callers — a signal
declared as `ImasSignal("equilibrium.time_slice.global_quantities.ip")` silently returns times
in milliseconds, while a signal declared as
`ImasSignal("equilibrium.time_slice.global_quantities.ip", dim_scales={"times": 1.0})` returns
seconds. Any downstream code that assumes a time unit has no way to verify which was used without
inspecting the signal declaration. MdsSignal returns whatever the MDSplus node stores (typically
milliseconds for DIII-D) without transformation.

---

## Summary: Conditions for Reconsideration

`ImasSignal` becomes viable as a primary interface when:

1. IMAS IDS population at DIII-D extends to CER, MSE, ECH, gas, bolometry, SXR, and MHD/AOT
2. Coverage is uniform across the full historical shot range (not shot-range-dependent)
3. The silent exception suppression pattern is replaced with explicit missing-data signaling
4. The PTData JSON index limitation is resolved for recent shots
5. NBI IDS includes per-beam diagnostic nodes beyond total injected power
6. `ImasComposer` supports per-shot tree overrides so equilibrium reconstruction choice is
   flexible at pipeline execution time rather than at composer construction time
