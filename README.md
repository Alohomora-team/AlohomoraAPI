[![Build Status](https://travis-ci.org/fga-eps-mds/Alohomora.svg?branch=devel)](https://travis-ci.org/fga-eps-mds/Alohomora)

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
