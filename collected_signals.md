# DIII-D MDSplus Data Collection Reference

This document describes all MDSplus signals fetched by the `data_fetching_omega` pipeline. Data is pulled from two servers — `atlas.gat.com` and `chiron.gat.com` — defined in `config_atlas.yaml` and `config_chiron.yaml` respectively.

Shot numbers are supplied at runtime via either a `shots_to_process.txt` file or a manually specified range; no shot list is hardcoded in the scripts.

---

## Server: `atlas.gat.com`

### Tree: `d3d`

#### Electron Diagnostics

**Thomson Scattering** (`TS.BLESSED`) — density and temperature profiles:
- `CORE:DENSITY`, `CORE:TEMP`
- `TANGENTIAL:DENSITY`, `TANGENTIAL:TEMP`
- `DIVERTOR:DENSITY`, `DIVERTOR:TEMP`

**Electron Cyclotron Emission (ECE)**:
- `TECEF01`–`TECEF48` (48 channels)

**BCI Interferometry** — line-integrated electron density:
- `DPD.R0:DENUF`, `DPD.V1:DENUF`, `DPD.V2:DENUF`, `DPD.V3:DENUF`

#### Ion Diagnostics (Charge Exchange Recombination — CER)

**Tangential system** (48 channels each):
- `CERAUTO.TANGENTIAL.CHANNEL01`–`CHANNEL48:TEMP`
- `CERAUTO.TANGENTIAL.CHANNEL01`–`CHANNEL48:ROT`

**Vertical system** (32 channels each):
- `CERAUTO.VERTICAL.CHANNEL01`–`CHANNEL32:TEMP`
- `CERAUTO.VERTICAL.CHANNEL01`–`CHANNEL32:ROT`

#### Soft X-Ray (SXR) Arrays

10 arrays, each with 32 signal channels plus a timebase:

| Array | Signals |
|---|---|
| `SX165R1F` | `SX165R1F01`–`32`, `TIMEBASE` |
| `SX165R1S` | `SX165R1S01`–`32`, `TIMEBASE` |
| `SX195R1F` | `SX195R1F01`–`32`, `TIMEBASE` |
| `SX195R1S` | `SX195R1S01`–`32`, `TIMEBASE` |
| `SX45R1F` | `SX45R1F01`–`32`, `TIMEBASE` |
| `SX45R1S` | `SX45R1S01`–`32`, `TIMEBASE` |
| `SX90RM1F` | `SX90RM1F01`–`32`, `TIMEBASE` |
| `SX90RM1S` | `SX90RM1S01`–`32`, `TIMEBASE` |
| `SX90RP1F` | `SX90RP1F01`–`32`, `TIMEBASE` |
| `SX90RP1S` | `SX90RP1S01`–`32`, `TIMEBASE` |

#### Motional Stark Effect (MSE)

- `ANALYSIS_01:MSEP01`–`MSEP69` (69 channels)
- `ANALYSIS_01:MSEP01`–`MSEP69:TIME` (per-channel timebases)

#### Bolometry (Raw Voltage)

- `PRAD.BOLOM.RAW:BOL_L01`–`BOL_L24_V` (lower array, 24 channels)
- `PRAD.BOLOM.RAW:BOL_U01`–`BOL_U24_V` (upper array, 24 channels)

#### Visible Bremsstrahlung (Zeff)

- `VB.TUBE01`–`TUBE24`
- `VB.CHORD01`–`CHORD24`
- `VB.ZEFF:ZEFF_01`–`ZEFF_24`

#### Filterscopes (PMT)

- `FILTERSCOPE.PMT01`–`PMT96` (96 channels)

#### Neutron Rates

- `FIP:NEUTRONRATE1`, `NEUTRONRATE3`, `NEUTRONRATE4`, `NEUTRONSRATE`

#### Neutral Beam Injection (NBI)

8 beam sources: `NB15L`, `NB15R`, `NB21L`, `NB21R`, `NB30L`, `NB30R`, `NB33L`, `NB33R`

Each source contains:
- `BEAMTARGET` subtree (~18 nodes)
- `OANB` subtree (~9 nodes)
- ~43 direct beam parameter nodes (power, voltage, species, geometry, etc.)

#### Electron Cyclotron Heating (ECH)

12 gyrotrons, each with ~7 nodes (azimuth, power, polarization angle, etc.):

`BORIS`, `CHEWBACCA`, `DOROTHY`, `HAN`, `KATYA`, `LEIA`, `LION`, `LUKE`, `NASA`, `NATASHA`, `R2D2`, `SCARECROW`

#### Ion Cyclotron Heating (ICH)

- `ICH:ICHPWR`
- `ICH:ICHPWR:MULTIPLIER`
- `ICH:ICHPWR:UNITS`

#### Gas Injection

11 valves, each with ~7 nodes (flow rate, command, etc.):

`GASA`, `GASB`, `GASC`, `GASD`, `GASE`, `LOB1`, `LOB2`, `PFX1`, `PFX2`, `PFX3`, `UOB`

#### I-Coil Toroidal Harmonics

- `ICOIL.TORHARMS.ILN1IAMP`, `ILN2IAMP`, `ILN3IAMP`
- `ICOIL.TORHARMS.IUN1IAMP`, `IUN2IAMP`, `IUN3IAMP`

---

### Tree: `EFIT01` (Magnetic Equilibrium Reconstruction)

`AMINOR`, `ALPHA`, `BETAN`, `GAPIN`, `PSIRZ`, `PSIN`, `RHOVN`, `PRES`, `Q95`, `QMIN`, `R0`, `KAPPA`, `TRITOP`, `TRIBOT`

---

### Tree: `MHD`

- `N1RMS` — n=1 toroidal mode amplitude
- `N2RMS` — n=2 toroidal mode amplitude

---

### Tree: `AOT`

- `TRIANGULARITY_U` — upper triangularity
- `TRIANGULARITY_L` — lower triangularity
- `Q` — safety factor profile

---

### Tree: `SPECTROSCOPY`

**Filterscope channels**:
- `FS01`–`FS08`

**Divertor spectroscopy** (`DIVSPRED.RAW`):
- `CIII_977`, `CII_651`, `CII_904`, `CIV_1550`
- `DLYA_1215`, `DLYB_1025`
- `INTENSITIES`, `INT_TIMES`, `START_TIMES`, `WAVELENGTHS`

**Bolometry power** (`PRAD.BOLOM.PRAD_01.POWER`):
- `BOL_L01`–`BOL_L24_P` (lower array, 24 channels)
- `BOL_U01`–`BOL_U24_P` (upper array, 24 channels)

---

### Tree: `ptdata` (Engineering Signals)

**MPI Magnetic Pickup Coils** (28 signals):

`MPI1A322D`, `MPI3A322D`, `MPI5A322D`, `MPI89A322D`, `MPI79FA322D`, `MPI7FA322D`, `MPI67A322D`, `MPI6NA322D`, `MPI1B322D`, `MPI3B322D`, `MPI5B322D`, `MPI89B322D`, `MPI79B322D`, `MPI7NB322D`, `MPI6FB322D`, `MPI66M322D`, `MPI66M132D`, `MPI66B137D`, `MPI66M312D`, `MPI66B312D`, `MPI66M020D`, `MPI66M097D`, `MPI66M307D`, `MPI1A011D`, `MPI1A274D`, `MPI1A109D`, `MPI1A199D`, `MPI1A341D`

**Beam attenuation**:
- `b1`–`b8`

**Toroidal limiter angles**:
- `TPLANG01`–`TPLANG72` (72 channels)

**C-coil fluxes**:
- `C19F`, `C79F`, `C139F`, `C199F`, `C259F`, `C319F`

**I-coil currents — upper**:
- `IU30F`, `IU90F`, `IU150F`, `IU210F`, `IU270F`, `IU330F`

**I-coil currents — lower**:
- `IL30F`, `IL90F`, `IL150F`, `IL210F`, `IL270F`, `IL330F`

**I-coil harmonic amplitudes** (duplicated from `d3d` tree via ptdata):
- `ILN1IAMP`, `ILN2IAMP`, `ILN3IAMP`, `IUN1IAMP`, `IUN2IAMP`, `IUN3IAMP`

**Beam Emission Spectroscopy (BES)**:
- `BESFU01`–`BESFU64` (64 channels)

**Scalar engineering parameters**:

| Signal | Description |
|---|---|
| `ip` | Plasma current |
| `bt` | Toroidal magnetic field |
| `bcoil` | B-coil signal |
| `pcbcoil` | PC B-coil signal |
| `bmspinj` | Beam stored energy (injected) |
| `bmstinj` | Beam stored energy (total injected) |
| `dssdenest` | Density estimate |
| `dstdenp` | Density (Thomson) |
| `fzns` | Fueling zone neutral source |
| `ipsip` | Plasma current (SIP) |
| `iptipp` | Plasma current (TIPP) |
| `plasticfix` | Plastic fix parameter |

---

## Server: `chiron.gat.com`

### Tree: `tangtv` (Tangential Visible Cameras)

7 video streams:

| Node | View | Polarization | Camera type |
|---|---|---|---|
| `LODIV_240RM1:PAR:INTENSIFIED:VIDEO_IMAGES` | Lower divertor | Parallel | Intensified |
| `LODIV_240RM1:PAR:STANDARD:VIDEO_IMAGES` | Lower divertor | Parallel | Standard |
| `LODIV_240RM1:PERP:STANDARD:VIDEO_IMAGES` | Lower divertor | Perpendicular | Standard |
| `UPDIV_225RP1:PERP:STANDARD:VIDEO_IMAGES` | Upper divertor | Perpendicular | Standard |
| `UPDIV_0RP1:PERP:STANDARD:VIDEO_IMAGES` | Upper divertor | Perpendicular | Standard |
| `UPDIV_225RP1:PAR:STANDARD:VIDEO_IMAGES` | Upper divertor | Parallel | Standard |
| `UPDIV_0RP1:PAR:STANDARD:VIDEO_IMAGES` | Upper divertor | Parallel | Standard |

### Tree: `irtv` (Infrared Cameras)

7 digital camera streams:

| Node | View location |
|---|---|
| `BIAS_105RM1:DIGITAL_CAM:DIGITAL_RAW` | Bias plate, 105° |
| `LOCEN_315RM1:DIGITAL_CAM:DIGITAL_RAW` | Lower center, 315° |
| `LODIV_165RP2:DIGITAL_CAM:DIGITAL_RAW` | Lower divertor, 165° |
| `LODIV_60RP2:DIGITAL_CAM:DIGITAL_RAW` | Lower divertor, 60° |
| `PERI75R0:DIGITAL_CAM:DIGITAL_RAW` | Periscope, 75° |
| `UPCEN_300RP1:DIGITAL_CAM:DIGITAL_RAW` | Upper center, 300° |
| `UPDIV_225RM2:DIGITAL_CAM:DIGITAL_RAW` | Upper divertor, 225° |

---

## Signal Count Summary

| Source | Category | Approx. channel count |
|---|---|---|
| `d3d` / `ptdata` | Thomson scattering (Te, ne) | 12 |
| `d3d` | ECE (Te) | 48 |
| `d3d` | BCI interferometry | 4 |
| `d3d` / `ptdata` | CER (Ti, rotation) | 160 |
| `d3d` | SXR arrays | ~320 |
| `d3d` | MSE | 69 |
| `d3d` | Bolometry (raw + power) | 96 |
| `d3d` | Visible bremsstrahlung / Zeff | 72 |
| `d3d` | Filterscopes | 96 |
| `d3d` | Neutron rates | 4 |
| `d3d` | Neutral beams (8 sources) | ~560 |
| `d3d` | ECH (12 gyrotrons) | ~84 |
| `d3d` | Gas injection (11 valves) | ~77 |
| `d3d` / `ptdata` | I-coil / C-coil / MPI magnetics | ~70 |
| `EFIT01` | Equilibrium reconstruction | 14 |
| `MHD` | Mode numbers | 2 |
| `AOT` | Shape parameters | 3 |
| `SPECTROSCOPY` | Divertor spectroscopy + filterscopes | ~66 |
| `ptdata` | BES | 64 |
| `ptdata` | TPLANG, beam attenuation, scalars | ~97 |
| `tangtv` | Tangential visible video | 7 streams |
| `irtv` | Infrared video | 7 streams |
