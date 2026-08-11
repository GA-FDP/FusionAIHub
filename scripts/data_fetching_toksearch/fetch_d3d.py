"""DIII-D data fetcher using TokSearch + FDP/OSDF.

Replaces the data_fetching_omega SLURM pipeline with a portable Python script
that routes all data through the OSDF FDP D3D origin via setup_environment().

Invocation
----------
Direct (bearer token resolved from ~/.fdp/token):
    python fetch_d3d.py --shots-file shots.txt --output-dir /path/to/output

Via fdp run (alternative for subprocess contexts):
    fdp run python fetch_d3d.py --shots-file shots.txt --output-dir /path/to/output

Via SLURM (no SLURM-specific logic required):
    sbatch --wrap "python fetch_d3d.py --shots-file shots.txt --output-dir /path/to/output"

Shot list options (mutually exclusive):
    --shots-file FILE    one shot number per line
    --range START END    inclusive integer range

Resume / checkpointing:
    Completed shots are appended to OUTPUT_DIR/.completed_shots.
    Re-running skips already-completed shots automatically.
    Failed shots are logged to OUTPUT_DIR/.failed_shots.

Signal selection:
    Default: ALL_SCALAR_SIGNALS (everything except video).
    --video: ALL_SIGNALS (includes tangtv + irtv); use lower --workers
             to avoid memory pressure from 3-D video arrays.
    --signals MODULE.EXPORT  (advanced): dotted path to any signals dict.

Compute backend:
    --workers N    number of parallel workers (default: 4)
    --backend      serial | multiprocessing | ray (default: multiprocessing)
"""
from __future__ import annotations

import argparse
import logging
import sys
import traceback
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch DIII-D signals via TokSearch + FDP/OSDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    shot_group = parser.add_mutually_exclusive_group(required=True)
    shot_group.add_argument("--shots-file", metavar="FILE",
                            help="Path to file with one shot number per line")
    shot_group.add_argument("--range", nargs=2, type=int, metavar=("START", "END"),
                            help="Inclusive shot range")
    parser.add_argument("--output-dir", required=True, metavar="DIR",
                        help="Directory for output HDF5 files")
    parser.add_argument("--video", action="store_true",
                        help="Include tangtv + irtv video signals (memory-intensive)")
    parser.add_argument("--signals", metavar="MODULE.EXPORT",
                        help="Dotted path to a custom signals dict (advanced)")
    parser.add_argument("--workers", type=int, default=4,
                        help="Parallel workers (default: 4; reduce for video)")
    parser.add_argument("--backend", choices=["serial", "multiprocessing", "ray"],
                        default="multiprocessing",
                        help="Compute backend (default: multiprocessing)")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing datasets in output HDF5 files")
    parser.add_argument("--no-resume", action="store_true",
                        help="Ignore .completed_shots and re-fetch all shots")
    return parser


def _load_signals(spec: str | None, video: bool):
    from .signals import ALL_SCALAR_SIGNALS, ALL_SIGNALS
    if spec:
        module_path, attr = spec.rsplit(".", 1)
        import importlib
        mod = importlib.import_module(module_path)
        return getattr(mod, attr)
    return ALL_SIGNALS if video else ALL_SCALAR_SIGNALS


def _load_shots(shots_file: str | None, range_args: list[int] | None) -> list[int]:
    if shots_file:
        lines = Path(shots_file).read_text().splitlines()
        return [int(ln.strip()) for ln in lines if ln.strip() and not ln.startswith("#")]
    start, end = range_args
    return list(range(start, end + 1))


def _load_completed(output_dir: Path) -> set[int]:
    cp = output_dir / ".completed_shots"
    if not cp.exists():
        return set()
    return {int(ln.strip()) for ln in cp.read_text().splitlines() if ln.strip()}


def _append_line(path: Path, value: str) -> None:
    with path.open("a") as f:
        f.write(value + "\n")


def _compute_kwargs(backend: str, workers: int) -> dict:
    if backend == "serial":
        return {"num_workers": 1}
    if backend == "ray":
        return {"backend": "ray", "num_workers": workers}
    return {"num_workers": workers}


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    log.info("Calling setup_environment()...")
    from toksearch_d3d import setup_environment
    setup_environment()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    completed_file = output_dir / ".completed_shots"
    failed_file = output_dir / ".failed_shots"

    all_shots = _load_shots(args.shots_file, args.range)
    if args.no_resume:
        shots = all_shots
    else:
        completed = _load_completed(output_dir)
        shots = [s for s in all_shots if s not in completed]
        skipped = len(all_shots) - len(shots)
        if skipped:
            log.info("Skipping %d already-completed shots", skipped)

    if not shots:
        log.info("No shots to process.")
        return 0

    log.info("Processing %d shots → %s", len(shots), output_dir)

    signals = _load_signals(args.signals, args.video)
    log.info("Fetching %d signals per shot", len(signals))

    from .pipeline import build_pipeline
    from .storage.hdf5 import write_shot

    pipeline = build_pipeline(shots, signals=signals)
    n_ok = n_fail = 0

    for record in pipeline.compute(**_compute_kwargs(args.backend, args.workers)):
        shot = record["shot"]
        try:
            out_path = write_shot(record, shot, output_dir, overwrite=args.overwrite)
            _append_line(completed_file, str(shot))
            n_ok += 1
            log.info("shot %d → %s", shot, out_path.name)
        except Exception:
            _append_line(failed_file, str(shot))
            n_fail += 1
            log.error("shot %d FAILED:\n%s", shot, traceback.format_exc())

    log.info("Done. %d succeeded, %d failed.", n_ok, n_fail)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
