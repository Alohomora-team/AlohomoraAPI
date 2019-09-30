# Alohomora - Portaria Virtual

### Arquitetura
#### Versão 1.0

## Histórico de Revisão
| Data         |  Versão  |                        Descrição                        |   Autor  |
| ------------- | ----------- | ---------------------------------------------------- | ---------- |
|  26/09/2019  | 1.0 | Criação da primeira versão do documento | Paulo Batista, Rodrigo Lima, Victor Gonçalves |

## Sumário
__[1. Introdução](#_1-introdução)__\
[1.1 Objetivo](#_11-objetivo)\
[1.2 Escopo](#_12-escopo)\
[1.3 Definições, Acrônimos e Abreviações](#_13-definições-acrônimos-e-abreviações)\
[1.4 Referências](#_14-referências)

__[2. Representação da Arquitetura](#_2-representação-da-arquitetura)__\
[2.1 Django](#_21-django)\
[2.2 Graphql](#_22-graphql)\
[2.2.1 Graphene-Python](#_221-graphene-python)\
[2.2.1.1 Graphene-Django](#_2211-graphene-django)\
[2.3 Vue.js](#_23-vue.js)

__[3. Objetivos e Restrições da Arquitetura](#_3-objetivos-e-restrições-da-arquitetura)__\
[3.1 Restrições](#_31-restrições)

__[4. Visão Lógica](#_4-visão-lógica)__\
[4.1 Visão Geral](#_41-visão-geral)

__[5. Qualidade](#_5-qualidade)__


## 1. Introdução
### 1.1 Objetivo
Este documento oferece mostrar a arquitetura utilizada da portaria virtual Alohomora, e     mostrar aos envolvidos cada parte da aplicação. Destina-se transmitir aos interessados as decisões arquiteturais que foram tomadas.

### 1.2 Escopo
Este documento fornece uma visão da arquitetura do Alohomora, um sistema de portaria virtual.
Alohomora, é um projeto realizado para as disciplinas Métodos de Desenvolvimento de Software(MDS) e Engenharia de Produto de Software(EPS), do curso Engenharia de Software da Faculdade UnB Gama (FGA) da Universidade de Brasília(UnB).

### 1.3 Definições, Acrônimos e Abreviações
| Acrônimo/Abreviação | Definição |
| ----------------------------- | ------------ |
| API | Application programming interface |
| MDS | Métodos de Desenvolvimento de Software |
| EPS | Engenharia de Produto de Software |

### 1.4 Referências
Sistema de Registro em Curso - Documento de Arquitetura de Software; Disponível em: [http://mds.cultura.gov.br/extend.formal_resources/guidances/examples/resources/sadoc_v1.htm](http://mds.cultura.gov.br/extend.formal_resources/guidances/examples/resources/sadoc_v1.htm). Acesso em: 26 de setembro de 2019.
PATROCÍNIO, Sofia; GOUVEIA, Micaella; PEREIRA, Samuel; TAIRA, Luis; MUNIZ, Amanda. Chatbot Gaia: Arquitetura. Disponível em: [https://github.com/fga-eps-mds/2019.1-Gaia/blob/master/docs/projeto/DocArquitetura.md](https://github.com/fga-eps-mds/2019.1-Gaia/blob/master/docs/projeto/DocArquitetura.md). Acesso em: 26 de setembro de 2019.

## 2. Representação da Arquitetura
### 2.1 Django
DJango é um Python Web framework de alto-nível que encoraja o desenvolvimento rápido e organizado. O framework enfatiza a reusabilidade e conectividade de componentes, sendo assim, utiliza de menos código.
Utiliza o modelo model-template-view MTV.
### 2.2 Graphql
GraphQL é um novo padrão que fornece uma mais eficiente, poderosa e flexível alternativo para o REST. GraphQL permite que seja especificado exatamente qual informação precisa de uma API.
GraphQL é uma  linguagem query, no qual não é conectado em nenhuma database ou serviço de armazenamento.
GraphQL traz algumas vantagens em relação ao REST:
 * Busca por informações de forma eficiente, pois utiliza apenas um endpoint.
 * Variedade de diferentes front-end frameworks e plataformas, com graphql pode acessar precisamente a informação necessária sem se preocupar.
 * Desenvolvimento rápido.

### 2.2.1 Graphene-Python
Graphene-Python é uma livraria para construir uma API GraphQL em python facilmente, seu objetivo principal é prover um simples, mas extensiva API para fazer a vida dos desenvolvedores mais fácil.

### 2.2.1.1 Graphene-Django
Graphene-Django é construído em cima do Graphene. Graphene-Django fornece uma camada de abstração adicional que torna mais fácil de adicionar GraphQL funcionalidades para o projeto Django.

### 2.3 Vue.js
Vue é um framework progressivo do JavaScript de código aberto para construir interfaces de usuários. Diferente de outros frameworks, Vue é projetado desde o ínicio para ser adotável de forma incremental O Vue também pode funcionar como uma estrutura de aplicativos web capaz de alimentar aplicativos avançado de um única página. 

## 3. Objetivos e Restrições da Arquitetura
### 3.1 Restrições
Requisitos chave e restrições do sistema que têm relacionamento significativo com a arquitetura:
 * O hardware deve estar conectado a internet.
 * O sistema deve estar integrado ao banco de dados para a autenticação dos usuários.
 * O sistema deve estar integrado a um bot no Telegram para interação com os usuários.
 * Os usuários moradores devem ter o aplicativo Telegram instalado e internet para a comunicação com o sistema via bot.
 * O hardware deve ter um microfone para a gravação de voz, pois precisa-se da voz para a autenticação.

## 4. Visão Lógica
### 4.1 Visão Geral
A portaria virtual Alohomora está sendo construída em na linguagem Python com a utilização do framework Django, da ferramenta de busca GraphQL, do Graphene-Django que facilita a integração com o GraphQl. O objetivo principal ao usar o Django é ter uma organização que facilite o trabalho e a adaptação do grupo, ao usar o GraphQL é ter maior velocidade na busca de dados pois ele retorna exatamente os dados pesquisados, sem nenhum excesso.
## 5. Qualidade
O algoritmo utilizando de técnicas para aumentar a velocidade do algoritmo, é possível fazer uma  autenticação rápida e eficiente.
No projeto é utilizado boas práticas. 
Com a utilização do graphql a velocidade da usabilidade e desenvolvimento do projeto vai aumentar.
Facilidade para integração com outras bibliotecas e serviços.
