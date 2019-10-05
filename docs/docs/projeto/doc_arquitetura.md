# Alohomora - Portaria Virtual

### Arquitetura
#### Versão 1.0

## Histórico de Revisão
| Data         |  Versão  |                        Descrição                        |   Autor  |
| ------------- | ----------- | ---------------------------------------------------- | ---------- |
|  26/09/2019  | 1.0 | Criação da primeira versão do documento | Paulo Batista, Rodrigo Lima, Victor Gonçalves |
|  01/10/2019  | 1.1 | Revisão de erros ortográficos e sintaxe | João Luis Baraky, Victor Jorge Gonçalves |

## Sumário
__[1. Introdução](#1-introducao)__ \
[1.1 Objetivo](#11-objetivo) \
[1.2 Escopo](#12-escopo) \
[1.3 Definições, Acrônimos e Abreviações](#13-definicoes-acronimos-e-abreviacoes) \
[1.4 Referências](#14-referencias)

__[2. Representação da Arquitetura](#2-representacao-da-arquitetura)__ \
[2.1 Django](#21-django) \
[2.2 GraphQL](#22-graphql) \
[2.2.1 Graphene-Python](#221-graphene-python) \
[2.2.2 Graphene-Django](#222-graphene-django) \
[2.3 Vue.js](#23-vuejs)

__[3. Objetivos e Restrições da Arquitetura](#3-objetivos-e-restricoes-da-arquitetura)__ \
[3.1 Restrições](#31-restricoes)

__[4. Visão Lógica](#4-visao-logica)__ \
[4.1 Visão Geral](#41-visao-geral)

__[5. Qualidade](#5-qualidade)__


## 1. Introdução
### 1.1 Objetivo
Este documento pretende mostrar a arquitetura utilizada da portaria virtual Alohomora, e mostrar aos envolvidos cada parte da aplicação. Destina-se transmitir aos interessados as decisões arquiteturais que foram tomadas.

### 1.2 Escopo
Este documento fornece uma visão da arquitetura do Alohomora, um sistema de portaria virtual.
Alohomora, é um projeto realizado para as disciplinas Métodos de Desenvolvimento de Software(MDS) e Engenharia de Produto de Software(EPS), do curso Engenharia de Software da Faculdade UnB Gama (FGA) da Universidade de Brasília(UnB).

### 1.3 Definições, Acrônimos e Abreviações
| Acrônimo/Abreviação | Definição |
| ----------------------------- | ------------ |
| API | Application Programming Interface |
| MDS | Métodos de Desenvolvimento de Software |
| EPS | Engenharia de Produto de Software |

### 1.4 Referências
Sistema de Registro em Curso - Documento de Arquitetura de Software; Disponível em: [http://mds.cultura.gov.br/extend.formal_resources/guidances/examples/resources/sadoc_v1.htm](http://mds.cultura.gov.br/extend.formal_resources/guidances/examples/resources/sadoc_v1.htm). Acesso em: 26 de setembro de 2019.
PATROCÍNIO, Sofia; GOUVEIA, Micaella; PEREIRA, Samuel; TAIRA, Luis; MUNIZ, Amanda. Chatbot Gaia: Arquitetura. Disponível em: [https://github.com/fga-eps-mds/2019.1-Gaia/blob/master/docs/projeto/DocArquitetura.md](https://github.com/fga-eps-mds/2019.1-Gaia/blob/master/docs/projeto/DocArquitetura.md). Acesso em: 26 de setembro de 2019.

## 2. Representação da Arquitetura
### 2.1 Django
Django é um Python Web framework de alto-nível que encoraja o desenvolvimento rápido e organizado. O framework enfatiza a reusabilidade e conectividade de componentes, sendo assim, utiliza-se menos código.
Aplica-se a arquitetura Model-Template-View (MTV).
### 2.2 GraphQL
GraphQL é uma linguagem de busca para APIs que fornece uma descrição completa dos dados da API e dispoẽ o poder de solicitar exatamento o que o usuário necessita. Tais funcionalidades contribuem na eficiência e velocidade no desenvolvimento de aplicações.
### 2.2.1 Graphene-Python
Graphene-Python é uma biblioteca que oferece as funcionalidades do GraphQL para o Python. Seu objetivo principal é dispor uma rica API para facilitar o desenvolvimento de aplicações.

### 2.2.2 Graphene-Django
Graphene-Django é construído em cima do Graphene. Fornece uma camada de abstração adicional que torna mais fácil implementar GraphQl em um projeto Django.

### 2.3 Vue.js
Vue é um framework progressivo do JavaScript de código aberto para construir interfaces de usuários. Diferente de outros frameworks, Vue é projetado desde o ínicio para ser adotável de forma incremental. O Vue também pode funcionar como uma estrutura de aplicativos web capaz de alimentar aplicativos avançados de um única página.

## 3. Objetivos e Restrições da Arquitetura
### 3.1 Restrições
Requisitos chave e restrições do sistema que têm relacionamento significativo com a arquitetura:

- O hardware deve estar conectado a internet.
- O sistema deve estar integrado ao banco de dados para a autenticação dos usuários.
- O sistema deve estar integrado a um bot no Telegram para interação com os usuários.
- Os usuários moradores devem ter o aplicativo Telegram instalado e internet para a comunicação com o sistema via bot.
- O hardware deve ter um microfone para a gravação de voz, pois precisa-se da voz para a autenticação.

## 4. Visão Lógica
### 4.1 Visão Geral
A portaria virtual Alohomora está sendo construída em Django, utilizando da ferramenta de busca GraphQL, integrada com Graphene-Django. O objetivo principal ao usar o Django é ter uma organização que facilite o trabalho e a adaptação do grupo. O GraphQL fornece velocidade na busca de dados e eficiência.
## 5. Qualidade
- Utilização de algorítimos otimizados para autenticação de usuário pelas voz.
- No projeto é utilizado boas práticas.
- Utilização de ferramentas que garantem velocidade e produtividade, como o GraphQL.
- Facilidade para integração com outras bibliotecas e serviços.
