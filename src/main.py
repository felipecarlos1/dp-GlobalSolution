from sorting import merge_sort_df
from dp_recommender import create_sample_data, recommend_courses_for_candidate
from reporting import generate_reports

# ---------------------------------------------------------
# Arquivo: main.py
# Responsabilidade:
# - Executar o fluxo completo do programa
# - Integrar: ordenação + DP + relatórios
# - É o arquivo que o usuário deve rodar
# ---------------------------------------------------------

def main():
    # Cria datasets automaticamente (e salva em data/)
    df_candidates, df_courses = create_sample_data()

    # Ordena candidatos por motivação (requisito: merge sort)
    df_sorted = merge_sort_df(df_candidates, key="motivacao_score")

    # Reverte para ordem decrescente
    df_sorted = df_sorted.iloc[::-1].reset_index(drop=True)

    # Executa a recomendação por DP para cada candidato
    recommendations = []
    for _, row in df_sorted.iterrows():
        rec = recommend_courses_for_candidate(row.to_dict(), df_courses)
        recommendations.append(rec)

    # Gera CSVs e gráficos
    generate_reports(recommendations)

    print("Relatórios gerados na pasta outputs/")

if __name__ == "__main__":
    main()