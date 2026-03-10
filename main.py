import pandas as pd

# 1. Definicje
nucleotides = ('U', 'C', 'A', 'G')

# ZMIANA: Zastąpiono kody 3-literowe 1-literowymi (Stop to '*')
aa_sequence = (
    "F F L L S S S S Y Y * * C C * W "
    "L L L L P P P P H H Q Q R R R R "
    "I I I M T T T T N N K K S S R R "
    "V V V V A A A A D D E E G G G G"
).split()

genetic_code = {}
index = 0
for n1 in nucleotides:
    for n2 in nucleotides:
        for n3 in nucleotides:
            codon = n1 + n2 + n3
            genetic_code[codon] = aa_sequence[index]
            index += 1

aminoacid_to_codons = {}
for codon, aa in genetic_code.items():
    if aa not in aminoacid_to_codons:
        aminoacid_to_codons[aa] = []
    aminoacid_to_codons[aa].append(codon)

# 2. Generowanie pełnej macierzy z ułamkami dziesiętnymi
all_aas = list(aminoacid_to_codons.keys())
matrix_data = {}

for source_aa in all_aas:
    codons = aminoacid_to_codons[source_aa]
    total_mutations = len(codons) * 9
    
    mutation_counts = {aa: 0 for aa in all_aas}
    
    for codon in codons:
        for i in range(3):
            for n in nucleotides:
                if n != codon[i]:
                    mutated_codon = codon[:i] + n + codon[i+1:]
                    target_aa = genetic_code[mutated_codon]
                    mutation_counts[target_aa] += 1
                    
    # Formatujemy wiersz z wynikami jako ułamki dziesiętne
    row_probs = {}
    for target_aa in all_aas:
        count = mutation_counts[target_aa]
        prob = count / total_mutations
        row_probs[target_aa] = round(prob, 6)
            
    matrix_data[source_aa] = row_probs

# 3. Tworzymy i wyświetlamy DataFrame z Pandas
df = pd.DataFrame(matrix_data).T 
df = df[all_aas] 

print("--- Fragment macierzy prawdopodobieństw (kody 1-literowe) ---")
print(df.head())

# Zapis do pliku
df.to_csv("macierz_prawdopodobienstw_1_literowa.csv")