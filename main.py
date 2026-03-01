nucletides = ('U', 'C', 'A', 'G')

# Pełna lista 64 "wyników" w kolejności, w jakiej wygenerują się kodony 
# (czyli najpierw UUU, UUC, UUA, UUG, potem UCU, UCC... itd.)
# Dodałem brakujący 'Trp'!
aa_sequence = (
    "Phe Phe Leu Leu "   # U U (U,C,A,G)
    "Ser Ser Ser Ser "   # U C (U,C,A,G)
    "Tyr Tyr Stop Stop " # U A (U,C,A,G)
    "Cys Cys Stop Trp "  # U G (U,C,A,G)
    
    "Leu Leu Leu Leu "   # C U (U,C,A,G)
    "Pro Pro Pro Pro "   # C C (U,C,A,G)
    "His His Gln Gln "   # C A (U,C,A,G)
    "Arg Arg Arg Arg "   # C G (U,C,A,G)
    
    "Ile Ile Ile Met "   # A U (U,C,A,G)
    "Thr Thr Thr Thr "   # A C (U,C,A,G)
    "Asn Asn Lys Lys "   # A A (U,C,A,G)
    "Ser Ser Arg Arg "   # A G (U,C,A,G)
    
    "Val Val Val Val "   # G U (U,C,A,G)
    "Ala Ala Ala Ala "   # G C (U,C,A,G)
    "Asp Asp Glu Glu "   # G A (U,C,A,G)
    "Gly Gly Gly Gly"    # G G (U,C,A,G)
).split()

genetic_code = {}
index = 0

for n1 in nucletides:
    for n2 in nucletides:
        for n3 in nucletides:
            codon = n1 + n2 + n3

            genetic_code[codon] = aa_sequence[index]
            index += 1



print(genetic_code['UUU'])