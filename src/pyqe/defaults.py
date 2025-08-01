# src/pyqe/defaults.py
# Default settings and constants for the PyQE package
import yaml
from pathlib import Path


def load_config(config_file):
    """Loads configuration from a YAML file."""
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config


# Load the configuration at the start of your script
config_file = Path(__file__).parent.resolve() / "../../config.yaml"
config = load_config(config_file)

# Now you can use the values from the config file
pseudo_directory = config["paths"]["pseudo_dir"]
output_directory = config["paths"]["output_dir"]

# Structure format supported by ASE
ASE_FORMATS = [
    "vasp",
    "cif",
    "xyz",
    "lammps-data",
    "lammps-dump",
    "cube",
    "espresso-in",
    "espresso-out",
    "gpaw-out",
    "json",
    "molden",
    "pdb",
    "traj",
    "xsf",
    # Add more formats as needed from ASE's documentation
]

# unit conversion
bohr2ang = 0.529177
