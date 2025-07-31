
import xmltodict
import json
from ase import Atoms
from ase.constraints import FixAtoms
from ase.io import read, write

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

def xml2dict(input_file):
  with open(input_file, 'r', encoding='utf-8') as f:
      xml_content = f.read()

  # Convert to dictionary
  data_dict = xmltodict.parse(xml_content)
  return data_dict

def extract_last_structure(data, pbc = True, constrain=False):
  struct_info = data['qes:espresso']['step'][-1]['atomic_structure']
  symbols = [atom['@name'] for atom in struct_info['atomic_positions']['atom']]
  positions = [list(map(float, atom['#text'].split())) for atom in struct_info['atomic_positions']['atom']]
  cell = [tuple(map(float, a.split())) for a in struct_info['cell'].values()]
  atoms = Atoms(symbols=symbols, positions = positions, cell=cell, pbc=pbc)
  if constrain:
    try:
      free_positions = data['qes:espresso']['input']['free_positions']['#text']
      free_positions = free_positions.split('\n')
      free_positions = [list(map(int, f.split())) for f in free_positions]
      fixed_indices = [i for i, free in enumerate(free_positions) if free != [1, 1, 1]]
      constraint = FixAtoms(indices=[0])
      atoms.set_constraint(constraint)
    except:
      print("Unable to set the constrained in atoms!!")
  return atoms

def atoms2poscar(atoms, name="POSCAR_relaxed.vasp"):
  write(name, atoms, format='vasp')
  print(f"Atoms object written to {name}!!")

def xml2relaxedposcar(input_file, filename, constrain=False, pbc=True):
  data = xml2dict(input_file)
  atoms = extract_last_structure(data, constrain=constrain, pbc=pbc)
  atoms2poscar(atoms, name=filename)
  return atoms

if __name__ == "__main__":
  input_file = "pbe.xml"
  output_file = "pbe.json"
  data = xml2json(input_file, output_file)
  atoms = extract_last_structure(data, constrain=True)
  atoms2poscar(atoms, name="POSCAR_relaxed.vasp")
