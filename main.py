# Eric Kugel
from parseFormula import getAtomCounts, parseMolecule
import numpy as np
import sympy as sp

reactants = ["Ca3(PO4)2", "SiO2"]
products = ["P4O10", "CaSiO3"]
reactantCounts = []
productCounts = []

allAtoms = []
for molecule in reactants:
  atomCounts = getAtomCounts(parseMolecule(molecule))
  reactantCounts.append(atomCounts)
  for atom in atomCounts.keys():
    if not atom in allAtoms:
      allAtoms.append(atom)
for molecule in products:
  atomCounts = getAtomCounts(parseMolecule(molecule))
  productCounts.append(atomCounts)

atoms = {}
for atom in allAtoms:
  atoms[atom] = []
  for atomCount in reactantCounts:
    try:
      atoms[atom].append(atomCount[atom])
    except:
      atoms[atom].append(0)
  for atomCount in productCounts:
    try:
      atoms[atom].append(atomCount[atom] * -1)
    except:
      atoms[atom].append(0)

array = []
for atom, value in atoms.items():
  array.append(value)
matrix = sp.Matrix(array)
matrixRref = matrix.rref()[0]
lastCol = matrixRref.col(-1)

npArray = np.array(lastCol).astype(np.float64)
print(npArray)