MW = float(input('Moleculare Weight:'))
FinalConc = float(input('Final Conc. in mM:'))
Weight = float(input('Weight in mg:'))
Volume = (Weight/MW)/FinalConc
print (Volume*10**3,"ml")