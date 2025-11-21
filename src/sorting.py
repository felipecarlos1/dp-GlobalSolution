import pandas as pd

# ---------------------------------------------------------
# Arquivo: sorting.py
# Responsabilidade: Implementar o algoritmo Merge Sort
# aplicado a um DataFrame. Esse arquivo atende ao requisito:
# "Estrutura para ordenação dos dados (quick ou merge sort)".
# ---------------------------------------------------------

def merge_sort_df(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """
    Ordena um DataFrame usando Merge Sort, sem usar sort_values().
    Parâmetros:
        df  -> DataFrame de entrada
        key -> coluna usada como critério de ordenação
    Retorno:
        DataFrame ordenado
    """

    # Converte o DataFrame para lista de dicionários
    # pois a ordenação recursiva funciona melhor com listas.
    records = df.to_dict("records")

    def merge_sort(lst):
        """
        Função recursiva do Merge Sort.
        - Divide a lista em duas partes
        - Ordena cada parte
        - Combina ordenadamente
        """
        if len(lst) <= 1:
            return lst
        
        mid = len(lst) // 2
        left = merge_sort(lst[:mid])
        right = merge_sort(lst[mid:])

        merged = []
        i = j = 0

        # Etapa de merge: combina listas ordenadas
        while i < len(left) and j < len(right):
            if left[i][key] <= right[j][key]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        # Adiciona elementos restantes
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_records = merge_sort(records)

    # Reconstrói o DataFrame ordenado
    return pd.DataFrame(sorted_records)
