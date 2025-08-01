
import xmltodict
import json
from ase import Atoms
from ase.constraints import FixAtoms
from ase.io import read, write

# unit conversion
bohr2ang = 0.529177

def xml2json(input_file, output_file):
  # Load XML file
  with open(input_file, 'r', encoding='utf-8') as f:
      xml_content = f.read()
  
  # Convert to dictionary
  data_dict = xmltodict.parse(xml_content)
  
  # Save as JSON
  with open(output_file, 'w', encoding='utf-8') as f:
      json.dump(data_dict, f, indent=4)
  print("XML to JSON conversion successful!!")
  return data_dict

def extract_last_structure(data, pbc = True, constrain=False):
  try: 
    struct_info = data['qes:espresso']['step'][-1]['atomic_structure']
  except:
    struct_info = data['qes:espresso']['step']['atomic_structure']
  symbols = [atom['@name'] for atom in struct_info['atomic_positions']['atom']]
  positions = [list(map(float, atom['#text'].split())) for atom in struct_info['atomic_positions']['atom']]
  positions = [[p[0]*bohr2ang, p[1]*bohr2ang, p[2]*bohr2ang] for p in positions]
  cell = [tuple(map(float, a.split())) for a in struct_info['cell'].values()]
  cell = [[c[0]*bohr2ang, c[1]*bohr2ang, c[2]*bohr2ang] for c in cell]
  atoms = Atoms(symbols=symbols, positions = positions, cell=cell, pbc=pbc)
  if constrain:
    free_positions = data['qes:espresso']['input']['free_positions']['#text']
    free_positions = free_positions.split('\n')
    free_positions = [list(map(int, f.split())) for f in free_positions]
    fixed_indices = [i for i, free in enumerate(free_positions) if free != [1, 1, 1]]
    constraint = FixAtoms(indices=[0])
    atoms.set_constraint(constraint)
  return atoms

def atoms2poscar(atoms, name="POSCAR_relaxed.vasp"):
  write(name, atoms, format='vasp')
  print(f"Atoms object written to {name}!!")

if __name__ == "__main__":
  input_file = "pbe.xml"
  output_file = "pbe.json"
  data = xml2json(input_file, output_file)
  atoms = extract_last_structure(data, constrain=False)
  atoms2poscar(atoms, name="POSCAR_relaxed.vasp")
