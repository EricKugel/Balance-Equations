from main import balanceEquation

QUESTIONS = [
    (["N2", "H2"], ["NH3"]),
    (["KClO3"], ["KCl", "O2"]),
    (["NaCl", "F2"], ["NaF", "Cl2"]),
    (["H2", "O2"], ["H2O"]),
    (["Pb(OH)2", "HCl"], ["H2O", "PbCl2"]),
    (["AlBr3", "K2SO4"], ["KBr", "Al2(SO4)3"]),
    (["CH4", "O2"], ["CO2", "H2O"]),
    (["C3H8", "O2"], ["CO2", "H2O"]),
    (["C8H18", "O2"], ["CO2", "H2O"]),
    (["FeCl3", "NaOH"], ["Fe(OH)3", "NaCl"]),
    (["P", "O2"], ["P2O5"]),
    (["Na", "H2O"], ["NaOH", "H2"]),
    (["Ag2O"], ["Ag", "O2"]),
    (["S8", "O2"], ["SO3"]),
    (["CO2", "H2O"], ["C6H12O6", "O2"]),
    (["K", "MgBr"], ["KBr", "Mg"]),
    (["HCl", "CaCO3"], ["CaCl2", "H2O", "CO2"]),
    (["HNO3", "NaHCO3"], ["NaNO3", "H2O", "CO2"]),
    (["H2O", "O2"], ["H2O2"]),
    (["NaBr", "CaF2"], ["NaF", "CaBr2"]),
    (["H2SO4", "NaNO2"], ["HNO2", "Na2SO4"]),
]

for question in QUESTIONS:
    print(balanceEquation(question[0], question[1]))

print(balanceEquation(["KNO3", "C12H22O11"], ["N2", "CO2", "H2O", "K2CO3"]))