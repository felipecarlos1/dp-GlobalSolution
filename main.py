# main.py
"""
Global Solution - Dynamic Programming (Disciplina)
Solução: Recomendador de cursos (knapsack) para maximizar 'impact_score' dado um limite de horas.
Inclui: merge sort para DataFrame, DP (memoization), nested functions, geração de relatórios.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from typing import List, Dict, Tuple

# ----------------------------
# 1) Criar datasets de exemplo
# ----------------------------
def create_sample_data():
    # 20+ candidatos com informações variadas (exigem pelo menos 20 "diferentes informações" por pessoa
    # para satisfazer o requisito do enunciado interpretamos "informações" como colunas de perfil).
    candidates = [
        {
            "id": i,
            "nome": f"Candidato_{i}",
            "idade": 18 + (i % 10),
            "sexo": "M" if i % 2 == 0 else "F",
            "nivel_escolar": ["Ensino Médio", "Graduação", "Técnico", "Pós"][i % 4],
            "hours_available": (i % 10) * 5 + 10,  # variação 10..55 horas
            "localidade": ["Zona A", "Zona B", "Zona C", "Zona D"][i % 4],
            "vulneravel": True if i % 7 == 0 else False,
            "prioridade_area": ["AI", "Cloud", "UX", "GreenTech", "Data"][i % 5],
            "ingles_nivel": ["Básico", "Intermediário", "Avançado"][i % 3],
            "experiencia_meses": (i * 3) % 60,
            "emprego_atual": ["Desempregado", "Freelancer", "Meio período", "Tempo cheio"][i % 4],
            "salario_atual": 0 if i % 4 == 0 else 1200 + i * 20,
            "acesso_internet": True if i % 5 != 0 else False,
            "dispositivo": ["Celular", "Notebook", "Tablet"][i % 3],
            "necessita_transporte": True if i % 6 == 0 else False,
            "saude_mental_score": max(0, 10 - (i % 5)), # 0..10
            "motivacao_score": (i % 10) + 1,
            "competencia_tecnica": (i % 7) + 1, # 1..7
            "competencia_humana": (i % 6) + 2, # 2..7
            "preferencia_carga_horaria": ["Curto", "Médio", "Longo"][i % 3],
            "disponibilidade_fins_de_semana": True if i % 2 == 0 else False,
            # se quiser acrescente mais campos para chegar a >20 por pessoa
            "observacoes": "Nenhuma" if i % 3 else "Precisa suporte financeiro"
        }
        for i in range(1, 23)  # 22 registros -> atende requisito de >=20
    ]
    df_candidates = pd.DataFrame(candidates)

    # Cursos de exemplo
    courses = [
        {"course_id": 1, "title": "Introdução à IA", "hours": 10, "impact_score": 12, "cost": 0, "category": "AI"},
        {"course_id": 2, "title": "Análise de Dados", "hours": 15, "impact_score": 15, "cost": 0, "category": "Data"},
        {"course_id": 3, "title": "Segurança Cibernética", "hours": 20, "impact_score": 18, "cost": 50, "category": "Security"},
        {"course_id": 4, "title": "UX Design", "hours": 12, "impact_score": 10, "cost": 0, "category": "UX"},
        {"course_id": 5, "title": "Cloud Fundamentals", "hours": 8, "impact_score": 9, "cost": 0, "category": "Cloud"},
        {"course_id": 6, "title": "Programação Python", "hours": 14, "impact_score": 14, "cost": 0, "category": "AI"},
        {"course_id": 7, "title": "Sustentabilidade e Economia Verde", "hours": 10, "impact_score": 11, "cost": 0, "category": "GreenTech"},
        {"course_id": 8, "title": "Comunicação e Liderança", "hours": 6, "impact_score": 8, "cost": 0, "category": "Soft"},
        {"course_id": 9, "title": "DevOps Básico", "hours": 16, "impact_score": 13, "cost": 0, "category": "Cloud"},
        {"course_id": 10, "title": "Modelagem de Negócios de Impacto", "hours": 9, "impact_score": 10, "cost": 0, "category": "Management"},
        # adicione mais cursos para diversidade
        {"course_id": 11, "title": "Ética em IA", "hours": 5, "impact_score": 7, "cost": 0, "category": "AI"},
        {"course_id": 12, "title": "Design de Jogos (Gamificação)", "hours": 12, "impact_score": 9, "cost": 0, "category": "UX"},
        {"course_id": 13, "title": "Inglês Técnico", "hours": 20, "impact_score": 16, "cost": 0, "category": "Language"},
        {"course_id": 14, "title": "Microempreendedorismo", "hours": 8, "impact_score": 8, "cost": 0, "category": "Business"},
        {"course_id": 15, "title": "Data Visualization", "hours": 10, "impact_score": 11, "cost": 0, "category": "Data"},
    ]
    df_courses = pd.DataFrame(courses)

    # criar pastas e salvar
    os.makedirs("data", exist_ok=True)
    df_candidates.to_csv("data/candidates_sample.csv", index=False)
    df_courses.to_csv("data/courses_sample.csv", index=False)
    return df_candidates, df_courses

# ----------------------------
# 2) Merge Sort para DataFrame
# ----------------------------
def merge_sort_df(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """
    Implementação de merge sort para DataFrame com base na coluna `key`.
    Retorna um novo DataFrame ordenado.
    """
    # Converter para lista de dicts para facilitar a ordenação recursiva
    records = df.to_dict("records")

    def merge_sort(records_list: List[Dict]) -> List[Dict]:
        if len(records_list) <= 1:
            return records_list
        mid = len(records_list) // 2
        left = merge_sort(records_list[:mid])
        right = merge_sort(records_list[mid:])
        # merge step
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i][key] <= right[j][key]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_records = merge_sort(records)
    return pd.DataFrame(sorted_records)

# ----------------------------
# 3) DP Recommender (Knapsack 0/1)
# ----------------------------
def recommend_courses_for_candidate(candidate: Dict, courses_df: pd.DataFrame) -> Dict:
    """
    Resolve o problema knapsack 0/1 por candidato:
    - capacity = candidate['hours_available']
    - weights = course 'hours'
    - values = course 'impact_score' * bonus_vulneravel
    Retorna um dicionário com a lista de course_ids recomendados e métricas.
    """

    capacity = int(candidate["hours_available"])
    # criar listas
    items = list(courses_df.to_dict("records"))
    n = len(items)

    # nested function: score modifier e memo DP
    def build_score_modifier(is_vulnerable: bool):
        """
        Função que retorna uma função de modificação de score.
        Exemplo de função dentro de função (closure).
        """
        factor = 1.3 if is_vulnerable else 1.0
        def modifier(base_score: float) -> float:
            return base_score * factor
        return modifier

    score_modifier = build_score_modifier(candidate.get("vulneravel", False))

    # transformar horas para inteiros e preparar arrays
    weights = [int(it["hours"]) for it in items]
    values = [int(round(score_modifier(it["impact_score"]))) for it in items]

    # memoização: dp(index, remaining_capacity) -> (best_value, chosen_indices)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(i: int, rem: int) -> Tuple[int, Tuple[int, ...]]:
        """
        i: índice atual (0..n)
        rem: capacidade restante
        Retorna tupla (melhor_valor, tuple_de_itens_selecionados)
        """
        if i == n or rem <= 0:
            return (0, ())
        # opção 1: pular
        val_skip, items_skip = dp(i + 1, rem)
        best_val, best_items = val_skip, items_skip

        # opção 2: pegar se couber
        if weights[i] <= rem:
            val_take, items_take = dp(i + 1, rem - weights[i])
            val_take += values[i]
            if val_take > best_val:
                best_val = val_take
                best_items = items_take + (i,)

        return (best_val, best_items)

    best_value, chosen_indices = dp(0, capacity)
    chosen_courses = [items[i]["course_id"] for i in chosen_indices]
    chosen_titles = [items[i]["title"] for i in chosen_indices]
    total_hours = sum(items[i]["hours"] for i in chosen_indices)
    raw_impact = sum(items[i]["impact_score"] for i in chosen_indices)
    adjusted_impact = sum(values[i] for i in chosen_indices)
    return {
        "candidate_id": candidate["id"],
        "candidate_name": candidate["nome"],
        "chosen_course_ids": chosen_courses,
        "chosen_course_titles": chosen_titles,
        "total_hours_used": total_hours,
        "raw_impact": raw_impact,
        "adjusted_impact": adjusted_impact,
        "best_value_dp": best_value
    }

# ----------------------------
# 4) Reporting
# ----------------------------
def generate_reports(recommendations: List[Dict], out_folder: str = "outputs"):
    os.makedirs(out_folder, exist_ok=True)
    df_rec = pd.DataFrame(recommendations)
    csv_path = os.path.join(out_folder, "recommendations.csv")
    df_rec.to_csv(csv_path, index=False)

    # resumo agregado
    df_rec["num_courses"] = df_rec["chosen_course_ids"].apply(lambda x: len(x) if isinstance(x, list) else 0)
    summary = df_rec[["candidate_id", "candidate_name", "total_hours_used", "adjusted_impact", "num_courses"]]
    summary.to_csv(os.path.join(out_folder, "summary.csv"), index=False)

    # gráficos simples
    plt.figure()
    plt.hist(df_rec["adjusted_impact"], bins=8)
    plt.title("Distribuição de Impacto Ajustado")
    plt.xlabel("impacto ajustado")
    plt.ylabel("frequência")
    plt.savefig(os.path.join(out_folder, "impact_hist.png"))
    plt.close()

    plt.figure()
    plt.scatter(df_rec["total_hours_used"], df_rec["adjusted_impact"])
    plt.title("Horas usadas vs Impacto")
    plt.xlabel("Horas usadas")
    plt.ylabel("Impacto ajustado")
    plt.savefig(os.path.join(out_folder, "hours_vs_impact.png"))
    plt.close()

    return csv_path, os.path.join(out_folder, "summary.csv")

# ----------------------------
# 5) Fluxo principal
# ----------------------------
def main():
    # 1) criar dados
    df_candidates, df_courses = create_sample_data()

    # 2) ordenar candidatos por "motivacao_score" (desc) usando merge_sort_df
    df_candidates_sorted = merge_sort_df(df_candidates, key="motivacao_score")
    # como merge_sort retorna ascendente, invertemos para ordem desc
    df_candidates_sorted = df_candidates_sorted.iloc[::-1].reset_index(drop=True)

    # 3) gerar recomendações por candidato
    recommendations = []
    for idx, row in df_candidates_sorted.iterrows():
        cand = row.to_dict()
        rec = recommend_courses_for_candidate(cand, df_courses)
        recommendations.append(rec)

    # 4) gerar relatórios
    csv_path, summary_path = generate_reports(recommendations)
    print("Relatórios gerados:", csv_path, summary_path)

    # salvar recomendações em Excel (opcional)
    pd.DataFrame(recommendations).to_excel("outputs/recommendations.xlsx", index=False)

if __name__ == "__main__":
    main()