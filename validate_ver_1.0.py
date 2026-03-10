import pandas as pd

EXAMPLE_PROTEIN_SEQUENCE = "IALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
TRUE_TEST_SEQUENCE = "IALWMRLLLLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"

prob_matrix = pd.read_csv('macierz_prawdopodobienstw_1_literowa.csv', index_col=0)

def probability_of_existing(prot_seq: str, prob_matrix: pd.DataFrame) -> float:
    probability = 1.0

    for id in range(len(prot_seq)):
        if prot_seq[id] == TRUE_TEST_SEQUENCE[id]:
            continue
        else:
            single_substitution_probability = prob_matrix.loc[prot_seq[id], TRUE_TEST_SEQUENCE[id]]
            probability -= 1 - probability * single_substitution_probability
            print(f'Difference at pos: {id} | canon: {TRUE_TEST_SEQUENCE[id]}, tested: {prot_seq[id]}')
            print(f'Probability of this change with SNP: {single_substitution_probability}')

    print(f'Probability of existing: {probability}')
probability_of_existing(EXAMPLE_PROTEIN_SEQUENCE, prob_matrix)
