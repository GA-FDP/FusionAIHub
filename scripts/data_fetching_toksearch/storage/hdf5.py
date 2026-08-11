"""HDF5 storage backend — backward-compatible with the data_fetching_omega schema.

Schema (identical to read_mds CLI output)
------------------------------------------
  {shot}/
    {tree_label}/
      {fetch_name}/
        data   float32 array
        dim0   float32 time array (milliseconds)

Tree labels are derived from the fetch_name prefix:
  \\D3D::...          → "d3d"
  \\EFIT01::...       → "EFIT01"
  \\MHD::...          → "MHD"
  \\AOT::...          → "AOT"
  \\SPECTROSCOPY::... → "SPECTROSCOPY"
  \\ELECTRONS::...    → "d3d"   (subtree, archived under d3d origin)
  \\IONS::...         → "d3d"
  \\NB::...           → "d3d"
  \\RF::...           → "d3d"
  \\NEUTRALS::...     → "d3d"
  \\OPERATIONS::...   → "d3d"
  \\TANGTV::...       → "tangtv"
  \\IRTV::...         → "irtv"
  bare name (no ::)   → "ptdata"

float32 is written at creation time, eliminating the separate
convert_dtypes.sh post-processing pass used in the omega pipeline.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import h5py
import numpy as np


# Maps the uppercase tree token extracted from a \\TREE:: prefix to the HDF5
# group label used in the original omega schema.
_TREE_LABEL: dict[str, str] = {
    "D3D":         "d3d",
    "EFIT01":      "EFIT01",
    "MHD":         "MHD",
    "AOT":         "AOT",
    "SPECTROSCOPY": "SPECTROSCOPY",
    # Standalone DIII-D subtrees — archived under the d3d origin
    "ELECTRONS":   "d3d",
    "IONS":        "d3d",
    "NB":          "d3d",
    "RF":          "d3d",
    "NEUTRALS":    "d3d",
    "OPERATIONS":  "d3d",
    # Video trees
    "TANGTV":      "tangtv",
    "IRTV":        "irtv",
}

_TREE_PREFIX_RE = re.compile(r"^\\([A-Z0-9_]+)::", re.IGNORECASE)


def _tree_label(fetch_name: str) -> str:
    """Return the HDF5 tree group label for a signal fetch_name."""
    m = _TREE_PREFIX_RE.match(fetch_name)
    if m:
        token = m.group(1).upper()
        return _TREE_LABEL.get(token, token.lower())
    # No :: prefix → PtData signal
    return "ptdata"


def _to_float32(arr: Any) -> np.ndarray:
    return np.asarray(arr, dtype=np.float32)


def write_shot(
    record: dict,
    shot: int,
    output_dir: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write one shot's data from a TokSearch record to an HDF5 file.

    Parameters
    ----------
    record:
        TokSearch record dict (keyed by fetch_name).  Each value is either
        a dict with ``"data"`` and ``"dim0"`` arrays, or ``None`` / missing
        when the signal was absent for this shot.
    shot:
        DIII-D shot number.
    output_dir:
        Directory where ``{shot}.h5`` will be written.
    overwrite:
        If False (default), existing datasets are left untouched.  If True,
        existing datasets are replaced.

    Returns
    -------
    pathlib.Path
        Path to the written HDF5 file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{shot}.h5"

    shot_str = str(shot)

    with h5py.File(out_path, "a") as f:
        if shot_str not in f:
            f.create_group(shot_str)
        shot_grp = f[shot_str]

        for fetch_name, sig_data in record.items():
            if fetch_name == "shot":
                continue
            if sig_data is None:
                continue

            data_arr = sig_data.get("data") if isinstance(sig_data, dict) else None
            dim0_arr = sig_data.get("dim0") if isinstance(sig_data, dict) else None

            if data_arr is None:
                continue

            tree = _tree_label(fetch_name)
            if tree not in shot_grp:
                shot_grp.create_group(tree)
            tree_grp = shot_grp[tree]

            if fetch_name in tree_grp:
                if overwrite:
                    del tree_grp[fetch_name]
                else:
                    continue

            sig_grp = tree_grp.create_group(fetch_name)
            sig_grp.create_dataset("data", data=_to_float32(data_arr), compression="gzip")
            if dim0_arr is not None:
                sig_grp.create_dataset("dim0", data=_to_float32(dim0_arr), compression="gzip")

    return out_path
