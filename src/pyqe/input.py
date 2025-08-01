# Python Classes to deal with input files for Quantum ESPRESSO
from ase.io import write, read


class qe_input:
    """
    Base class for Quantum ESPRESSO input files.
    """

    def __init__(self, structure_file, input_data, pseudopotentials=None):
        self.structure_file = structure_file
        self.pseudopotentials = self.get_pseudopotentials(pseudopotentials)
        self.input_data = input_data
        self.atoms = read(structure_file)

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
