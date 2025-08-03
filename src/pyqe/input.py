# Python Classes to deal with input files for Quantum ESPRESSO
from ase.io import write, read
from pyqe.defaults import pseudo_directory, output_directory


class qe_input:
    """
    Base class for Quantum ESPRESSO input files.
    """

    def __init__(self, structure_file, input_data, pseudopotentials=None, cell=None):
        self.structure_file = structure_file
        self.atoms = read(structure_file)
        self.pseudopotentials = self.get_pseudopotentials(pseudopotentials)
        self.input_data = self.update_input_data(input_data)
        self.cell = cell
        if self.cell is not None:
            self.atoms.set_cell(self.cell, scale_atoms=True)

    def update_input_data(self, input_data):
        """
        Update the input data with new values.
        """
        if "output_dir" not in input_data:
            input_data["outdir"] = output_directory
        if "pseudo_dir" not in input_data:
            input_data["pseudo_dir"] = pseudo_directory
        if "nat" not in input_data:
            input_data["nat"] = len(self.atoms)
        if "ntyp" not in input_data:
            input_data["ntyp"] = len(set(self.atoms.get_chemical_symbols()))

        return input_data

    def get_pseudopotentials(
        self, pseudopotentials=None, default_pp="ONCV_PBE-1.2.upf"
    ):
        """
        Get the pseudopotentials for the calculation.
        """
        if pseudopotentials is not None:
            self.pseudopotentials = pseudopotentials
            return self.pseudopotentials
        else:
            pseudopotentials = {}
        for atom in set(self.atoms.get_chemical_symbols()):
            pseudopotentials[atom] = atom + "_" + default_pp
        self.pseudopotentials = pseudopotentials
        return self.pseudopotentials

    def write_input(self, filename="pw.in"):
        """
        Write the Quantum ESPRESSO input file.
        """
        write(
            filename,
            self.atoms,
            pseudopotentials=self.pseudopotentials,
            input_data=self.input_data,
            format="espresso-in",
        )
