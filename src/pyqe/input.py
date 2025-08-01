# Python Classes to deal with input files for Quantum ESPRESSO
from ase.io import write, read


class qe_input:
    """
    Base class for Quantum ESPRESSO input files.
    """

    def __init__(self, atoms, pseudopotentials, input_data):
        self.atoms = atoms
        self.pseudopotentials = pseudopotentials
        self.input_data = input_data

    def write_input(self, filename):
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
