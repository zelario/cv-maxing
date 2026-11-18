# Estrutura do Formulário — Turing Test Study (CV Maxing)

> **Link do Formulário no Google Forms**: [Human vs. AI CV Tailoring](https://docs.google.com/forms/d/1hAJTlzHHDgxj6dVai3JkjWl5ksn8PsbTAnVOHcnmnrc/viewform)  
> **Link de Edição / Respostas**: [Google Forms Edit](https://docs.google.com/forms/d/1hAJTlzHHDgxj6dVai3JkjWl5ksn8PsbTAnVOHcnmnrc/edit#responses)

---

## 1. Cabeçalho e Instruções Iniciais

- **Título**: `Human vs. AI CV Tailoring`
- **Descrição**:
  > *"This study evaluates the authenticity and quality of resumes tailored to job postings. You will evaluate 3 candidate scenarios across 3 pages (one scenario per page). For each scenario, compare 3 blinded versions (Version A, Version B, Version C) and answer 4 questions. There are no demographic questions."*
- **Duração estimada**: 8 a 10 minutos.

---

## 2. Desenho Experimental e Chave de Descegamento (Latin Square)

Para eliminar o viés de ordem (*order bias*), a ordem das condições está contra-balanceada entre os 3 casos:

| Caso | Perfil do Candidato | Vaga Alvo | Version A | Version B | Version C |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Case 1** | **Tomás Silva** (Junior) | Data Scientist Intern | **CV Maxing** (IA HCAI) | **Baseline LLM** (ChatGPT) | **Human** (Controlo Humano) |
| **Case 2** | **Pedro Oliveira** (Transition) | Fullstack Web Developer | **Human** (Controlo Humano) | **CV Maxing** (IA HCAI) | **Baseline LLM** (ChatGPT) |
| **Case 3** | **Rita Santos** (Senior) | Staff Tech Lead (Dist. Systems) | **Baseline LLM** (ChatGPT) | **Human** (Controlo Humano) | **CV Maxing** (IA HCAI) |

> **Normalização Visual**: Todas as versões foram renderizadas com o mesmo template visual A4 (Jinja2 + Playwright) para garantir que a avaliação incide estritamente sobre a autenticidade, linguagem e substância dos factos.

---

## 3. Estrutura Detalhada por Caso (Página a Página)

### Página 1 / 3: CASE 1 — Tomás Silva (Data Scientist Intern)
- **Contexto**:
  > *"Candidate profile: CS graduate with strong machine learning, statistics, Python, and SQL background."*
- **Artefacto Visual**: Imagem com as 3 versões lado a lado (`Version A`, `Version B`, `Version C`).
- **Perguntas**:
  1. **Q1 — AI Perception Rating (Grelha Likert 1-5)**:
     > *"On a scale of 1 to 5, how AI-generated or human-written does each version appear?"*  
     > *(1 - Definitely Human · 2 - Likely Human · 3 - Uncertain · 4 - Likely AI · 5 - Definitely AI)*  
     > - Linhas: `Version A`, `Version B`, `Version C`
  2. **Q2 — Turing Test Forced Choice (Escolha Múltipla Obrigatória)**:
     > *"Case 1: Overall, which single version do you believe was tailored by a HUMAN?"*  
     > - Opções: `Version A` | `Version B` | `Version C`
  3. **Q3 — Hiring Recommendation (Escolha Múltipla Obrigatória)**:
     > *"Case 1: If you were the hiring manager, which version would you recommend for an interview?"*  
     > - Opções: `Version A` | `Version B` | `Version C`
  4. **Q4 — Justificação Qualitativa (Texto Curto Opcional)**:
     > *"Case 1: Briefly explain what details or phrasing led to your choices (Optional)"*

---

### Página 2 / 3: CASE 2 — Pedro Oliveira (Fullstack Web Developer)
- **Contexto**:
  > *"Candidate profile: Career transitioner with a Civil Engineering background and an intensive 900h Full-Stack Bootcamp (React, Node.js, PostgreSQL)."*
- **Artefacto Visual**: Imagem com as 3 versões lado a lado (`Version A`, `Version B`, `Version C`).
- **Perguntas**:
  1. **Q1 — AI Perception Rating (Grelha Likert 1-5)**:
     > *"On a scale of 1 to 5, how AI-generated or human-written does each version appear?"*
     > - Linhas: `Version A`, `Version B`, `Version C`
  2. **Q2 — Turing Test Forced Choice (Escolha Múltipla Obrigatória)**:
     > *"Case 2: Overall, which single version do you believe was tailored by a HUMAN?"*  
     > - Opções: `Version A` | `Version B` | `Version C`
  3. **Q3 — Hiring Recommendation (Escolha Múltipla Obrigatória)**:
     > *"Case 2: If you were the hiring manager, which version would you recommend for an interview?"*  
     > - Opções: `Version A` | `Version B` | `Version C`
  4. **Q4 — Justificação Qualitativa (Texto Curto Opcional)**:
     > *"Case 2: Briefly explain what details or phrasing led to your choices (Optional)"*

---

### Página 3 / 3: CASE 3 — Rita Santos (Senior / Staff Tech Lead)
- **Contexto**:
  > *"Candidate profile: 8+ years experience, event-driven architectures (Kafka), Go/Python, AWS, and technical mentorship."*
- **Artefacto Visual**: Imagem com as 3 versões lado a lado (`Version A`, `Version B`, `Version C`).
- **Perguntas**:
  1. **Q1 — AI Perception Rating (Grelha Likert 1-5)**:
     > *"On a scale of 1 to 5, how AI-generated or human-written does each version appear?"*
     > - Linhas: `Version A`, `Version B`, `Version C`
  2. **Q2 — Turing Test Forced Choice (Escolha Múltipla Obrigatória)**:
     > *"Case 3: Overall, which single version do you believe was tailored by a HUMAN?"*  
     > - Opções: `Version A` | `Version B` | `Version C`
  3. **Q3 — Hiring Recommendation (Escolha Múltipla Obrigatória)**:
     > *"Case 3: If you were the hiring manager, which version would you recommend for an interview?"*  
     > - Opções: `Version A` | `Version B` | `Version C`
  4. **Q4 — Justificação Qualitativa (Texto Curto Opcional)**:
     > *"Case 3: Briefly explain what details or phrasing led to your choices (Optional)"*
