import pandas as pd

FILE = 'hs_can_sp_03_26_20260317_124231.tsv'
SUB_MATRIX = 'macierz_prawdopodobienstw_1_literowa.csv'

def data_reader(file_path: str) -> pd.DataFrame:
    file = pd.read_csv(file_path, sep='\t')
    return file

def mutation(data):
    # return: [wild_type, mutated_type]

    return [data.iloc[5], data.iloc[6]]

sub_matrix = pd.read_csv(SUB_MATRIX, index_col=0)

def main():
    data = data_reader(FILE)
    res_data = []

    for index, row in data.iterrows():
        wild, mutated = mutation(row)
        prob = sub_matrix.loc[wild, mutated]
        print(f'{prob}')
        res_data.append([prob, row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6]])
    new_df = pd.DataFrame(res_data)
    new_df.to_csv(f'results.tsv', sep='\t', index=False)
main()

# collumn numbers meaning:
# 0 - peptide
# 1 - target
# 2 - match_begin
# 3 - matxh_end
# 4 - variant_position
# 5 - wild_type
# 6 - mutated_type
