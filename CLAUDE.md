# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment Setup

This project uses [Pixi](https://pixi.sh) (not Anaconda/conda) for environment management.

```bash
# Install Pixi (one-time)
curl -fsSL https://pixi.sh/install.sh | sh

# Install dependencies
pixi install

# Activate environment (required each session)
pixi shell
```

## Data Fetching Pipelines

There are two parallel data fetching pipelines targeting DIII-D tokamak shot data:

### 1. `scripts/data_fetching_toksearch/` (primary, portable)

A Python package that replaces the omega SLURM pipeline. Routes all data through the OSDF FDP D3D origin (Pelican) — no direct connections to `atlas.gat.com` or `chiron.gat.com`. Requires `toksearch_d3d.setup_environment()` to be called before any pipeline execution.

**Entry point:** `fetch_d3d.py`

```bash
# Authenticate via FDP bearer token (~/.fdp/token)
python -m scripts.data_fetching_toksearch.fetch_d3d --shots-file shots.txt --output-dir /path/to/output

# Or via fdp CLI (alternative for subprocess contexts)
fdp run python fetch_d3d.py --shots-file shots.txt --output-dir /path/to/output

# Via SLURM
sbatch --wrap "python fetch_d3d.py --shots-file shots.txt --output-dir /path/to/output"

# Shot selection options (mutually exclusive)
--shots-file FILE    # one shot per line, lines starting with # are comments
--range START END    # inclusive integer range

# Signal selection
# Default: ALL_SCALAR_SIGNALS (all signals except video)
--video              # include tangtv + irtv video (memory-intensive; use fewer --workers)
--signals MODULE.EXPORT  # dotted path to a custom signals dict

# Backend options
--workers N          # parallel workers (default: 4)
--backend serial|multiprocessing|ray  # (default: multiprocessing)

# Resume / overwrite
--overwrite          # overwrite existing HDF5 datasets
--no-resume          # ignore .completed_shots and re-fetch all shots
```

**Key internal modules:**
- `signals/__init__.py` — exports `ALL_SCALAR_SIGNALS` and `ALL_SIGNALS` (composite dicts)
- `signals/mds.py` — `MdsSignal` definitions for all MDSplus trees (d3d, efit01, mhd, aot, spectroscopy, tangtv, irtv)
- `signals/ptdata.py` — `PtDataSignal` definitions (MPI coils, BES, TPLANG, C/I-coils, engineering scalars)
- `pipeline.py` — `build_pipeline(shots, signals)` returns a configured `toksearch.Pipeline`
- `storage/hdf5.py` — `write_shot(record, shot, output_dir)` writes one shot's data to HDF5

**Signal dict conventions:**
- `MdsSignal` fetch keys are full MDSplus paths: `r"\D3D::TOP.ELECTRONS.TS.BLESSED.CORE:DENSITY"`
- `PtDataSignal` fetch keys are bare signal names: `"ip"`, `"bt"`, `"BESFU01"`
- These keys are also used as HDF5 dataset keys (backward-compatible with the omega schema)

### 2. `scripts/data_fetching_omega/` (legacy SLURM-based)

Shell + YAML pipeline that connects directly to `atlas.gat.com` and `chiron.gat.com` via MDSplus. Uses SLURM job arrays for parallelism. Configure shot range/list and server in `submit_read_mds_batches.sh`, then:

```bash
# Foreground
./submit_read_mds_batches.sh

# Background (recommended for long runs)
nohup ./submit_read_mds_batches.sh > submission_d3d_mdsplus.log 2>&1 &
```

Signal lists are defined in `config_atlas.yaml` (atlas server) and `config_chiron.yaml` (chiron server / video).

## HDF5 Output Schema

Both pipelines write the same schema (toksearch pipeline writes float32 directly, eliminating the separate `convert_dtypes.sh` step):

```
{shot}.h5
└── {shot}/
    └── {tree}/          # "d3d", "EFIT01", "MHD", "AOT", "SPECTROSCOPY", "ptdata", "tangtv", "irtv"
        └── {fetch_name}/
            ├── data     # float32 signal values
            └── dim0     # float32 time axis (milliseconds)
```

Resume/checkpointing: completed shots are tracked in `OUTPUT_DIR/.completed_shots`; failed shots in `OUTPUT_DIR/.failed_shots`. Re-running automatically skips completed shots.

## Data Storage Locations (Princeton Clusters)

- Raw data: `/scratch/gpfs/EKOLEMEN/d3d_fusion_data/`
- Raw video: `/scratch/gpfs/EKOLEMEN/big_d3d_data/images/`
- Model-ready files: `/scratch/gpfs/EKOLEMEN/foundation_model/` (set permissions to `664`)

## Training

Models support single GPU and multi-GPU (DDP) training. WandB is set to offline by default; sync with:

```bash
wandb sync --sync-all --include-offline
```

Monitor SLURM jobs: `squeue -u <username>`, `jobstats <job_id>`.

## Flash Attention

Install from prebuilt wheels — do NOT use `pip install flash-attn` (builds are slow). Find a wheel matching your CUDA/Python/PyTorch versions at the Dao-AILab or mjun0812 GitHub releases pages. Requires GCC >= 9 (on Princeton clusters: `module load gcc-toolset/10`).

## ImasSignal — Not Used in This Pipeline

`ImasSignal`/`ImasComposer` was evaluated and rejected as the primary data access interface. See `scripts/data_fetching_toksearch/IMAS_DEFICIENCIES.md` for the full rationale. Key issues: most diagnostics have no IMAS IDS at DIII-D, PTData JSON index caps at ~shot 201,299, and silent exception suppression makes batch failures opaque. Use `MdsSignal` and `PtDataSignal` directly.
