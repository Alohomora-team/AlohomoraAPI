# AlohomoraAPI

[![Build Status](https://travis-ci.org/Alohomora-team/AlohomoraAPI.svg?branch=devel)](https://travis-ci.org/Alohomora-team/AlohomoraAPI)
[![Coverage Status](https://coveralls.io/repos/github/Alohomora-team/AlohomoraAPI/badge.svg?branch=devel)](https://coveralls.io/github/Alohomora-team/AlohomoraAPI?branch=devel))
[![Maintainability](https://api.codeclimate.com/v1/badges/2c164a8849badef20a10/maintainability)](https://codeclimate.com/github/Alohomora-team/AlohomoraAPI/maintainability)

![Logo](logo_alohomora.png)

## Descrição

[*AlohomoraAPI*](https://docs.google.com/presentation/d/1Stq0aMrGHJtB4bNKjKWnblM6ARlbEPcDAjC2B-zUUU0/edit?usp=sharing) é um sistema idealizado para a **gerência de portarias** de condomínios e prédios. Escrito em [*Python*](https://www.python.org) com o auxílio do [*framework Django*](https://www.djangoproject.com), o sistema visa resolver problemas de custo com portaria e fornecer autonomia aos moradores.

 O sistema conta com uma ferramenta de **biometria de voz**, fazendo com que a **voz do morador** se torne a sua própria **chave**. Tal funcionalidade faz com que o uso de **senhas se torne algo secundário**.
 
  *Alohomora* disponibiliza *endpoints* que facilitam a **integração** com diversos outros **dispositivos** e sistemas, como **[Telegram](https://telegram.org)**, por exemplo, que pode funcionar como uma ponte entre o **sistema e o usuário**.
  
  > Conheça também o [*AlohomoraBot*](https://github.com/Alohomora-team/2019.2-AlohomoraBot)!

### Funcionalidades
*Alohomora* possui um conjunto de funcionalidades que possibilitam a implatação de uma portaria automatizada, dinâmica e descritiva em relação a entrada de pessoas. As funcionalidades do *Alohomora* podem proporcionar
- Entrada do morador sem necessidade de revisão humana (porteiros)
- Autonomia ao morador para gerenciar visitas mesmo não estando presente fisicamente
- Controle sobre o fluxo de entradas, rastreando *quem*, *quando* e *para onde*

[Confira as funcionalidades](https://github.com/Alohomora-team/2019.2-AlohomoraPage/blob/10-criar-documentacao-uso-api/docs/uso/guia_de_uso.md)

### Alohomora + IoT

<p align="center">
  <img width="200" height="180" src="iot.png">
</p>

***Alohomora*** conta também com uma interface de comunicação baseada no [Home Assistant](https://www.home-assistant.io) que permite a sua **integração** com dispositivos de **IoT**, revelando um novo horizonte de **expansões e melhorias** para o sistema de **portaria como um todo**.

---

## Instalação


### Clonando o repositório

A instalação do *Alohomora* pode ser feita usando um terminal com a extensão do **git**. Também é **necessário** que você tenha o ***Docker*** **instalado no computador**. Caso você ainda não tenha, conheça o [*Docker*](https://docs.docker.com).

1. Abra o terminal e mude para um diretório de sua escolha para receber os arquivos do repositório. Depois, execute o seguinte comando
```bash
$ git clone https://github.com/Alohomora-team/AlohomoraAPI.git
```


2. Entre dentro da pasta AlohomoraAPI e execute o comando
```bash
$ docker-compose build api
```

Caso tudo tenha ocorrido sem erros, a aplicação já está pronta para ser executada

---

## Executando a aplicação

#### Usando o ambiente via docker-compose

1. Crie o *build* da aplicação

```bash
$ docker-compose build api
```

2. Suba o banco dados

```bash
$ docker-compose up -d db
```

3. Rode as migrações do banco de dados

```bash
$ docker-compose run api migrate
```

4. Suba o servidor django

```bash
$ docker-compose up api
```

Após esses comandos a aplicação estará disponível em http://localhost:8000. Os *endpoints* estarão acessíveis em http://localhost:8000/graphql.

Confira as funcionalidades e como as utilizar [aqui](https://github.com/Alohomora-team/2019.2-AlohomoraPage/blob/10-criar-documentacao-uso-api/docs/uso/guia_de_uso.md).

---

## Como contribuir

Para contribuir com o projeto confira o [guia de contribuição](/CONTRIBUTING.md).

---

## Equipe

> #### Scrum master
> Felipe Borges - [@bumbleblo](https://github.com/Bumbleblo)

> #### Product Owner
> Mateus Nóbrega - [@mateusnr](https://github.com/mateusnr)

> #### DevOps
> Samuel Borges - [@BordaLorde](https://github.com/BordaLorde)

> #### Desenvolvedores
> Aline Lermen - [@AlineLermen](https://github.com/AlineLermen)
>
> João Baraky - [@baraky](https://github.com/baraky)
>
> Luis Furtado - [@luis-furtado](https://github.com/luis-furtado)
>
> Paulo Batista - [@higton](https://github.com/higton)
>
> Rodrigo Lima - [@RodrigoTCLima](https://github.com/RodrigoTCLima)
>
> Victor Silva - [@VictorJorgeFGA](https://github.com/VictorJorgeFGA)

---

## Licença

Licença [MIT](/LICENSE)
