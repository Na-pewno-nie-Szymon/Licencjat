import pandas as pd

# 1. Definicje z poprzednich kroków
nucleotides = ('U', 'C', 'A', 'G')
aa_sequence = (
    "Phe Phe Leu Leu Ser Ser Ser Ser Tyr Tyr Stop Stop Cys Cys Stop Trp "
    "Leu Leu Leu Leu Pro Pro Pro Pro His His Gln Gln Arg Arg Arg Arg "
    "Ile Ile Ile Met Thr Thr Thr Thr Asn Asn Lys Lys Ser Ser Arg Arg "
    "Val Val Val Val Ala Ala Ala Ala Asp Asp Glu Glu Gly Gly Gly Gly"
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

# 2. Generowanie pełnej macierzy
all_aas = list(aminoacid_to_codons.keys()) # Lista wszystkich unikalnych aminokwasów (w tym Stop)
matrix_data = {}

# Pętla przez wszystkie aminokwasy-źródła (wiersze)
for source_aa in all_aas:
    codons = aminoacid_to_codons[source_aa]
    total_mutations = len(codons) * 9 # Każdy kodon daje 9 mutacji punktowych
    
    # Słownik do zliczania wyników mutacji
    mutation_counts = {aa: 0 for aa in all_aas}
    
    # Mutujemy każdy kodon danego aminokwasu
    for codon in codons:
        for i in range(3):
            for n in nucleotides:
                if n != codon[i]:
                    mutated_codon = codon[:i] + n + codon[i+1:]
                    target_aa = genetic_code[mutated_codon]
                    mutation_counts[target_aa] += 1
                    
    # Formatujemy wiersz z wynikami w postaci "Licznik/Mianownik"
    row_probs = {}
    for target_aa in all_aas:
        count = mutation_counts[target_aa]

        prob = count / total_mutations
        row_probs[target_aa] = round(prob, 6)
            
    matrix_data[source_aa] = row_probs

# 3. Tworzymy i wyświetlamy DataFrame z Pandas
df = pd.DataFrame(matrix_data).T # .T zamienia osie (aminokwasy źródłowe jako wiersze)
df = df[all_aas] # Ustawiamy kolumny w tej samej kolejności co wiersze

print("--- Fragment macierzy prawdopodobieństw (pierwsze 5 aminokwasów) ---")
print(df.head())

# Odkomentuj poniższą linijkę, aby zapisać wynik do pliku, który wstawisz do Worda!
df.to_csv("macierz_mutacji.csv")
df.to_excel("macierz_mutacji.xlsx")