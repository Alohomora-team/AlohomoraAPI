# AlohomoraAPI
[![Build Status](https://travis-ci.org/fga-eps-mds/2019.2-Alohomora.svg?branch=devel)](https://travis-ci.org/fga-eps-mds/2019.2-Alohomora)
[![Coverage Status](https://coveralls.io/repos/github/fga-eps-mds/2019.2-Alohomora/badge.svg?branch=devel)](https://coveralls.io/github/fga-eps-mds/2019.2-Alohomora?branch=devel)
[![Maintainability](https://api.codeclimate.com/v1/badges/2c164a8849badef20a10/maintainability)](https://codeclimate.com/github/Alohomora-team/AlohomoraAPI/maintainability)
![Logo](logo_alohomora.png)

## Descrição

AlohomoraAPI é um sistema idealizado para a **gerência de portarias** de condomínios ou prédios. O sistema conta com uma ferramenta de **autênticação por voz** para os moradores. Também são disponibilizados *endpoints* que facilitam a sua **integração** com diversos outros **dispositivos** e sistemas terceiros, como **[Telegram](https://telegram.org)**, que funciona como uma ponte entre o **sistema e o usuário real**.

### Integração com IoT
**Alohomora** conta com uma interface de comunicação que permite a sua **integração** com dispositivos de **IoT**.

> Alohomora é aditivo e fácil de se integrar na composição de novos grandes sistemas

[Confira as funcionalidades!](https://github.com/Alohomora-team/2019.2-AlohomoraPage/blob/10-criar-documentacao-uso-api/docs/uso/guia_de_uso.md)

### Como subir a aplicação

#### Usando o ambiente via docker-compose

1. Buildando a aplicação API

```bash
docker-compose build api
```

2. Subindo o banco de dados

```bash
docker-compose up -d db
```

3. Rodando as migrações do banco de dados

```bash
docker-compose run api migrate
```

4. Subindo o servidor django

```bash
docker-compose up api
```

Após esses comandos a aplicação estará disponível em http://localhost:8000.


#### Realizando testes localmente

Para realizar os testes do pytlint locamente basta utilizar o comando abaixo. É válido lembrar que essa verificação é a mesma que acontece na nossa pipeline de integração continua, portanto é muito difícil a análise ser realizada com sucesso na sua máquina e ocorrer um erro no CI.

```bash
docker-compose up lint
```

#### Rodando nosso site locamente

Para verificar localmente como sua contribuição para nossa documentação vai aparecer em nosso site basta utilizar o serviços docs no nosso arquivo docker-compose.

```bash
docker-compose up docs
```

O comando acima irá levantar um servidor mkdocs via docker na porta 8080 do seu computador. Além disso existe um volume que sincroniza os arquivos do seu computador com o que é apresentado dentro do container docker.


## O que o Alohomora


Link da apresentação no [drive](https://docs.google.com/presentation/d/1Stq0aMrGHJtB4bNKjKWnblM6ARlbEPcDAjC2B-zUUU0/edit?usp=sharing)
