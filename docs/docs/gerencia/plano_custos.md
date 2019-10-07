## 1. Introdução

Este documento procura explicar como serão gerenciados os custos do projeto e irá mostrar as técnicas que serão utilizadas para medição e manutenção dos custos.

## 2. Processo para gerenciamento dos custos do projeto

O processo será baseado no plano de gerenciamento de custo descrito no PMBOK, que contém as seguintes quatro fases: planejamento de custos, estimativa de custos, determinação do orçamento e controle dos custos.

### 2.1 Estimativa de custos

De acordo com o PMBOK, estimar os custos consiste em desenvolver uma estimativa dos recursos necessários para a execução das atividades do projeto. As estimativas incluem a identificação e a consideração das alternativos de custo para iniciar e terminar o projeto.

No processo de estimativa dos custos, as técnicas utilizadas serão as de estimativa análoga e bottom-up, onde:

- Estimativa análoga: se baseia na experiência dos membros da equipe em projetos semelhantes;
- Estimativa bottom-up: se baseia na estrutura analítica do projeto para estimar os custos, partindo do nível mais baixo da estrutura

### 2.2 Determinação do orçamento

O cálculo utilizado para determinar o valor do orçamento é baseado no número de horas trabalhadas multiplicado pelo preço da hora

```
Orçamento = Horas Trabalhadas * Preço da Hora
```

### 2.3 Controle de custos

O controle de custos será feito por meio da EVM (*Earned Value Management*, Gerenciamento do Valor Agregado, em português) ao decorrer do projeto.

A EVM procura monitorar três indicadores:

- Valor Planejado (VP)

Será estimado a partir das horas e será dado em reais. Aqui entra o número de horas de trabalho planejadas para cada membro da equipe, multiplicado pelo número de integrantes e pelo custo da hora trabalhada.

- Valor Agregado (VA)

Medida de trabalho executado de acordo com o orçamento autorizado para o trabalho em questão. Calculado pela multiplicação do valor planejado da atividade pela porcentagem concluída dessa atividade (no fim do tempo planejado).

- Custo Real (CR)

Mostra o quanto foi gasto na execução do trabalho. Calculado pela multiplicação das horas gastas pelos integrantes pelo preço da hora.


## 3. Regras de medição de desempenho

Com o auxílio da EVM, a análise será feita a partir de dois índices de eficiência:

- Índice de desempenho de custos (IDC)
- Índice de desempenho de prazos (IDP)


### 3.1 IDC
O IDC mede a eficiência dos custos em relação ao orçamento planejado, calculado pelo valor agregado dividido pelo custo real. Para fins de análise, o IDC pode entrar em três diferentes intervalos:

- IDC > 1

Indica custo mais baixo que o planejado

- IDC = 1

Indica custo conforme o planejado

- IDC < 1

Indica custo mais alto que o planejado


### 3.2 IDP

Mede a eficiência do cronograma. Calculado dividindo o valor agregado pelo planejado. Para fins de análise, o IDP pode entrar em três diferentes intervalos:

- IDP > 1

Indica adiantamento

- IDP = 1

Indica que está no prazo

- IDP < 1

Indica atraso


## 4. Referências

YOSHIDA, Eduardo; SILVA, Guilherme; SOUZA, Kamilla; VITOR, Lucas. Aix - Plano de Gerenciamento de Custos. Disponível: em https://fga-eps-mds.github.io/2019.1-Aix/gerencia/2019/04/05/plano-de-gerenciamento-de-custos/. Acesso em 03 de outubro de 2019.
<br/><br/>
SOARES, João; ARAÚJO, Marcelo; HENRIQUE, Ronyell; NOGUEIRA, Thiago. ReceitaMais - Plano de Gerenciamento de Custo. Disponível em: https://github.com/fga-eps-mds/2017.2-Receita-Mais/wiki/Plano-de-Gerenciamento-de-Custo. Acesso em 03 de outubro de 2019.
<br/><br/>
Project Management Institue. A Guide to the Project Management Body of Knowledge 5th Edition. EUA: PMI, 2013.