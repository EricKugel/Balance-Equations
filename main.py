# Eric Kugel
from parseFormula import getAtomCounts, parseMolecule
import numpy as np
import sympy as sp

# reactants = ["Ca3(PO4)2", "SiO2"]
# products = ["P4O10", "CaSiO3"]
reactants = ["KClO3"]
products = ["KCl", "O2"]
def promptChemicals():
  global reactants, products
  reactants = []
  products = []
  for i in range(int(input("How many reactants are there?: "))):
    reactants.append(input("Enter a reactant: "))
  for i in range(int(input("How many products are there?: "))):
    products.append(input("Enter a product: "))
# promptChemicals()
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
while len(array) < len(array[0]):
  array.append([0 for i in range(len(array[0]))])
matrix = sp.Matrix(array)
matrixRref = matrix.rref()[0]
lastCol = matrixRref.col(-1)

coefficients = np.rot90(np.array(lastCol).astype(np.float64))[0]
print(coefficients)

if np.any(coefficients == 0.0):
  # Don't judge
  min = 1000000
  for coefficient in list(coefficients):
    if coefficient != 0 and coefficient < min:
      min = coefficient
  scalar = 1 / min
  for index in range(len(coefficients)):
    if coefficients[index] == 0.0:
      coefficients[index] = scalar
    else:
      coefficients[index] *= scalar

scalar = np.lcm.reduce([coefficients])
for index in range(len(coefficients)):
  coefficients[index] *= scalar

output = ""
moleculeIndex = 0
for reactant in reactants:
  if coefficients[moleculeIndex] != 1:
    output += str(coefficients[moleculeIndex])
  output += reactant
  output += " + "
  moleculeIndex += 1

output = output[:-2]
output += "--> "

for product in products:
  if coefficients[moleculeIndex] != 1:
    output += str(coefficients[moleculeIndex])
  output += reactant
  output += " + "
  moleculeIndex += 1

output = output[:-3]
print(output)