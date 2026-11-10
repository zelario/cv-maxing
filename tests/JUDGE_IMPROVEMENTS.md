# Potenciais melhorias do Judge

Este documento regista melhorias propostas para o avaliador automático definido em
[`judge.py`](./judge.py), sem implicar que já estejam implementadas.

## Prioridade alta

### 1. Tornar as escalas de pontuação reproduzíveis

**Situação atual:** o prompt define algumas faixas de pontuação, mas não descreve
critérios concretos para todas as notas. Dois testes semelhantes podem receber
avaliações diferentes.

**Melhoria proposta:** definir âncoras claras para as pontuações de cada dimensão,
incluindo exemplos do que distingue, por exemplo, 10, 8, 6, 4 e 0. Especificar
também como tratar informação que não se aplica ao candidato ou que não pode ser
avaliada a partir dos dados disponíveis.

**Critério de validação:** aplicar o Judge repetidamente a resultados idênticos e
comparar as notas; a variação deve ser pequena e explicável pelos critérios.

### 2. Separar precisão factual de fundamentação em evidência

**Situação atual:** `Accuracy` e `Evidence` podem penalizar a mesma afirmação,
como uma competência verdadeira que aparece sem contexto no CV.

**Melhoria proposta:**

- `Accuracy`: verificar se cada afirmação é compatível com as fontes de verdade.
- `Evidence`: avaliar se o CV mostra contexto ou exemplos que sustentem a afirmação.
- Indicar explicitamente que uma afirmação pode ser verdadeira, mas pouco
  fundamentada, sem ser classificada como alucinação.

**Critério de validação:** uma competência confirmada pelo candidato, mas listada
sem exemplo, deve manter boa precisão factual e receber uma nota de evidência mais
baixa.

### 3. Aplicar as regras críticas também no código

**Situação atual:** o limite de `accuracy_score` quando há alucinações é instruído
no prompt, mas não é imposto depois da resposta do modelo.

**Melhoria proposta:** após validar a resposta como `ValidationResult`, aplicar
deterministicamente a regra: se `hallucinations` não estiver vazia,
`accuracy_score` não pode exceder 6. Registar que a pontuação foi ajustada e
preservar a justificação do Judge.

**Critério de validação:** um teste unitário com alucinações e precisão acima de 6
deve produzir uma pontuação final de, no máximo, 6; sem alucinações, a pontuação
deve permanecer inalterada.

### 4. Definir uma política explícita para fontes de verdade

**Situação atual:** o prompt considera o CV original e a informação confirmada
pelo candidato; menciona tanto a conversa simulada como `user_provided_evidence`,
mas a regra de deteção de alucinações não descreve com precisão como usar e
resolver conflitos entre essas fontes.

**Melhoria proposta:** definir uma ordem de precedência e regras para:

1. factos presentes em `temp_cv.json`;
2. informação afirmada ou confirmada em `simulated_conversation.json`;
3. evidência registada em `temp_optimization.json`;
4. conflitos entre fontes ou respostas vagas.

O Judge deve citar a fonte que sustenta cada conclusão e não tratar uma sugestão
do otimizador como facto confirmado pelo candidato.

**Critério de validação:** incluir casos de teste com informação confirmada,
negada, contraditória e ambígua; só informação explicitamente sustentada deve ser
aceite como facto.

## Prioridade média

### 5. Avaliar o PDF além dos dados estruturados

**Situação atual:** `Judge.evaluate` carrega JSONs da pipeline, mas não inclui
`optimized_cv.pdf` no contexto. Portanto, não consegue avaliar diretamente a
legibilidade ou o resultado visual do documento.

**Melhoria proposta:** acrescentar uma validação visual separada, por exemplo,
verificando automaticamente número de páginas, texto extraído, presença do
consentimento GDPR e conteúdo cortado. Se for usada avaliação por modelo
multimodal, fornecer páginas renderizadas como imagens e manter essa avaliação
separada da precisão factual.

**Critério de validação:** testar PDFs com consentimento em falta, conteúdo
cortado, várias páginas inesperadas e renderização correta; os resultados devem
identificar cada caso.

### 6. Reduzir o enviesamento causado pelos resultados intermédios

**Situação atual:** o Judge recebe `temp_review.json` e `temp_optimization.json`,
além do CV final. As conclusões dessas etapas podem influenciar a avaliação do
resultado final.

**Melhoria proposta:** avaliar primeiro o CV final usando apenas as fontes de
verdade e a descrição da vaga. Se for útil avaliar o comportamento interno da
pipeline, executar uma segunda avaliação que inclua revisão e otimização,
reportando-a separadamente.

**Critério de validação:** comparar avaliações com e sem os resultados
intermédios; diferenças relevantes devem ser justificáveis e não depender apenas
da autoavaliação da pipeline.

### 7. Fazer o resultado indicar evidência para as conclusões

**Situação atual:** o esquema guarda listas de alucinações, pontos fortes,
problemas e recomendações, mas não exige referências específicas às fontes ou
secções do CV.

**Melhoria proposta:** estruturar cada conclusão com a afirmação avaliada, a
fonte correspondente, o motivo da classificação e, quando aplicável, a
recomendação. Isto facilita a revisão humana e a depuração.

**Critério de validação:** cada alucinação e problema deve apontar para uma
afirmação do CV gerado e explicar que evidência foi procurada e não encontrada.

## Prioridade baixa

### 8. Distinguir erro de execução de resultado de avaliação

**Situação atual:** a falta de ficheiros obrigatórios faz `evaluate` imprimir um
erro e devolver `None`, enquanto erros da API terminam o processo.

**Melhoria proposta:** definir um contrato consistente para erros — por exemplo,
lançar exceções específicas para ficheiros em falta, resposta vazia ou falha do
fornecedor — e deixar o chamador decidir se interrompe o teste ou regista uma
falha. Não produzir um resultado de avaliação com formato de sucesso quando a
avaliação não ocorreu.

**Critério de validação:** testes para cada erro devem confirmar que o chamador
recebe um erro explícito e que não é criado um `temp_judge.json` enganador.

## Ordem sugerida

1. Esclarecer as fontes de verdade e as escalas.
2. Separar `Accuracy` de `Evidence`.
3. Impor no código as regras determinísticas, incluindo o limite por alucinação.
4. Acrescentar testes unitários para as regras e casos-limite.
5. Avaliar o PDF visualmente e, se necessário, separar a avaliação do processo da
   avaliação do resultado final.
