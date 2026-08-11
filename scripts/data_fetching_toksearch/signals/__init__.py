"""DIII-D signal catalog for TokSearch.

Each submodule exports named dicts mapping fetch_name -> Signal object:
  - fetch_name for MdsSignal: full MDSplus path string, e.g. r"\D3D::TOP.ELECTRONS.TS.BLESSED.CORE:DENSITY"
  - fetch_name for PtDataSignal: bare signal name, e.g. "ip"

These keys are used as signal names in the TokSearch record and as HDF5 dataset keys,
preserving backward compatibility with the data_fetching_omega schema.

Submodules
----------
mds     -- all MdsSignal definitions (d3d, efit01, mhd, aot, spectroscopy, tangtv, irtv trees)
ptdata  -- all PtDataSignal definitions (MPI, BES, TPLANG, coils, scalars)

Composite collections (assembled here)
---------------------------------------
ALL_SCALAR_SIGNALS  -- every signal except video streams
ALL_SIGNALS         -- ALL_SCALAR_SIGNALS + tangtv/irtv video

Call toksearch_d3d.setup_environment() before executing any pipeline that uses these signals.
"""
from .mds import (
    TS_SIGNALS,
    ECE_SIGNALS,
    BCI_SIGNALS,
    CER_SIGNALS,
    ICOIL_SIGNALS,
    SXR_SIGNALS,
    NEUTRON_SIGNALS,
    MSE_SIGNALS,
    BOLOM_RAW_SIGNALS,
    VB_SIGNALS,
    FILTERSCOPE_SIGNALS,
    DIVSPRED_SIGNALS,
    BOLOM_PWR_SIGNALS,
    NBI_SIGNALS,
    ECH_SIGNALS,
    ICH_SIGNALS,
    GAS_SIGNALS,
    EFIT_SIGNALS,
    MHD_SIGNALS,
    AOT_SIGNALS,
    VIDEO_SIGNALS,
)
from .ptdata import PTDATA_SIGNALS

ALL_SCALAR_SIGNALS: dict = {
    **TS_SIGNALS,
    **ECE_SIGNALS,
    **BCI_SIGNALS,
    **CER_SIGNALS,
    **ICOIL_SIGNALS,
    **SXR_SIGNALS,
    **NEUTRON_SIGNALS,
    **MSE_SIGNALS,
    **BOLOM_RAW_SIGNALS,
    **VB_SIGNALS,
    **FILTERSCOPE_SIGNALS,
    **DIVSPRED_SIGNALS,
    **BOLOM_PWR_SIGNALS,
    **NBI_SIGNALS,
    **ECH_SIGNALS,
    **ICH_SIGNALS,
    **GAS_SIGNALS,
    **EFIT_SIGNALS,
    **MHD_SIGNALS,
    **AOT_SIGNALS,
    **PTDATA_SIGNALS,
}

ALL_SIGNALS: dict = {**ALL_SCALAR_SIGNALS, **VIDEO_SIGNALS}
