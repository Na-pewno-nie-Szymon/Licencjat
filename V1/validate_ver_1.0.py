import pandas as pd
import argparse

import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm

# Constansts
SUB_MATRIX = 'macierz_prawdopodobienstw_1_literowa.csv'
CHUNK_SIZE = 10000

def heatmap(matrix_df, output_prefix):
    plt.figure(figsize=(12,10))
    sns.heatmap(matrix_df, annot=False, cmap="YlOrBr", cbar_kws={'label': 'Prawdopodobieństwo'})
    plt.title("Macierz prawdopobieństw SNP", fontsize=16)
    plt.xlabel("Aminokwas po mutacji")
    plt.ylabel("Aminokwas (Wild Type)")
    plt.savefig(f'{output_prefix}_matrix_heatmap.png')
    plt.close()

def generate_advanced_plots(probs_series, output_prefix):
    fig, (ax1, ax2) = plt.subplot(1, 2, figsize=(16, 6))

    sns.histplot(probs_series, bins=20, kde=True, color='dodgerblue', ax=ax1)
    ax1.set_title('Rozkład prawdopodobieństwa (Liniowy)')

    nonzero_probs = probs_series[probs_series>0]
    sns.histplot(nonzero_probs, bins=50, kde=True, ax=ax2)
    ax2.set_xscale('log')
    ax2.set_title('Rozkład prawdopodobieństwa (Logarystmiczny)')

    plt.tight_layout()
    plt.savefig(f'{output_prefix}_distribution.png', dpi=300)
    plt.close()

def generate_histogram(input_file: str, output_prefix: str, save_fig: bool, show_fig: bool):
    print('\nGenerating probability histogram...')

    try:
        df = pd.read_csv(input_file, sep='\t', usecols=['Probability'])

        sns.set_theme(style='whitegrid')
        plt.figure(figsize=(10,6))

        sns.histplot(data=df, x='Probability', bins=50, kde=True, color='dodgerblue')

        plt.title('Rozkład prawdopodobieństwa mutacji', fontsize=16, pad=15)
        plt.xlabel('Prawdopodobieństwo', fontsize=12)
        plt.ylabel('Częstotliwość występowania', fontsize=12)

        if save_fig:
            plot_file = f'{output_prefix}_histogram.png'
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            print(f'Graph saved as {plot_file}')
        
        if show_fig:
            plt.show()
        
        
        plt.close()

        print(f'Histogram generated succesfully!')
    except Exception as e:
        print(f'Error occured during graph generation: {e}')

def main():
    # CLI argument parser setup
    parser = argparse.ArgumentParser(
        description='Walidacja mutacji z wizualizacją',
        epilog='Example: python validate_ver_1.0.py -f path/to/file.tsv'
    )

    parser.add_argument(
        '-f', '--file',
        type=str,
        required=True,
        help='Path to file with data from AliceDB'
    )
    parser.add_argument(
        '-o', '--output',
        default='results',
        help='Path and name of the output file'
    )
    parser.add_argument(
        '--save_fig', 
        action='store_true',
        help="save graph"
    )
    parser.add_argument(
        '--show_fig', 
        action='store_true',
        help="show graph"
    )

    args = parser.parse_args()
    
    print('Wczytywanie macierzy i generowanie heatmapy...')
    sub_matrix = pd.read_csv(SUB_MATRIX, index_col=0)
    heatmap(sub_matrix, args.output)

    def get_probability(row):
        wild = row.iloc[5]
        mutated = row.iloc[6]
        return sub_matrix.loc[wild, mutated]
    
    prefix = args.output
    file_possible = f'{prefix}_possible.tsv'
    file_all = f'{prefix}_all_prob.tsv'
    
    first_chunk = True
    
    print(f"Processing file\t| chunk size:{CHUNK_SIZE}")
    chunk_iterator = pd.read_csv(args.file, sep='\t', chunksize=CHUNK_SIZE)

    for chunk in tqdm(chunk_iterator, desc="Chunk processing"):
        chunk.insert(0, 'Probability', chunk.apply(get_probability, axis=1))

        possible_chunk = chunk[chunk['Probability'] > 0]

        mode = 'w' if first_chunk else 'a'
        header = first_chunk 

        chunk.to_csv(file_all, sep='\t', index=False, mode=mode, header=header)
        possible_chunk.to_csv(file_possible, sep='\t', index=False, mode=mode, header=header)
        
        first_chunk = False
    
    generate_histogram(file_all, prefix, args.save_fig, args.show_fig)
    print("Done!")



if __name__=='__main__':
    main()

    