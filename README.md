# 📘 Global Solution – Dynamic Programming (FIAP 2025)

### **Tema: O Futuro do Trabalho – Requalificação Inteligente com Programação Dinâmica**

Este projeto apresenta uma solução completa que utiliza **Programação Dinâmica (DP)**, **Merge Sort**, **função dentro de função**, **DataFrames**, **relatórios** e **arquitetura modular** para recomendar cursos ideais para candidatos que desejam se requalificar no mercado de trabalho — alinhado ao tema do Futuro do Trabalho.

---

## 🧩 1. Objetivo da Solução

O avanço da automação e da IA exige que profissionais se requalifiquem constantemente.  
Diante disso, esta solução responde:

> **Como recomendar automaticamente os melhores cursos para cada candidato, maximizando seu impacto de empregabilidade dentro do limite de horas disponíveis?**

O problema é tratado como um **Knapsack 0/1**, resolvido com Programação Dinâmica.

---

## 📌 2. Formulação do Problema

### ✔ **Entrada**
- 22 candidatos com **20+ atributos** (motivação, escolaridade, internet, vulnerabilidade etc.)
- 15 cursos, cada um com:
  - horas necessárias  
  - impacto na empregabilidade  

### ✔ **Processamento**
1. Ordenação dos candidatos por motivação usando **Merge Sort**.  
2. Para cada candidato:
   - Aplicação do algoritmo **Knapsack** via DP.
   - Ajuste de impacto por meio de uma **função dentro de função (closure)** para vulneráveis.  
3. Geração de relatórios e gráficos.  

### ✔ **Saída**
- `recommendations.csv`  
- `summary.csv`  
- Gráficos `.png`  
- Datasets `.csv` gerados automaticamente  

---

## 🔍 3. Explicação da Solução

A solução está dividida em quatro módulos na pasta `src/`.

---

### **3.1. Merge Sort – Ordenação (`sorting.py`)**

Implementação manual do algoritmo **Merge Sort** para ordenar candidatos por motivação.  
Não usa `.sort_values()`.  
Complexidade: **O(n log n)**.

---

### **3.2. Programação Dinâmica + Função Dentro de Função (`dp_recommender.py`)**

Este módulo contém:

- Criação automática de datasets com 22 candidatos e 15 cursos  
- Implementação do **Knapsack 0/1 com memoização**  
- Uso obrigatório de **função dentro de função (closure)**:
  
```python
def build_score_modifier(is_vulnerable):
    def modifier(score):
        return score * factor
    return modifier