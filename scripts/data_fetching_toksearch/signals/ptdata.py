"""PtDataSignal definitions for DIII-D.

fetch_name == the bare signal name string (used as HDF5 dataset key and
TokSearch record key, preserving backward compatibility with the omega pipeline).

Source: scripts/data_fetching_omega/config_atlas.yaml  (lines 1720–1929)
Fix: MPI1A274D deduplicated (appeared twice on lines 1745 and 1748).
"""
from toksearch import PtDataSignal


def _pt(name: str) -> PtDataSignal:
    return PtDataSignal(name)


# ---------------------------------------------------------------------------
# MPI pickup coils  (28 unique signals — MPI1A274D deduplicated)
# ---------------------------------------------------------------------------
_MPI_NAMES = [
    "MPI1A322D",
    "MPI3A322D",
    "MPI5A322D",
    "MPI89A322D",
    "MPI79FA322D",
    "MPI7FA322D",
    "MPI67A322D",
    "MPI6NA322D",
    "MPI1B322D",
    "MPI3B322D",
    "MPI5B322D",
    "MPI89B322D",
    "MPI79B322D",
    "MPI7NB322D",
    "MPI6FB322D",
    "MPI66M322D",
    "MPI66M132D",
    "MPI66B137D",
    "MPI66M312D",
    "MPI66B312D",
    "MPI66M020D",
    "MPI66M097D",
    "MPI66M307D",
    "MPI1A011D",
    "MPI1A274D",   # duplicate at line 1748 removed
    "MPI1A109D",
    "MPI1A199D",
    "MPI1A341D",
]
MPI_SIGNALS: dict = {name: _pt(name) for name in _MPI_NAMES}

# ---------------------------------------------------------------------------
# Beam attenuation  (b1–b8)
# ---------------------------------------------------------------------------
BEAM_ATTN_SIGNALS: dict = {f"b{i}": _pt(f"b{i}") for i in range(1, 9)}

# ---------------------------------------------------------------------------
# Thomson scattering tangential-viewing plasma-length angles  (TPLANG01–72)
# ---------------------------------------------------------------------------
TPLANG_SIGNALS: dict = {f"TPLANG{i:02d}": _pt(f"TPLANG{i:02d}") for i in range(1, 73)}

# ---------------------------------------------------------------------------
# C-coil currents
# ---------------------------------------------------------------------------
_C_COIL_NAMES = ["C19F", "C79F", "C139F", "C199F", "C259F", "C319F"]
C_COIL_SIGNALS: dict = {name: _pt(name) for name in _C_COIL_NAMES}

# ---------------------------------------------------------------------------
# I-coil currents — upper (IU) and lower (IL), 6 toroidal positions each
# ---------------------------------------------------------------------------
_I_COIL_POSITIONS = [30, 90, 150, 210, 270, 330]
I_COIL_SIGNALS: dict = {
    **{f"IU{pos}F": _pt(f"IU{pos}F") for pos in _I_COIL_POSITIONS},
    **{f"IL{pos}F": _pt(f"IL{pos}F") for pos in _I_COIL_POSITIONS},
}

# ---------------------------------------------------------------------------
# I-coil toroidal harmonic amplitudes  (ILN1/2/3IAMP, IUN1/2/3IAMP)
# ---------------------------------------------------------------------------
ICOIL_HARM_SIGNALS: dict = {
    **{f"ILN{n}IAMP": _pt(f"ILN{n}IAMP") for n in range(1, 4)},
    **{f"IUN{n}IAMP": _pt(f"IUN{n}IAMP") for n in range(1, 4)},
}

# ---------------------------------------------------------------------------
# BES (beam emission spectroscopy) channels  (BESFU01–64)
# ---------------------------------------------------------------------------
BES_SIGNALS: dict = {f"BESFU{i:02d}": _pt(f"BESFU{i:02d}") for i in range(1, 65)}

# ---------------------------------------------------------------------------
# Engineering scalars
# ---------------------------------------------------------------------------
_SCALAR_NAMES = [
    "bcoil",
    "bmspinj",
    "bmstinj",
    "bt",
    "dssdenest",
    "fzns",
    "ip",
    "ipsip",
    "iptipp",
    "pcbcoil",
    "plasticfix",
    "dstdenp",
]
SCALAR_SIGNALS: dict = {name: _pt(name) for name in _SCALAR_NAMES}

# ---------------------------------------------------------------------------
# Composite
# ---------------------------------------------------------------------------
PTDATA_SIGNALS: dict = {
    **MPI_SIGNALS,
    **BEAM_ATTN_SIGNALS,
    **TPLANG_SIGNALS,
    **C_COIL_SIGNALS,
    **I_COIL_SIGNALS,
    **ICOIL_HARM_SIGNALS,
    **BES_SIGNALS,
    **SCALAR_SIGNALS,
}
