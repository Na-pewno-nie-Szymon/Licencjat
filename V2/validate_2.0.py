import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

SUB_MATRIX = 'macierz_prawdopodobienstw_1_literowa.csv'
CHUNK_SIZE = 10000

def generate_plots(input_file: str, output_prefix: str, save_fig: bool, show_fig: bool):
    """Generuje zaawansowane wykresy na podstawie przetworzonych danych."""
    print('\nGenerowanie ulepszonych wykresów wizualizujących wyniki...')
    try:
        # typ mutacji
        df = pd.read_csv(input_file, sep='\t')
        
        col_wild = df.columns[5]
        col_mut = df.columns[6]
        df['Mutation_Type'] = df[col_wild].astype(str) + ' -> ' + df[col_mut].astype(str)

        sns.set_theme(style='whitegrid')
        
        #histogramy
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Wykres lewy liniowy
        sns.histplot(data=df, x='Probability', bins=20, kde=True, color='dodgerblue', ax=axes[0])
        axes[0].set_title('Rozkład prawdopodobieństwa SNP (Skala Liniowa)', fontsize=14)
        axes[0].set_xlabel('Prawdopodobieństwo', fontsize=12)
        axes[0].set_ylabel('Częstotliwość występowania', fontsize=12)
        
        # prawy: Skala logarytmiczna osi X 
        df_nonzero = df[df['Probability'] > 0]
        sns.histplot(data=df_nonzero, x='Probability', bins=20, kde=True, color='salmon', log_scale=(True, False), ax=axes[1])
        axes[1].set_title('Rozkład prawdopodobieństwa SNP (Skala Logarytmiczna)', fontsize=14)
        axes[1].set_xlabel('Prawdopodobieństwo (log)', fontsize=12)
        axes[1].set_ylabel('Częstotliwość występowania', fontsize=12)
        
        plt.tight_layout()
        if save_fig:
            plt.savefig(f'{output_prefix}_histogramy.png', dpi=300, bbox_inches='tight')
            print(f"Zapisano: {output_prefix}_histogramy.png")
        
        # ==========================================
        # 2. WYKRES TOP 15 NAJCZĘSTSZYCH MUTACJI
        # ==========================================
        plt.figure(figsize=(12, 6))
        
        # Zliczamy najczęstsze typy mutacji w pliku i bierzemy 15 pierwszych
        top_mutations = df['Mutation_Type'].value_counts().head(15)
        
        # Tworzymy wykres słupkowy
        sns.barplot(x=top_mutations.values, y=top_mutations.index, palette='viridis', hue=top_mutations.index, legend=False)
        plt.title('Top 15 najczęstszych typów podstawień aminokwasów w bazie (SNP)', fontsize=16)
        plt.xlabel('Liczba wystąpień', fontsize=12)
        plt.ylabel('Typ mutacji (Wild Type -> Zmutowany)', fontsize=12)
        
        plt.tight_layout()
        if save_fig:
            plt.savefig(f'{output_prefix}_top_mutacje.png', dpi=300, bbox_inches='tight')
            print(f"Zapisano: {output_prefix}_top_mutacje.png")

        if show_fig:
            plt.show()
            
        plt.close('all')
        
    except Exception as e:
        print(f"Błąd podczas generowania wykresów: {e}")

def main():
    # CLI argument parser setup
    parser = argparse.ArgumentParser(
        description='Walidacja wariantów SNP na podstawie macierzy prawdopodobieństw',
        epilog='Przykład użycia: python validate_ver_2.0.py -f path/to/file.tsv --save_fig'
    )

    parser.add_argument('-f', '--file', type=str, required=True, help='Ścieżka do pliku z danymi z AliceDB')
    parser.add_argument('-o', '--output', default='results', help='Ścieżka i prefix plików wyjściowych')
    parser.add_argument('--save_fig', action='store_true', help='Zapisz wygenerowane wykresy jako pliki PNG')
    parser.add_argument('--show_fig', action='store_true', help='Wyświetl wykresy na ekranie po przetworzeniu')

    args = parser.parse_args()
    
    print('Wczytywanie macierzy prawdopodobieństw...')
    try:
        sub_matrix = pd.read_csv(SUB_MATRIX, index_col=0)
    except FileNotFoundError:
        print(f"Błąd krytyczny: Nie znaleziono pliku z macierzą '{SUB_MATRIX}'. Upewnij się, że znajduje się w tym samym folderze.")
        return

    def get_probability(row):
        # Pobieranie aminokwasów z odpowiednich kolumn (indeksy 5 i 6 według oryginału)
        wild = row.iloc[5]
        mutated = row.iloc[6]
        
        # Zabezpieczenie przed brakującymi danymi lub dziwnymi znakami z bazy
        if wild in sub_matrix.index and mutated in sub_matrix.columns:
            return sub_matrix.loc[wild, mutated]
        return 0.0
    
    prefix = args.output
    file_all = f'{prefix}_all.tsv'
    file_possible = f'{prefix}_possible.tsv'
    
    first_chunk = True
    
    # Proba oszacowania liczby wierszy do paska postępu (nieobowiązkowe, ale estetyczne)
    try:
        total_rows = sum(1 for _ in open(args.file, 'r', encoding='utf-8')) - 1
        total_chunks = (total_rows // CHUNK_SIZE) + 1
    except:
        total_chunks = None

    print('\nPrzetwarzanie danych wejściowych w paczkach (chunks)...')
    try:
        for chunk in tqdm(pd.read_csv(args.file, sep='\t', chunksize=CHUNK_SIZE), total=total_chunks, desc="Postęp"):
            # Obliczanie prawdopodobieństwa dla wierszy w paczce
            chunk['Probability'] = chunk.apply(get_probability, axis=1)

            # Filtrowanie tylko tych wierszy, gdzie prawdopodobieństwo jest większe od 0
            possible_chunk = chunk[chunk['Probability'] > 0]

            # Zapis do plików TSV (tryb zapisu 'w' dla pierwszej paczki, 'a' dla kolejnych)
            mode = 'w' if first_chunk else 'a'
            header = first_chunk 

            chunk.to_csv(file_all, sep='\t', index=False, mode=mode, header=header)
            possible_chunk.to_csv(file_possible, sep='\t', index=False, mode=mode, header=header)
            
            first_chunk = False
            
    except Exception as e:
        print(f"Wystąpił błąd podczas przetwarzania pliku wejściowego: {e}")
        return
        
    print("\nZakończono analizę i zapis plików TSV!")
    
    # Przekazujemy plik "_all.tsv" do nowej funkcji rysującej wykresy
    generate_plots(file_all, prefix, args.save_fig, args.show_fig)
    print("Skrypt zakończył działanie pomyślnie!")

if __name__ == "__main__":
    main()