# Eric Kugel
from parseFormula import getAtomCounts, parseMolecule
import numpy as np
import sympy as sp
from fractions import Fraction

def balanceEquation(reactants, products):
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
  matrixLastCol = np.rot90(np.array(matrixRref.col(-1)).astype(float))[0]
  coefficients = []
  for item in matrixLastCol:
    coefficients.append(Fraction(abs(item)).limit_denominator())

  if 0 in coefficients:
    min = 1
    for coefficient in list(coefficients):
      if coefficient != 0 and coefficient < min:
        min = coefficient
    scalar = Fraction(1, min)
    for index in range(len(coefficients)):
      if coefficients[index] == 0:
        coefficients[index] = scalar
      else:
        coefficients[index] = coefficients[index] * scalar

  denominators = []
  for co in coefficients:
    denominators.append(co.denominator)
  lcm = np.lcm.reduce(denominators)
  for i in range(len(coefficients)):
    coefficients[i] *= lcm

  output = ""
  moleculeIndex = 0
  for reactant in reactants:
    if coefficients[moleculeIndex] != 1:
      output += str(int(coefficients[moleculeIndex]))
    output += reactant
    output += " + "
    moleculeIndex += 1

  output = output[:-2]
  output += "--> "

  for product in products:
    if coefficients[moleculeIndex] != 1:
      output += str(int(coefficients[moleculeIndex]))
    output += product
    output += " + "
    moleculeIndex += 1

  output = output[:-3]
  return output