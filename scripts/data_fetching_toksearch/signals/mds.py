"""MdsSignal definitions for the DIII-D signal catalog.

All signals are accessed via the OSDF FDP D3D origin (Pelican). No direct
connections to atlas.gat.com or chiron.gat.com are made. Call
toksearch_d3d.setup_environment() before executing any pipeline.

fetch_name (dict key) is the full MDSplus path as it appears in the original
config_atlas.yaml / config_chiron.yaml. This string is also used as the HDF5
dataset key, preserving backward compatibility with the omega pipeline schema.

MdsSignal node is the path with the leading \\TREE:: prefix stripped.
"""
from toksearch import MdsSignal


def _mds(node: str, tree: str) -> MdsSignal:
    return MdsSignal(node, tree)


# ── Thomson Scattering ─────────────────────────────────────────────────────────
TS_SIGNALS = {
    r"\D3D::TOP.ELECTRONS.TS.BLESSED.CORE:DENSITY":
        _mds("TOP.ELECTRONS.TS.BLESSED.CORE:DENSITY", "d3d"),
    r"\D3D::TOP.ELECTRONS.TS.BLESSED.CORE:TEMP":
        _mds("TOP.ELECTRONS.TS.BLESSED.CORE:TEMP", "d3d"),
    r"\D3D::TOP.ELECTRONS.TS.BLESSED.TANGENTIAL:DENSITY":
        _mds("TOP.ELECTRONS.TS.BLESSED.TANGENTIAL:DENSITY", "d3d"),
    r"\D3D::TOP.ELECTRONS.TS.BLESSED.TANGENTIAL:TEMP":
        _mds("TOP.ELECTRONS.TS.BLESSED.TANGENTIAL:TEMP", "d3d"),
    r"\D3D::TOP.ELECTRONS.TS.BLESSED.DIVERTOR:DENSITY":
        _mds("TOP.ELECTRONS.TS.BLESSED.DIVERTOR:DENSITY", "d3d"),
    r"\D3D::TOP.ELECTRONS.TS.BLESSED.DIVERTOR:TEMP":
        _mds("TOP.ELECTRONS.TS.BLESSED.DIVERTOR:TEMP", "d3d"),
}

# ── ECE (48 channels) ──────────────────────────────────────────────────────────
ECE_SIGNALS = {
    rf"\D3D::TOP.ELECTRONS.ECE.TECEF:TECEF{i:02d}":
        _mds(f"TOP.ELECTRONS.ECE.TECEF:TECEF{i:02d}", "d3d")
    for i in range(1, 49)
}

# ── BCI Interferometry (4 chords) ─────────────────────────────────────────────
BCI_SIGNALS = {
    r"\D3D::TOP.ELECTRONS.BCI.DPD.R0:DENUF": _mds("TOP.ELECTRONS.BCI.DPD.R0:DENUF", "d3d"),
    r"\D3D::TOP.ELECTRONS.BCI.DPD.V1:DENUF": _mds("TOP.ELECTRONS.BCI.DPD.V1:DENUF", "d3d"),
    r"\D3D::TOP.ELECTRONS.BCI.DPD.V2:DENUF": _mds("TOP.ELECTRONS.BCI.DPD.V2:DENUF", "d3d"),
    r"\D3D::TOP.ELECTRONS.BCI.DPD.V3:DENUF": _mds("TOP.ELECTRONS.BCI.DPD.V3:DENUF", "d3d"),
}

# ── CER (48 tangential + 32 vertical channels, TEMP and ROT each) ─────────────
CER_SIGNALS = {
    **{
        rf"\D3D::TOP.IONS.CER.CERAUTO.TANGENTIAL.CHANNEL{i:02d}:{param}":
            _mds(f"TOP.IONS.CER.CERAUTO.TANGENTIAL.CHANNEL{i:02d}:{param}", "d3d")
        for i in range(1, 49) for param in ("TEMP", "ROT")
    },
    **{
        rf"\D3D::TOP.IONS.CER.CERAUTO.VERTICAL.CHANNEL{i:02d}:{param}":
            _mds(f"TOP.IONS.CER.CERAUTO.VERTICAL.CHANNEL{i:02d}:{param}", "d3d")
        for i in range(1, 33) for param in ("TEMP", "ROT")
    },
}

# ── I-coil Toroidal Harmonics ──────────────────────────────────────────────────
ICOIL_SIGNALS = {
    rf"\D3D::TOP.OPERATIONS.ICOIL.TORHARMS.{node}":
        _mds(f"TOP.OPERATIONS.ICOIL.TORHARMS.{node}", "d3d")
    for node in ("ILN1IAMP", "ILN2IAMP", "ILN3IAMP", "IUN1IAMP", "IUN2IAMP", "IUN3IAMP")
}

# ── SXR Arrays (10 arrays x 32 channels + TIMEBASE each) ─────────────────────
_SXR_ARRAYS = (
    "SX165R1F", "SX165R1S", "SX195R1F", "SX195R1S",
    "SX45R1F",  "SX45R1S",  "SX90RM1F", "SX90RM1S", "SX90RP1F", "SX90RP1S",
)

SXR_SIGNALS: dict = {}
for _arr in _SXR_ARRAYS:
    for _ch in range(1, 33):
        _k = rf"\D3D::TOP.SPECTROSCOPY.SXR:{_arr}:{_arr}{_ch:02d}"
        SXR_SIGNALS[_k] = _mds(f"TOP.SPECTROSCOPY.SXR:{_arr}:{_arr}{_ch:02d}", "d3d")
    _k = rf"\D3D::TOP.SPECTROSCOPY.SXR:{_arr}:TIMEBASE"
    SXR_SIGNALS[_k] = _mds(f"TOP.SPECTROSCOPY.SXR:{_arr}:TIMEBASE", "d3d")

# ── Neutron Rates (IONS.NEUTRONS.FIP) ────────────────────────────────────────
NEUTRON_SIGNALS = {
    r"\D3D::TOP.IONS.NEUTRONS.FIP:NEUTRONRATE1":
        _mds("TOP.IONS.NEUTRONS.FIP:NEUTRONRATE1", "d3d"),
    r"\D3D::TOP.IONS.NEUTRONS.FIP:NEUTRONRATE3":
        _mds("TOP.IONS.NEUTRONS.FIP:NEUTRONRATE3", "d3d"),
    r"\D3D::TOP.IONS.NEUTRONS.FIP:NEUTRONRATE4":
        _mds("TOP.IONS.NEUTRONS.FIP:NEUTRONRATE4", "d3d"),
    r"\D3D::TOP.IONS.NEUTRONS.FIP:NEUTRONSRATE":
        _mds("TOP.IONS.NEUTRONS.FIP:NEUTRONSRATE", "d3d"),
}

# ── MSE (69 channels + per-channel timebases) ─────────────────────────────────
MSE_SIGNALS = {
    **{
        rf"\D3D::TOP.MSE.ANALYSIS_01:MSEP{i:02d}":
            _mds(f"TOP.MSE.ANALYSIS_01:MSEP{i:02d}", "d3d")
        for i in range(1, 70)
    },
    **{
        rf"\D3D::TOP.MSE.ANALYSIS_01:MSEP{i:02d}:TIME":
            _mds(f"TOP.MSE.ANALYSIS_01:MSEP{i:02d}:TIME", "d3d")
        for i in range(1, 70)
    },
}

# ── Bolometry Raw Voltage (48 channels: L01-24, U01-24) ──────────────────────
BOLOM_RAW_SIGNALS = {
    rf"\D3D::TOP.SPECTROSCOPY.PRAD.BOLOM.RAW:BOL_{side}{i:02d}_V":
        _mds(f"TOP.SPECTROSCOPY.PRAD.BOLOM.RAW:BOL_{side}{i:02d}_V", "d3d")
    for side in ("L", "U") for i in range(1, 25)
}

# ── Visible Bremsstrahlung / Zeff (tubes, chords, Zeff channels) ─────────────
VB_SIGNALS = {
    **{
        rf"\D3D::TOP.SPECTROSCOPY.VB.TUBE{i:02d}":
            _mds(f"TOP.SPECTROSCOPY.VB.TUBE{i:02d}", "d3d")
        for i in range(1, 25)
    },
    **{
        rf"\D3D::TOP.SPECTROSCOPY.VB.CHORD{i:02d}":
            _mds(f"TOP.SPECTROSCOPY.VB.CHORD{i:02d}", "d3d")
        for i in range(1, 25)
    },
    **{
        rf"\D3D::TOP.SPECTROSCOPY.VB.ZEFF:ZEFF_{i:02d}":
            _mds(f"TOP.SPECTROSCOPY.VB.ZEFF:ZEFF_{i:02d}", "d3d")
        for i in range(1, 25)
    },
}

# ── Filterscopes ──────────────────────────────────────────────────────────────
# FS01-08: in the SPECTROSCOPY tree (paths use \SPECTROSCOPY:: despite appearing
#          in the d3d block of config_atlas.yaml — must use tree="spectroscopy")
# PMT01-96: in the d3d tree under TOP.SPECTROSCOPY.FILTERSCOPE
FILTERSCOPE_SIGNALS = {
    **{
        rf"\SPECTROSCOPY::FS{i:02d}": _mds(f"FS{i:02d}", "spectroscopy")
        for i in range(1, 9)
    },
    **{
        rf"\D3D::TOP.SPECTROSCOPY.FILTERSCOPE.PMT{i:02d}":
            _mds(f"TOP.SPECTROSCOPY.FILTERSCOPE.PMT{i:02d}", "d3d")
        for i in range(1, 97)
    },
}

# ── NBI (8 beams: NB15L/R, NB21L/R, NB30L/R, NB33L/R) ───────────────────────
_NB_BEAMS = ("NB15L", "NB15R", "NB21L", "NB21R", "NB30L", "NB30R", "NB33L", "NB33R")

# Appended to "<beam>.BEAMTARGET"; empty string = the BEAMTARGET node itself
_NB_BEAMTARGET_SUFFIXES = (
    "", ":ACTUAL", ":ACTUALF", ":BEAMCOM", ":BEAMPROG",
    ":DIFF", ":DIFFF", ":DUR", ":OFFTRAIN", ":ONTRAIN",
    ":PHASE", ":START", ":STATE", ":TARGET", ":TARGETF",
    ":TDAT", ":TDATF", ":TIMEBASE",
)

# Appended to "<beam>.OANB"; empty string = the OANB node itself
_NB_OANB_SUFFIXES = (
    "", ":BLPTCH_CAD", ":BLPTCH_INCL", ":CYLLTH_F",
    ":CYLLTH_LR", ":CYLLTH_RR", ":SRCGAP_L", ":SRCGAP_R", ":SRCPTCH",
)

# Colon-separated nodes accessed directly on the beam path
_NB_DIRECT_NODES = (
    "BEAMSTAT", "BEAMSTATF", "CURRENT", "ETA1", "F0",
    "FIRED", "FIRED:INFO", "GAS", "HEADPOINT", "IFIX", "INTERCEPT",
    "IONSRCTYPE", "MODE", "MODULATION", "NBSHOT", "NBVAC_SCALAR",
    "NEUT_GAS_FL", "PABS", "PERVEANCE", "PINJ_SCALAR", "POWER", "PSHINE",
    "PTDATA_CAL", "PTDATA_CALF", "PTDATA_RAW", "PTDATA_RAWF", "REAL32",
    "SHINE_THRU", "SING_SRC_FAC", "SLOPE", "SYNC", "TE",
    "THRESHOLD", "THRESHOLD:INFO", "VBEAM", "VBEAMF",
    "VOLTAGE", "VOLTAGE_CAL", "VOLTAGE_CALF",
)

# Injection power/timing nodes whose names embed the beam label
_NB_BEAM_SPECIFIC = {
    "NB15L": ("PINJF_15L", "PINJ_15L", "TINJ_15L"),
    "NB15R": ("PINJF_15R", "PINJ_15R", "TINJ_15R"),
    "NB21L": ("PINJF_21L", "PINJ_21L", "TINJ_21L"),
    "NB21R": ("PINJF_21R", "PINJ_21R", "TINJ_21R"),
    "NB30L": ("PINJF_30L", "PINJ_30L", "TINJ_30L"),
    "NB30R": ("PINJF_30R", "PINJ_30R", "TINJ_30R"),
    "NB33L": ("PINJF_33L", "PINJ_33L", "TINJ_33L"),
    "NB33R": ("PINJF_33R", "PINJ_33R", "TINJ_33R"),
}

NBI_SIGNALS: dict = {}
for _beam in _NB_BEAMS:
    _base = f"TOP.NB.{_beam}"
    for _sfx in _NB_BEAMTARGET_SUFFIXES:
        _node = f"{_base}.BEAMTARGET{_sfx}"
        NBI_SIGNALS[rf"\D3D::{_node}"] = _mds(_node, "d3d")
    for _sfx in _NB_OANB_SUFFIXES:
        _node = f"{_base}.OANB{_sfx}"
        NBI_SIGNALS[rf"\D3D::{_node}"] = _mds(_node, "d3d")
    for _n in _NB_DIRECT_NODES:
        _node = f"{_base}:{_n}"
        NBI_SIGNALS[rf"\D3D::{_node}"] = _mds(_node, "d3d")
    for _n in _NB_BEAM_SPECIFIC[_beam]:
        _node = f"{_base}:{_n}"
        NBI_SIGNALS[rf"\D3D::{_node}"] = _mds(_node, "d3d")

# ── ECH (12 gyrotrons x 7 nodes) ─────────────────────────────────────────────
# Each gyrotron has a 4-5 char prefix used in node names.
# HAN uses DLPWRC (diode-laser power) instead of FPWRC (forward power).
_ECH_GYROTRONS = {
    "BORIS":     "ECBOR",
    "CHEWBACCA": "ECCHE",
    "DOROTHY":   "ECDOR",
    "HAN":       "ECHAN",
    "KATYA":     "ECKAT",
    "LEIA":      "ECLEI",
    "LION":      "ECLIO",
    "LUKE":      "ECLUK",
    "NASA":      "ECNAS",
    "NATASHA":   "ECNAT",
    "R2D2":      "ECR2D",
    "SCARECROW": "ECSCA",
}
_ECH_SUFFIXES_STD = ("AZIANG", "FPWRC", "POLANG", "POLCNT", "STAT", "TORCNT", "XMFRAC")
_ECH_SUFFIXES_HAN = ("AZIANG", "DLPWRC", "POLANG", "POLCNT", "STAT", "TORCNT", "XMFRAC")

ECH_SIGNALS: dict = {}
for _gyr, _abbr in _ECH_GYROTRONS.items():
    _sfxs = _ECH_SUFFIXES_HAN if _gyr == "HAN" else _ECH_SUFFIXES_STD
    for _sfx in _sfxs:
        _node = f"TOP.RF.ECH.{_gyr}:{_abbr}{_sfx}"
        ECH_SIGNALS[rf"\D3D::{_node}"] = _mds(_node, "d3d")

# ── ICH ───────────────────────────────────────────────────────────────────────
ICH_SIGNALS = {
    r"\D3D::TOP.RF.ICH:ICHPWR":            _mds("TOP.RF.ICH:ICHPWR", "d3d"),
    r"\D3D::TOP.RF.ICH:ICHPWR:MULTIPLIER": _mds("TOP.RF.ICH:ICHPWR:MULTIPLIER", "d3d"),
    r"\D3D::TOP.RF.ICH:ICHPWR:UNITS":      _mds("TOP.RF.ICH:ICHPWR:UNITS", "d3d"),
}

# ── Gas Injection (11 valves x 7 nodes) ──────────────────────────────────────
_GAS_VALVES = ("GASA", "GASB", "GASC", "GASD", "GASE", "LOB1", "LOB2", "PFX1", "PFX2", "PFX3", "UOB")
_GAS_NODES  = ("CALC_FLOW", "FLOW", "P1", "P2", "PCS", "RAW", "SHOT_CALIB")

GAS_SIGNALS = {
    rf"\D3D::TOP.NEUTRALS.GASFLOW.{valve}:{node}":
        _mds(f"TOP.NEUTRALS.GASFLOW.{valve}:{node}", "d3d")
    for valve in _GAS_VALVES for node in _GAS_NODES
}

# ── EFIT01 (magnetic equilibrium, 14 signals) ─────────────────────────────────
EFIT_SIGNALS = {
    rf"\EFIT01::{node}": _mds(node, "efit01")
    for node in (
        "AMINOR", "ALPHA", "BETAN", "GAPIN", "PSIRZ", "PSIN",
        "RHOVN", "PRES", "Q95", "QMIN", "R0", "KAPPA", "TRITOP", "TRIBOT",
    )
}

# ── MHD (toroidal mode amplitudes) ───────────────────────────────────────────
MHD_SIGNALS = {
    r"\MHD::N1RMS": _mds("N1RMS", "mhd"),
    r"\MHD::N2RMS": _mds("N2RMS", "mhd"),
}

# ── AOT (shape parameters) ───────────────────────────────────────────────────
AOT_SIGNALS = {
    r"\AOT::TRIANGULARITY_U": _mds("TRIANGULARITY_U", "aot"),
    r"\AOT::TRIANGULARITY_L": _mds("TRIANGULARITY_L", "aot"),
    r"\AOT::Q":                _mds("Q", "aot"),
}

# ── SPECTROSCOPY tree: divertor spectroscopy + bolometry power ────────────────
DIVSPRED_SIGNALS = {
    rf"\SPECTROSCOPY::TOP.DIVSPRED.RAW:{sig}":
        _mds(f"TOP.DIVSPRED.RAW:{sig}", "spectroscopy")
    for sig in (
        "CIII_977", "CII_651", "CII_904", "CIV_1550", "DLYA_1215",
        "DLYB_1025", "INTENSITIES", "INT_TIMES", "START_TIMES", "WAVELENGTHS",
    )
}

BOLOM_PWR_SIGNALS = {
    rf"\SPECTROSCOPY::TOP.PRAD.BOLOM.PRAD_01.POWER:BOL_{side}{i:02d}_P":
        _mds(f"TOP.PRAD.BOLOM.PRAD_01.POWER:BOL_{side}{i:02d}_P", "spectroscopy")
    for side in ("L", "U") for i in range(1, 25)
}

# ── Video signals (tangtv + irtv, from chiron — available via OSDF) ───────────
VIDEO_SIGNALS = {
    # Tangential visible cameras
    r"\TANGTV::TOP.TANGTV:LODIV_240RM1:PAR:INTENSIFIED:VIDEO_IMAGES":
        _mds("TOP.TANGTV:LODIV_240RM1:PAR:INTENSIFIED:VIDEO_IMAGES", "tangtv"),
    r"\TANGTV::TOP.TANGTV:LODIV_240RM1:PAR:STANDARD:VIDEO_IMAGES":
        _mds("TOP.TANGTV:LODIV_240RM1:PAR:STANDARD:VIDEO_IMAGES", "tangtv"),
    r"\TANGTV::TOP.TANGTV:LODIV_240RM1:PERP:STANDARD:VIDEO_IMAGES":
        _mds("TOP.TANGTV:LODIV_240RM1:PERP:STANDARD:VIDEO_IMAGES", "tangtv"),
    r"\TANGTV::TOP.TANGTV:UPDIV_225RP1:PERP:STANDARD:VIDEO_IMAGES":
        _mds("TOP.TANGTV:UPDIV_225RP1:PERP:STANDARD:VIDEO_IMAGES", "tangtv"),
    r"\TANGTV::TOP.TANGTV:UPDIV_0RP1:PERP:STANDARD:VIDEO_IMAGES":
        _mds("TOP.TANGTV:UPDIV_0RP1:PERP:STANDARD:VIDEO_IMAGES", "tangtv"),
    r"\TANGTV::TOP.TANGTV:UPDIV_225RP1:PAR:STANDARD:VIDEO_IMAGES":
        _mds("TOP.TANGTV:UPDIV_225RP1:PAR:STANDARD:VIDEO_IMAGES", "tangtv"),
    r"\TANGTV::TOP.TANGTV:UPDIV_0RP1:PAR:STANDARD:VIDEO_IMAGES":
        _mds("TOP.TANGTV:UPDIV_0RP1:PAR:STANDARD:VIDEO_IMAGES", "tangtv"),
    # Infrared cameras
    r"\IRTV::TOP.IRTV:BIAS_105RM1:DIGITAL_CAM:DIGITAL_RAW":
        _mds("TOP.IRTV:BIAS_105RM1:DIGITAL_CAM:DIGITAL_RAW", "irtv"),
    r"\IRTV::TOP.IRTV:LOCEN_315RM1:DIGITAL_CAM:DIGITAL_RAW":
        _mds("TOP.IRTV:LOCEN_315RM1:DIGITAL_CAM:DIGITAL_RAW", "irtv"),
    r"\IRTV::TOP.IRTV:LODIV_165RP2:DIGITAL_CAM:DIGITAL_RAW":
        _mds("TOP.IRTV:LODIV_165RP2:DIGITAL_CAM:DIGITAL_RAW", "irtv"),
    r"\IRTV::TOP.IRTV:LODIV_60RP2:DIGITAL_CAM:DIGITAL_RAW":
        _mds("TOP.IRTV:LODIV_60RP2:DIGITAL_CAM:DIGITAL_RAW", "irtv"),
    r"\IRTV::TOP.IRTV:PERI75R0:DIGITAL_CAM:DIGITAL_RAW":
        _mds("TOP.IRTV:PERI75R0:DIGITAL_CAM:DIGITAL_RAW", "irtv"),
    r"\IRTV::TOP.IRTV:UPCEN_300RP1:DIGITAL_CAM:DIGITAL_RAW":
        _mds("TOP.IRTV:UPCEN_300RP1:DIGITAL_CAM:DIGITAL_RAW", "irtv"),
    r"\IRTV::TOP.IRTV:UPDIV_225RM2:DIGITAL_CAM:DIGITAL_RAW":
        _mds("TOP.IRTV:UPDIV_225RM2:DIGITAL_CAM:DIGITAL_RAW", "irtv"),
}
