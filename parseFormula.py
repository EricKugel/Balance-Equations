# Balance an equation
# Eric Kugel

def getParenthesisBlockAt(index, block):
  endIndex = index + 1
  counter = 1
  while counter != 0:
    if block[endIndex] == "(":
      counter += 1
    elif block[endIndex] == ")":
      counter -= 1
    endIndex += 1
  return block[index + 1: endIndex - 1]

def parseMolecule(molecule):
  index = 0
  moleculeObj = []
  while index < len(molecule):
    character = molecule[index]
    if character == "(":
      block = getParenthesisBlockAt(index, molecule)
      moleculeObj.append(parseMolecule(block))
      index += len(block) + 2
    elif character.isnumeric():
        numberString = ""
        while index < len(molecule) and molecule[index].isnumeric():
          numberString += molecule[index]
          index += 1
        moleculeObj.append(int(numberString))
    elif character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
      elementString = character
      index += 1
      while index < len(molecule) and molecule[index] in "abcdefghijklmnopqrstuvwxyz":
        elementString += molecule[index]
        index += 1
      moleculeObj.append(elementString)
    else:
      index += 1
  return moleculeObj

def getAtomCounts(moleculeObj):
  atomCounts = {}
  for index in range(len(moleculeObj)):
    obj = moleculeObj[index]
    if type(obj) is str:
      count = 1
      if(index < len(moleculeObj) - 1 and type(moleculeObj[index + 1]) is int):
        count = moleculeObj[index + 1]
      if obj in atomCounts.keys():
        atomCounts[obj] += count
      else:
        atomCounts[obj] = count
    elif type(obj) is list:
      count = 1
      if(index < len(moleculeObj) - 1 and type(moleculeObj[index + 1]) 
         is int):
        count = moleculeObj[index + 1]
      for subAtom, subCount in getAtomCounts(obj).items():
        if subAtom in atomCounts.keys():
          atomCounts[subAtom] += subCount * count
        else:
          atomCounts[subAtom] = subCount * count
  return atomCounts