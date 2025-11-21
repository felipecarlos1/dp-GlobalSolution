import pandas as pd
import os
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Arquivo: reporting.py
# Responsabilidade:
# - Criar relatórios da solução
# - Gerar gráficos
# - Salvar CSVs na pasta outputs/
# ---------------------------------------------------------

def generate_reports(recommendations, out_folder="outputs"):
    """
    Gera arquivos de saída:
        - recommendations.csv
        - summary.csv
        - gráficos PNG
    """
    os.makedirs(out_folder, exist_ok=True)

    df = pd.DataFrame(recommendations)

    # Salva todos os resultados completos
    df.to_csv(f"{out_folder}/recommendations.csv", index=False)

    # Adiciona coluna com número de cursos por candidato
    df["num_courses"] = df["chosen_course_ids"].apply(len)

    # Relatório resumido
    df[["candidate_id", "candidate_name", "impact", "num_courses"]] \
        .to_csv(f"{out_folder}/summary.csv", index=False)

    # ------------------ GRÁFICOS ------------------

    # Histograma de impacto
    plt.hist(df["impact"])
    plt.title("Distribuição de Impacto")
    plt.savefig(f"{out_folder}/impact_hist.png")
    plt.close()

    # Correlação cursos X impacto
    plt.scatter(df["num_courses"], df["impact"])
    plt.title("Cursos x Impacto")
    plt.savefig(f"{out_folder}/courses_vs_impact.png")
    plt.close()
