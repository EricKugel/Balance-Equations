"""
Author: Eric Kugel
3/17/22

I'm currently taking AP Computer Science. If you think this is
cool, consider trying a programming class!
"""
from parseFormula import getAtomCounts, parseMolecule
import numpy as np
import sympy as sp
from fractions import Fraction

def balanceEquation(reactants, products):
  reactantCounts = []
  productCounts = []

  """
  This code uses methods in the parseFormula file to analyze the molecules and count
  how many of each element are in it.
  """
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

  """
  If you are given xKClO3 --> yKCl + zO2, you know that the number of K atoms in the
  reactants is x * 1 and in the products is y * 1. Therefore, x = y. This can be
  rewritten as 1x + -1y = 0. This is what the code below is doing. Doing this for all 
  the elements means you can solve for x, y, and z using a system of equations.
  """
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

  """
  After we get all the equations for our system of equations, we can create a matrix with
  a row for each element and a column for each molecule and solve the system using guassian
  elimination. The reduced row echelon form will have the answers in the last column, so 
  we take them out and store them in the coefficients list as fractions.
  """
  array = []
  for atom, value in atoms.items():
    array.append(value)
  # If the array isn't a square, make it a square by adding rows of zeroes.
  while len(array) < len(array[0]):
    array.append([0 for i in range(len(array[0]))])
  matrix = sp.Matrix(array)
  matrixRref = matrix.rref()[0]
  matrixLastCol = np.rot90(np.array(matrixRref.col(-1)).astype(float))[0]
  coefficients = []
  for item in matrixLastCol:
    coefficients.append(Fraction(abs(item)).limit_denominator())

  """
  Getting a zero in rref means there are infinitely possible solutions. That
  makes sense in chemistry, becuase 2Na + Cl2 --> 2NaCl is the same as 
  4Na + 2Cl2 --> 2NaCl. We can set the zero to be the reciprocral of the
  smallest fraction and scale the others to match it.
  """
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

  """
  This code removes any fractions by multiplying everything by the least
  common denominator.
  """
  denominators = []
  for co in coefficients:
    denominators.append(co.denominator)
  lcd = np.lcm.reduce(denominators)
  for i in range(len(coefficients)):
    coefficients[i] *= lcd

  """
  This code just formats and returns the result.
  """
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

# If you're lacking inspiration...
# K4(Fe(SCN)6) + K2Cr2O7 + H2SO4 --> Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3
print("Enter an equation. For example: Na + Cl2 --> NaCl")
inputtedText = input().strip()
reactantAndProduct = inputtedText.split(" --> ")
print(balanceEquation(reactantAndProduct[0].split(" + "), reactantAndProduct[1].split(" + ")))