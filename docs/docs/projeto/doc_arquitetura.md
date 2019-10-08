# Alohomora - Portaria Virtual

### Arquitetura
#### Versão 1.0

## Histórico de Revisão
| Data         |  Versão  |                        Descrição                        |   Autor  |
| ------------- | ----------- | ---------------------------------------------------- | ---------- |
|  26/09/2019  | 1.0 | Criação da primeira versão do documento | Paulo Batista, Rodrigo Lima, Victor Gonçalves |
|  01/10/2019  | 1.1 | Revisão de erros ortográficos e sintaxe | João Luis Baraky, Victor Jorge Gonçalves |
| 06/10/2019 | 1.2 | Incremento de uma explicação básica do que é significa MVT | Rodrigo Lima, João Luis Baraky |
| 07/10/2019 | 1.2 | Adição dos objetivos, diagramas de pacotes e relações e melhoria no topico 5| João Luis Baraky, Rodrigo Lima |

## Sumário
__[1. Introdução](#1-introducao)__ \
[1.1 Objetivo](#11-objetivo) \
[1.2 Escopo](#12-escopo) \
[1.3 Definições, Acrônimos e Abreviações](#13-definicoes-acronimos-e-abreviacoes) \
[1.4 Referências](#14-referencias)

__[2. Representação da Arquitetura](#2-representacao-da-arquitetura)__ \
[2.1 Django](#21-django) \
[2.1.1 MVT](#211-mvt)\
[2.2 GraphQL](#22-graphql) \
[2.2.1 Graphene-Python](#221-graphene-python) \
[2.2.2 Graphene-Django](#222-graphene-django) \
[2.3 Vue.js](#23-vuejs)

__[3. Objetivos e Restrições da Arquitetura](#3-objetivos-e-restricoes-da-arquitetura)__ \
[3.1 Objetivos](#31-objetivos)
[3.2 Restrições](#32-restricoes)

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
|MVT|Model, View, Template|

### 1.4 Referências
Sistema de Registro em Curso - Documento de Arquitetura de Software; Disponível em: [http://mds.cultura.gov.br/extend.formal_resources/guidances/examples/resources/sadoc_v1.htm](http://mds.cultura.gov.br/extend.formal_resources/guidances/examples/resources/sadoc_v1.htm). Acesso em: 26 de setembro de 2019.
PATROCÍNIO, Sofia; GOUVEIA, Micaella; PEREIRA, Samuel; TAIRA, Luis; MUNIZ, Amanda. Chatbot Gaia: Arquitetura. Disponível em: [https://github.com/fga-eps-mds/2019.1-Gaia/blob/master/docs/projeto/DocArquitetura.md](https://github.com/fga-eps-mds/2019.1-Gaia/blob/master/docs/projeto/DocArquitetura.md). Acesso em: 26 de setembro de 2019. Padrões Arquiteturais MVC X Arquitetura do Django; Disponível em: [https://github.com/fga-eps-mds/A-Disciplina/wiki/Padr%C3%B5es-Arquiteturais---MVC-X-Arquitetura-do-Django](https://github.com/fga-eps-mds/A-Disciplina/wiki/Padr%C3%B5es-Arquiteturais---MVC-X-Arquitetura-do-Django). Acesso em: 05 de outubro de 2019.

## 2. Representação da Arquitetura
### 2.1 Django
Django é um Python Web framework de alto-nível que encoraja o desenvolvimento rápido e organizado. O framework enfatiza a reusabilidade e conectividade de componentes, sendo assim,utiliza-se menos código.
Aplica-se a arquitetura Model-View-Template (MVT).
### 2.1.1 MVT
* Model - É a parte que representa as classes, além de ser a parte responsavel por ler e escrever informações no banco de dados, para isso cada classe da model representa uma tabela do banco de dados.
* View - É a comunicação entre a Model e a Template. É nela que há o tratamento de informações recebidas e o retorno para o usuário.
* Template - É a parte da visão de usuário. Geralmente usa HTML, CSS, javascript, etc. Normalmente é focada na apresentação da aplicação para o usuário.


### 2.2 GraphQL
GraphQL é uma linguagem de busca para APIs que fornece uma descrição completa dos dados da API e dispoẽ o poder de solicitar exatamento o que o usuário necessita. Tais funcionalidades contribuem na eficiência e velocidade no desenvolvimento de aplicações.
### 2.2.1 Graphene-Python
Graphene-Python é uma biblioteca que oferece as funcionalidades do GraphQL para o Python. Seu objetivo principal é dispor uma rica API para facilitar o desenvolvimento de aplicações.

### 2.2.2 Graphene-Django
Graphene-Django é construído em cima do Graphene. Fornece uma camada de abstração adicional que torna mais fácil implementar GraphQl em um projeto Django.

### 2.3 Vue.js
Vue é um framework progressivo do JavaScript de código aberto para construir interfaces de usuários. Diferente de outros frameworks, Vue é projetado desde o ínicio para ser adotável de forma incremental. O Vue também pode funcionar como uma estrutura de aplicativos web capaz de alimentar aplicativos avançados de um única página.

## 3. Objetivos e Restrições da Arquitetura

### 3.1 Objetivos
- Deve ser possível estruturar o condomínio (blocos e apartamentos) e cadastrar moradores manualmente;
- Fornecer a funcionalidade de autenticação de usuário, morador e visitante, via voz;
- O sistema deve estabelecer uma comunicação com o usuário via áudio, de forma a colher informações necessárias para autorização da entrada;
- Deve ser possível fazer o cadastro de um visitante via voz;
- É necessário ter uma comunicação com o morador com o intuito de notificar a chegada de um visitante;
- O morador deverá ter o poder se permitir ou não a entrada de um visitante que o referencia.

### 3.2 Restrições
- O hardware deve estar conectado a internet.
- O sistema deve estar integrado ao banco de dados para a autenticação dos usuários.
- O sistema deve estar integrado a um bot no Telegram para interação com os usuários.
- Os usuários moradores devem ter o aplicativo Telegram instalado e internet para a comunicação com o sistema via bot.
- O hardware deve ter um microfone para a gravação de voz, pois precisa-se da voz para a autenticação.

## 4. Visão Lógica
### 4.1 Visão Geral
A portaria virtual Alohomora está sendo construída em Django, utilizando da ferramenta de busca GraphQL, integrada com Graphene-Django. O objetivo principal ao usar o Django é ter uma organização que facilite o trabalho e a adaptação do grupo. O GraphQL fornece velocidade na busca de dados e eficiência.

### 4.2 Diagrama de Relações

![Diagrama_Relações](https://imgur.com/vDmAmoT.png)

### 4.3 Diagrama de Pacotes

![Diagrama_Pacotes](https://imgur.com/Tx87mx5.png)

## 5. Qualidade
- Utilização de algorítimos otimizados para autenticação de usuário pelas voz.
- Utilização de boas práticas no desenvolvimento do projeto.
- Utilização de ferramentas que garantem velocidade e produtividade, como o GraphQL e Django.
- Facilidade para integração com outras bibliotecas e serviços.
- Fornecer um produto final o mais eficiente e otimizado possível.
