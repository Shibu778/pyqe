import xmltodict
import json
from ase import Atoms
from ase.constraints import FixAtoms
from ase.io import read, write
from pyqe.defaults import bohr2ang
import os


def xml2json(input_file, output_file, save=False):
    # Load XML file
    with open(input_file, "r", encoding="utf-8") as f:
        xml_content = f.read()

    # Convert to dictionary
    data_dict = xmltodict.parse(xml_content)

    # Save as JSON
    if save:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data_dict, f, indent=4)
        print("XML to JSON conversion successful!!")
    return data_dict


def xml2dict(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        xml_content = f.read()

    # Convert to dictionary
    data_dict = xmltodict.parse(xml_content)
    return data_dict


def extract_last_structure(data, pbc=True, constrain=False):
    try:
        struct_info = data["qes:espresso"]["step"][-1]["atomic_structure"]
    except:
        struct_info = data["qes:espresso"]["step"]["atomic_structure"]
    symbols = [atom["@name"] for atom in struct_info["atomic_positions"]["atom"]]
    positions = [
        list(map(float, atom["#text"].split()))
        for atom in struct_info["atomic_positions"]["atom"]
    ]
    positions = [[p[0] * bohr2ang, p[1] * bohr2ang, p[2] * bohr2ang] for p in positions]
    cell = [tuple(map(float, a.split())) for a in struct_info["cell"].values()]
    cell = [[c[0] * bohr2ang, c[1] * bohr2ang, c[2] * bohr2ang] for c in cell]
    atoms = Atoms(symbols=symbols, positions=positions, cell=cell, pbc=pbc)
    if constrain:
        free_positions = data["qes:espresso"]["input"]["free_positions"]["#text"]
        free_positions = free_positions.split("\n")
        free_positions = [list(map(int, f.split())) for f in free_positions]
        fixed_indices = [
            i for i, free in enumerate(free_positions) if free != [1, 1, 1]
        ]
        constraint = FixAtoms(indices=[0])
        atoms.set_constraint(constraint)
    return atoms


def atoms2poscar(atoms, name="POSCAR_relaxed.vasp", format="vasp"):
    write(name, atoms, format=format)
    print(f"Atoms object written to {name} in {format} format!!")


def xml2laststruct(input_file, filename, pbc=True, constrain=False, format="vasp"):
    data = xml2dict(input_file)
    atoms = extract_last_structure(data, constrain=constrain, pbc=pbc)
    atoms2poscar(atoms, filename, format=format)


def conv_structure(
    input_file,
    output_file,
    inp_format="vasp",
    out_format="xyz",
    overwrite=False,
    verbose=True,
):
    """
    Convert a structure file from one format to another using ASE.

    Args:
        input_file (str): Path to the input structure file.
        output_file (str): Path to the output structure file.
        inp_format (str): Format of the input file (default: "vasp").
        out_format (str): Format of the output file (default: "xyz").
        overwrite (bool): Overwrite output file if it exists (default: False).
        verbose (bool): Print status messages (default: True).

    Returns:
        bool: True if conversion was successful, False otherwise.
    """
    if not os.path.isfile(input_file):
        if verbose:
            print(f"Input file '{input_file}' does not exist.")
        return False

    if os.path.exists(output_file) and not overwrite:
        if verbose:
            print(
                f"Output file '{output_file}' already exists. Use overwrite=True to overwrite."
            )
        return False

    try:
        atoms = read(input_file, format=inp_format)
        write(output_file, atoms, format=out_format)
        if verbose:
            print(
                f"Structure converted from {inp_format} to {out_format} and saved as {output_file}."
            )
        return True
    except Exception as e:
        if verbose:
            print(f"Error during conversion: {e}")
        return False


if __name__ == "__main__":
    input_file = "pbe.xml"
    output_file = "pbe.json"
    data = xml2json(input_file, output_file)
    atoms = extract_last_structure(data, constrain=False)
    atoms2poscar(atoms, name="POSCAR_relaxed.vasp")
