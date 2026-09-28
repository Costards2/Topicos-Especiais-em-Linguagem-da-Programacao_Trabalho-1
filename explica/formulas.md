# Guia Executivo: Entendendo as Métricas de Saúde de Software

> **Objetivo:** traduzir indicadores técnicos de engenharia de software em informações claras para gestores, investidores e membros da diretoria, permitindo avaliar **estabilidade, risco operacional, capacidade de execução e sustentabilidade** de um projeto de tecnologia.

---

## 📊 Visão Geral

As métricas analisadas procuram responder a sete perguntas fundamentais:

| Dimensão | Métrica | Pergunta de negócio |
|---|---|---|
| 👥 Dependência | **Bus Factor** | Quanto o projeto depende de poucas pessoas? |
| ⏱️ Execução | **Cadência de Resolução** | Quanto tempo a equipe leva para avaliar mudanças? |
| 💬 Colaboração | **Nível de Atrito** | Quanto esforço de comunicação cada mudança exige? |
| 🕐 Sustentabilidade | **Perfil de Dedicação** | Em quais períodos a maior parte do desenvolvimento acontece? |
| 🔥 Qualidade | **Hotspots** | Quais partes do software concentram alterações recorrentes? |
| 🤝 Comunidade | **Merge Rate** | Qual proporção das contribuições é incorporada? |
| 🎯 Prioridades | **Bugs vs. Features** | Como a equipe distribui seu esforço entre correções e evolução? |

> **Importante:** nenhuma dessas métricas deve ser interpretada isoladamente. Um valor alto ou baixo não significa automaticamente que um projeto é "bom" ou "ruim". O contexto do projeto, o tamanho da equipe, o modelo de contribuição e o período analisado precisam ser considerados.

---

# 1. 👥 Índice de Concentração de Risco — Bus Factor

## O que significa na prática?

Imagine que as três pessoas que mais conhecem o projeto deixassem a empresa amanhã.

**O conhecimento necessário para manter o software continuaria distribuído entre o restante da equipe?**

O **Bus Factor** mede a concentração de conhecimento e atividade em poucas pessoas.

Quanto maior a concentração, maior tende a ser a dependência operacional de determinados indivíduos.

Essa métrica é especialmente relevante para avaliar:

- risco de continuidade;
- concentração de conhecimento;
- dependência de pessoas-chave;
- capacidade de sucessão técnica;
- risco operacional.

## Como é calculado?

O sistema classifica os desenvolvedores pelo volume de entregas realizadas no projeto.

Em seguida, considera as entregas dos **3 desenvolvedores mais ativos** e compara esse volume com todas as entregas realizadas.

## Fórmula

$$
\text{Bus Factor (\%)} =
\frac{\text{Entregas dos 3 maiores desenvolvedores}}
{\text{Total de entregas do projeto}}
\times 100
$$

### Exemplo

Se os três principais desenvolvedores forem responsáveis por 750 das 1.000 entregas:

$$
\frac{750}{1000} \times 100 = 75\%
$$

Isso significa que **75% das entregas estão concentradas nos três principais contribuidores**.

> ⚠️ **Interpretação:** quanto maior a concentração, maior a dependência estatística dessas pessoas. O limite de 70% pode ser utilizado como referência interna de alerta, mas não deve ser tratado como uma regra universal.

---

# 2. ⏱️ Cadência de Resolução de Tarefas

## O que significa na prática?

Esta métrica mede **quanto tempo uma contribuição leva para percorrer o processo de avaliação até seu encerramento**.

Em projetos colaborativos, uma Pull Request (PR) representa uma proposta de alteração no código.

A métrica procura responder:

> **"Quando alguém propõe uma mudança, quanto tempo o projeto leva para tomar uma decisão?"**

Um tempo elevado pode estar associado a:

- processos de revisão mais complexos;
- falta de disponibilidade dos revisores;
- grande volume de contribuições;
- dependências técnicas;
- outras características do projeto.

## Como é calculado?

Para cada Pull Request, são coletados:

- data/hora de abertura;
- data/hora de encerramento.

Calcula-se então o tempo decorrido entre os dois eventos.

## Fórmula por tarefa

$$
T_i =
\text{Data de fechamento}_i -
\text{Data de abertura}_i
$$

A cadência média é:

$$
\text{Cadência Média} =
\frac{\sum_{i=1}^{N} T_i}{N}
$$

Onde:

- $T_i$ = tempo de resolução da tarefa $i$;
- $N$ = quantidade de tarefas analisadas.

### Unidade

**Dias**, podendo também ser apresentada em horas.

> 💡 **Boa prática:** além da média, considere a **mediana** e percentis, como P90 ou P95. Uma única PR excepcionalmente demorada pode distorcer bastante a média.

---

# 3. 💬 Nível de Atrito — Densidade de Discussão

## O que significa na prática?

Uma alteração simples deveria, em condições normais, exigir uma quantidade proporcional de discussão.

Quando pequenas mudanças geram longas discussões, isso pode indicar:

- regras pouco claras;
- divergências técnicas;
- falta de alinhamento;
- processos de revisão complexos;
- mudanças de arquitetura;
- requisitos pouco definidos.

A métrica funciona como um **indicador de esforço de colaboração**.

## Como é calculado?

O sistema contabiliza os comentários associados às tarefas avaliadas.

Depois, divide o total de comentários pela quantidade de tarefas analisadas.

## Fórmula

$$
\text{Nível de Atrito} =
\frac{\text{Total de comentários}}
{\text{Quantidade de tarefas avaliadas}}
$$

### Exemplo

Se 500 comentários foram registrados em 100 Pull Requests:

$$
\frac{500}{100} = 5
$$

O projeto apresenta uma média de **5 comentários por tarefa**.

> ⚠️ **Atenção:** muitos comentários não significam necessariamente um problema. Projetos complexos ou equipes que praticam revisões rigorosas podem naturalmente apresentar maior volume de discussão.

---

# 4. 🕐 Perfil de Dedicação — Distribuição de Horários

## O que significa na prática?

Esta métrica mostra **em quais horários as atividades de desenvolvimento acontecem**.

O objetivo é identificar o padrão temporal das contribuições e entender o perfil de atividade do projeto.

Uma distribuição pode mostrar predominância de atividade:

- durante o horário comercial;
- à noite;
- nos finais de semana;
- distribuída ao longo de 24 horas.

## Como é calculado?

Para cada contribuição, o sistema registra o horário associado ao evento.

A data completa é transformada em uma variável correspondente à **hora do dia**:

$$
H \in \{0,1,2,\ldots,23\}
$$

Depois, as contribuições são agrupadas por hora.

## Fórmula

$$
F(h) =
\text{Quantidade de contribuições realizadas na hora } h
$$

onde:

$$
h \in [0,23]
$$

O resultado pode ser apresentado em um **histograma de atividade por hora**.

### Exemplo

| Horário | Contribuições |
|---:|---:|
| 08h | 120 |
| 09h | 185 |
| 10h | 210 |
| 11h | 190 |
| 12h | 75 |
| 13h | 90 |
| 14h | 160 |
| 15h | 180 |
| 16h | 175 |
| 17h | 150 |
| 18h | 80 |
| 19h | 60 |
| 20h | 45 |
| 21h | 30 |
| 22h | 35 |

> ⚠️ **Importante:** o horário precisa ser interpretado corretamente. Se os dados estiverem em **UTC**, a distribuição não representa necessariamente o horário local dos desenvolvedores.

---

# 5. 🔥 Mapeamento de Peças Críticas — Hotspots

## O que significa na prática?

Um **hotspot** é uma parte do código que sofre alterações frequentes ao longo da história do projeto.

A ideia é semelhante à identificação de uma peça de um equipamento que constantemente retorna à manutenção.

Arquivos que aparecem repetidamente em alterações podem merecer investigação adicional por razões como:

- alta complexidade;
- grande importância para o sistema;
- evolução constante de requisitos;
- bugs recorrentes;
- arquitetura centralizada;
- acoplamento entre componentes.

## Como é calculado?

O sistema percorre o histórico de alterações do projeto.

Para cada alteração, identifica os arquivos modificados e contabiliza quantas vezes cada arquivo apareceu.

## Fórmula

Para um arquivo $f$:

$$
\text{Hotspot}(f) =
\sum_{i=1}^{N}
I(f \text{ foi alterado no evento } i)
$$

Onde $I$ é uma função indicadora:

$$
I(x)=
\begin{cases}
1, & \text{se } x \text{ for verdadeiro}\\
0, & \text{caso contrário}
\end{cases}
$$

O resultado final pode ser ordenado para identificar os arquivos mais frequentemente modificados.

### Exemplo

| Arquivo | Alterações |
|---|---:|
| `payment.py` | 842 |
| `user_service.py` | 731 |
| `database.py` | 615 |
| `auth.py` | 504 |
| `api.py` | 491 |

> ⚠️ **Importante:** frequência de alteração não significa necessariamente "má qualidade". Um arquivo central pode ser alterado frequentemente justamente porque possui muitas responsabilidades ou porque representa uma área de evolução constante.

---

# 6. 🤝 Taxa de Aceitação — Merge Rate

## O que significa na prática?

Projetos que recebem contribuições externas dependem de um processo eficiente de avaliação e integração dessas mudanças.

A **Taxa de Aceitação** mede a proporção de contribuições avaliadas que foram efetivamente incorporadas ao projeto.

Ela ajuda a entender a relação entre:

**contribuições recebidas → contribuições aceitas**

## Como é calculado?

O sistema identifica todas as contribuições encerradas e classifica seu resultado final.

Em seguida, divide o número de contribuições incorporadas pelo número total de contribuições avaliadas.

## Fórmula

$$
\text{Merge Rate (\%)} =
\frac{\text{Contribuições aceitas}}
{\text{Total de contribuições avaliadas}}
\times 100
$$

### Exemplo

Se 800 Pull Requests foram encerradas e 600 foram incorporadas:

$$
\frac{600}{800}\times100 = 75\%
$$

A taxa de aceitação é de **75%**.

> ⚠️ **Cuidado na interpretação:** uma taxa baixa não significa necessariamente que o projeto seja pouco receptivo. Contribuições podem ser rejeitadas por duplicidade, incompatibilidade técnica, escopo inadequado, baixa qualidade ou porque o projeto não precisa daquela alteração.

---

# 7. 🎯 Foco de Prioridades — Bugs vs. Inovações

## O que significa na prática?

Esta métrica procura identificar **como o tempo de resolução varia entre diferentes tipos de trabalho**.

A análise separa as solicitações em categorias como:

- 🐛 **Bugs:** correções de problemas existentes;
- ✨ **Features:** criação de novas funcionalidades;
- 🔧 **Melhorias:** evolução ou aprimoramento de funcionalidades existentes.

A comparação ajuda a entender como o fluxo de trabalho do projeto está distribuído.

## Como é calculado?

O sistema analisa as informações disponíveis nas solicitações e utiliza critérios de classificação para separar os tipos de trabalho.

Uma abordagem simples pode utilizar palavras-chave.

### 🐛 Bugs

- erro;
- falha;
- crash;
- bug;
- problema;
- correção.

### ✨ Features / Melhorias

- novo;
- adicionar;
- implementação;
- melhoria;
- suporte;
- funcionalidade.

Depois da classificação, calcula-se o tempo médio de resolução de cada categoria.

## Fórmula

Para cada categoria $C$:

$$
\text{Tempo Médio}(C) =
\frac{\sum_{i=1}^{N_C} T_i}
{N_C}
$$

Assim, podemos comparar:

$$
\text{Tempo Médio de Bugs}
\quad \text{vs.} \quad
\text{Tempo Médio de Features}
$$

### Exemplo

| Categoria | Solicitações | Tempo médio |
|---|---:|---:|
| 🐛 Bugs | 150 | 4,2 dias |
| ✨ Features | 100 | 12,5 dias |
| 🔧 Melhorias | 80 | 8,1 dias |

> ⚠️ **Limitação importante:** classificação exclusivamente por palavras-chave pode gerar falsos positivos e falsos negativos. Para análises mais confiáveis, é preferível utilizar labels, categorias ou classificação semântica.

---

# 📈 Como interpretar o conjunto de métricas

O verdadeiro valor dessas métricas surge quando elas são analisadas **em conjunto**.

## 👥 Alta concentração de contribuições

Pode indicar que uma pequena parcela dos contribuidores concentra grande parte do conhecimento e das entregas.

**Pergunta de negócio:**

> Existe risco de continuidade caso essas pessoas deixem o projeto?

---

## ⏱️ Alto tempo de resolução + 💬 alto nível de atrito

Pode indicar que as mudanças estão demorando e exigindo grande volume de discussão.

**Pergunta de negócio:**

> O processo de revisão está criando um gargalo?

---

## 🔥 Muitos hotspots + alto volume de alterações

Pode indicar que determinadas partes do sistema concentram grande quantidade de evolução.

**Pergunta de negócio:**

> Existem componentes que deveriam ser investigados, refatorados ou desacoplados?

---

## 🤝 Alta quantidade de contribuições + baixa taxa de aceitação

Pode indicar uma diferença significativa entre o volume de contribuições recebidas e o volume incorporado.

**Pergunta de negócio:**

> O processo de contribuição está alinhado com as necessidades e critérios do projeto?

---

# 📊 Painel Executivo

Para uma apresentação à diretoria, as métricas podem ser resumidas da seguinte forma:

| Indicador | O que mede | Principal ponto de atenção |
|---|---|---|
| 👥 **Bus Factor** | Concentração de contribuições | Dependência de pessoas-chave |
| ⏱️ **Cadência** | Tempo de avaliação | Gargalos de processo |
| 💬 **Nível de Atrito** | Volume de discussão | Complexidade de colaboração |
| 🕐 **Perfil de Dedicação** | Distribuição temporal | Padrão de atividade |
| 🔥 **Hotspots** | Frequência de alterações | Concentração técnica |
| 🤝 **Merge Rate** | Aceitação de contribuições | Processo de integração |
| 🎯 **Bugs vs. Features** | Tempo por categoria | Distribuição do esforço |

---

# 🔬 Considerações Metodológicas

Para que os indicadores sejam comparáveis e úteis, recomenda-se registrar claramente:

- **Período analisado** — por exemplo, últimos 12 meses;
- **População analisada** — commits, Pull Requests abertas, Pull Requests encerradas etc.;
- **Fuso horário** utilizado;
- **Critério de classificação** das tarefas;
- **Tratamento de bots** e contas automatizadas;
- **Tratamento de contribuições duplicadas**;
- **Critério para considerar uma contribuição como aceita**;
- **Tamanho da amostra**;
- **Métricas estatísticas utilizadas** — média, mediana, P90/P95 etc.

---

# ⚠️ Uma métrica isolada não conta toda a história

Esses indicadores devem ser utilizados como **sinais para investigação**, e não como diagnósticos automáticos.

Um projeto pode apresentar alta concentração de contribuições porque possui um pequeno núcleo de mantenedores altamente ativos.

Um projeto com muitos comentários pode ter uma cultura de revisão extremamente detalhada.

Um arquivo frequentemente modificado pode ser um componente central que naturalmente evolui com frequência.

Portanto, a interpretação correta é:

```text
Métrica
   ↓
Sinal
   ↓
Investigação
   ↓
Contexto
   ↓
Decisão
