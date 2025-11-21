import pandas as pd
import os
from functools import lru_cache

# ------------------------------------------------------------------------
# Arquivo: dp_recommender.py
# Responsabilidade:
# 1. Criar dataset (22 candidatos, 15 cursos)
# 2. Implementar Programação Dinâmica (Knapsack 0/1)
# 3. Implementar FUNÇÃO DENTRO DE FUNÇÃO (requisito obrigatório)
# 4. Criar CSVs automaticamente (data/)
# ------------------------------------------------------------------------

def create_sample_data():
    """
    Gera automaticamente dois DataFrames:
    - df_candidates (22 candidatos com mais de 20 atributos)
    - df_courses (lista de cursos)
    Também salva esses DataFrames como arquivos CSV na pasta data/.
    """

    # --------- 22 CANDIDATOS COM 20+ ATRIBUTOS ---------
    candidates = [
        {
            "id": i,
            "nome": f"Candidato_{i}",
            "idade": 18 + (i % 10),
            "sexo": "M" if i % 2 == 0 else "F",
            "nivel_escolar": ["Ensino Médio", "Graduação", "Técnico", "Pós"][i % 4],
            "hours_available": (i % 10) * 5 + 10,
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
            "saude_mental_score": max(0, 10 - (i % 5)),
            "motivacao_score": (i % 10) + 1,
            "competencia_tecnica": (i % 7) + 1,
            "competencia_humana": (i % 6) + 2,
            "preferencia_carga_horaria": ["Curto", "Médio", "Longo"][i % 3],
            "disponibilidade_fins_de_semana": True if i % 2 == 0 else False,
            "observacoes": "Nenhuma" if i % 3 else "Precisa suporte financeiro"
        }
        for i in range(1, 23)
    ]

    df_candidates = pd.DataFrame(candidates)

    # ----------------- LISTA DE CURSOS -----------------
    courses = [
        {"course_id": 1, "title": "Introdução à IA", "hours": 10, "impact_score": 12},
        {"course_id": 2, "title": "Análise de Dados", "hours": 15, "impact_score": 15},
        {"course_id": 3, "title": "Segurança Cibernética", "hours": 20, "impact_score": 18},
        {"course_id": 4, "title": "UX Design", "hours": 12, "impact_score": 10},
        {"course_id": 5, "title": "Cloud Fundamentals", "hours": 8, "impact_score": 9},
        {"course_id": 6, "title": "Python", "hours": 14, "impact_score": 14},
        {"course_id": 7, "title": "Green Tech", "hours": 10, "impact_score": 11},
        {"course_id": 8, "title": "Comunicação", "hours": 6, "impact_score": 8},
        {"course_id": 9, "title": "DevOps", "hours": 16, "impact_score": 13},
        {"course_id": 10, "title": "Negócios de Impacto", "hours": 9, "impact_score": 10},
        {"course_id": 11, "title": "Ética em IA", "hours": 5, "impact_score": 7},
        {"course_id": 12, "title": "Gamificação", "hours": 12, "impact_score": 9},
        {"course_id": 13, "title": "Inglês Técnico", "hours": 20, "impact_score": 16},
        {"course_id": 14, "title": "Empreendedorismo", "hours": 8, "impact_score": 8},
        {"course_id": 15, "title": "Data Viz", "hours": 10, "impact_score": 11},
    ]

    df_courses = pd.DataFrame(courses)

    # Cria pasta data/ caso não exista
    os.makedirs("data", exist_ok=True)

    # Salva arquivos .csv
    df_candidates.to_csv("data/candidates_sample.csv", index=False)
    df_courses.to_csv("data/courses_sample.csv", index=False)

    return df_candidates, df_courses


def recommend_courses_for_candidate(candidate, courses_df):
    """
    Resolve o problema de otimização (Knapsack 0/1)
    usando Programação Dinâmica com memoização.
    """

    # Capacidade = quantas horas o candidato tem disponíveis
    capacity = int(candidate["hours_available"])

    items = list(courses_df.to_dict("records"))
    n = len(items)

    # --------------------------------------
    # FUNÇÃO DENTRO DE FUNÇÃO (requisito)
    # --------------------------------------
    def build_score_modifier(is_vulnerable):
        """
        Função EXTERNA que retorna outra função INTERNA.
        Isso demonstra o conceito de closure.
        """
        factor = 1.3 if is_vulnerable else 1.0

        def modifier(score):
            return score * factor  # a função acessa o valor de factor
        return modifier

    score_modifier = build_score_modifier(candidate.get("vulneravel", False))

    # Separa pesos e valores do knapsack
    weights = [item["hours"] for item in items]
    values = [score_modifier(item["impact_score"]) for item in items]

    # -------------------------------
    # PROGRAMAÇÃO DINÂMICA + CACHE
    # -------------------------------

    @lru_cache(None)
    def dp(i, remaining):
        """
        Programação Dinâmica com memoização.
        i -> índice do curso analisado
        remaining -> horas restantes disponíveis
        """
        if i == n or remaining <= 0:
            return (0, ())

        # Caso 1: pular o item
        best_val, best_items = dp(i+1, remaining)

        # Caso 2: incluir o item (se couber)
        if weights[i] <= remaining:
            take_val, take_items = dp(i+1, remaining - weights[i])
            take_val += values[i]

            if take_val > best_val:
                return (take_val, take_items + (i,))

        return (best_val, best_items)

    # Chama o DP
    best_val, chosen_idx = dp(0, capacity)

    chosen_courses = [items[i]["course_id"] for i in chosen_idx]
    chosen_titles = [items[i]["title"] for i in chosen_idx]

    return {
        "candidate_id": candidate["id"],
        "candidate_name": candidate["nome"],
        "chosen_course_ids": chosen_courses,
        "chosen_course_titles": chosen_titles,
        "impact": best_val
    }
