# Potenciais melhorias do simulador de candidato

Este documento regista propostas para melhorar o simulador definido em
[`candidate.py`](./src/candidate.py). O simulador serve para automatizar testes
da pipeline; as respostas geradas não representam respostas de utilizadores
reais.

## Prioridade alta

### 1. Usar respostas fixas para testes reproduzíveis

**Situação atual:** as respostas são geradas por um LLM e podem variar entre
execuções, mesmo com as mesmas entradas. Isso torna mais difícil comparar
alterações na pipeline.

**Melhoria proposta:** permitir cenários com respostas predefinidas para
perguntas esperadas. Manter o modo LLM para testes exploratórios, mas usar o modo
de respostas fixas em regressões e comparações entre versões.

**Critério de validação:** executar o mesmo cenário várias vezes com respostas
fixas deve fornecer exatamente as mesmas respostas à pipeline.

### 2. Restringir as respostas a factos disponíveis

**Situação atual:** o prompt instrui o modelo a não inventar, mas o modelo ainda
pode interpretar incorretamente o CV ou acrescentar informação sem suporte.

**Melhoria proposta:** representar os factos do candidato de forma estruturada
quando possível e indicar que cada resposta só pode usar esses factos. Se a
pergunta pedir informação que não consta das fontes, o simulador deve responder
que essa informação não foi fornecida, sem a inventar.

**Critério de validação:** incluir perguntas sobre factos presentes, ausentes e
explicitamente negados. As respostas não devem introduzir competências, datas,
empregadores, métricas ou qualificações que não estejam nas fontes.

### 3. Distinguir informação ausente de resposta negativa

**Situação atual:** o prompt sugere respostas como “I do not have one” quando a
informação não aparece no CV ou no perfil. A ausência de informação não prova
que o candidato não tenha essa competência, ligação ou certificação.

**Melhoria proposta:** usar respostas diferentes para:

- informação explicitamente negada pelo perfil;
- informação que o perfil confirma;
- informação desconhecida ou não fornecida.

Por exemplo, responder “não tenho experiência com X” apenas se isso estiver
explicitamente indicado; caso contrário, dizer que o perfil não fornece essa
informação.

**Critério de validação:** um dado ausente deve resultar numa resposta de
incerteza, enquanto uma negação explícita deve resultar numa resposta negativa.

## Prioridade média

### 4. Incluir o histórico da conversa

**Situação atual:** `answer_question` constrói cada prompt com o CV, o perfil, a
vaga e a pergunta atual, mas não inclui as respostas anteriores guardadas em
`self.conversation`. Assim, respostas a perguntas posteriores podem contradizer
respostas anteriores.

**Melhoria proposta:** passar o histórico da conversa ao prompt e instruir o
simulador a manter consistência. Se uma pergunta posterior revelar uma
contradição no próprio cenário, o simulador deve indicar a incerteza em vez de
inventar uma resolução.

**Critério de validação:** fazer perguntas repetidas ou relacionadas e confirmar
que o simulador não altera os factos fornecidos.

### 5. Separar o simulador LLM da fonte de verdade

**Situação atual:** o mesmo modelo interpreta as fontes e redige a resposta.
Uma resposta convincente pode, por isso, parecer factual mesmo quando acrescenta
detalhes.

**Melhoria proposta:** manter o CV e o perfil como fontes de verdade e tratar a
resposta do LLM apenas como uma formulação dessas fontes. Guardar a pergunta, a
resposta e, se possível, os factos de origem usados para produzi-la, para
facilitar auditoria.

**Critério de validação:** cada afirmação factual da resposta deve poder ser
associada a uma passagem do CV ou do perfil; afirmações sem origem devem ser
assinaladas.

### 6. Tratar falhas da API sem terminar abruptamente o processo

**Situação atual:** após esgotar as tentativas, o simulador chama `sys.exit(1)`,
o que termina o processo que executa o caso de teste e pode dificultar a
preservação de resultados parciais.

**Melhoria proposta:** lançar uma exceção específica de falha do simulador. A
pipeline de validação pode capturá-la, marcar o caso como falhado e guardar os
diagnósticos e resultados parciais, sem criar um resultado de avaliação
aparentemente bem-sucedido.

**Critério de validação:** simular uma falha permanente do fornecedor e
confirmar que o caso é registado como falhado, sem terminar silenciosamente a
execução da matriz nem gerar uma resposta fictícia.

## Prioridade baixa

### 7. Registar o modo e o modelo usados

**Situação atual:** os resultados arquivados guardam a conversa, mas não
identificam necessariamente de forma clara se as respostas vieram de um LLM ou
de um cenário fixo, nem toda a configuração relevante.

**Melhoria proposta:** guardar metadados do caso de teste, incluindo o modo do
simulador, o identificador do modelo e a versão do cenário. Nunca guardar a API
key ou outros segredos.

**Critério de validação:** cada resultado arquivado deve permitir identificar
como a conversa foi produzida e repetir o cenário quando se usaram respostas
fixas.

## Ordem sugerida

1. Distinguir factos confirmados, negados e desconhecidos.
2. Introduzir respostas fixas para regressões reproduzíveis.
3. Garantir consistência através do histórico da conversa.
4. Auditar as afirmações das respostas contra as fontes do cenário.
5. Tratar falhas da API como falhas explícitas do caso de teste.
