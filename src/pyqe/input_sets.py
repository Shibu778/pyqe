# Set of inputs for work

# input1: Basic inputs for relaxing a slab model using PBE functional, DFT-D3 dispersion correction, and ONCV_PBE pseudopotentials.
# This input set is suitable for slab models with a vacuum layer.
input1 = {
    "calculation": "relax",
    "restart_mode": "from_scratch",
    "nstep": 200,
    "prefix": "pbe",
    "ecutwfc": 30,
    "ecutrho": 300,
    "etot_conv_thr": 1e-5,
    "forc_conv_thr": 1e-2,
    "conv_thr": 1e-8,
    "ibrav": 0,
    "vdw_corr": "dft-d3",
}
