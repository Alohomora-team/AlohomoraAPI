# Changelog

Todas as mudanças notáveis no sistema você encontra aqui.

---

## [Unreleased]

### Adicionado
- Campos ***audioSpeakingName*** e ***audioSamplerate*** adicionados na *mutation* de [criação de morador](https://github.com/Alohomora-team/2019.2-AlohomoraPage/blob/master/docs/projeto/guia_de_uso.md#211-criando-um-morador) e na *query* de [autênticação do morador](https://github.com/Alohomora-team/2019.2-AlohomoraPage/blob/master/docs/projeto/guia_de_uso.md#31-autenticação-de-morador)

- Disponibilizadas maneiras de criar e consultar *feedbacks*

- [*Fixtures*](https://django.readthedocs.io/en/2.2.x/howto/initial-data.html) e comandos para popular o banco de dados.

- Mecanismo de [*Entry*](https://github.com/Alohomora-team/2019.2-AlohomoraPage/blob/master/docs/projeto/guia_de_uso.md#4-logs-de-entrada) que possibilita o registro do horário de entrada do morador

- Disponibilização de [*CRUD*](https://github.com/Alohomora-team/2019.2-AlohomoraPage/blob/master/docs/projeto/guia_de_uso.md#2-crud) para as entidades já existentes na API

- Autenticação por models

- Entidade [*administrador*](https://github.com/Alohomora-team/2019.2-AlohomoraPage/blob/master/docs/projeto/guia_de_uso.md#5-administração), juntamente com mecanismo de *CRUD*.

- Mecanismo de [ativar/desativar usuário](https://github.com/Alohomora-team/2019.2-AlohomoraPage/blob/master/docs/projeto/guia_de_uso.md#52-gerênciando-conta-de-usuários), bem como a consulta de usuários ativados ou desativados.


### Modificado
- Refatoração na estrutura de arquivos de *schema* e nos testes de *accounts*
- Regras do [*Pylint*]() modificadas 
- Código refatorado a fim de cobrir as mudanças no [*Pylint*]()

### Removido
*  Remoção dos atributos *email, phone, voiceData e owner* da entidade [*Visitor*](https://github.com/Alohomora-team/2019.2-AlohomoraPage/blob/master/docs/projeto/guia_de_uso.md#22-visitante) 

### Corrigido
-  Argumento "python -m" adicionado antes do "pip install" no [*Dockerfile*](docker/Dockerfile)

---

## Release 1 - 10 Outubro de 2019
### Adicionado
* Guia de contribuição do projeto
* Estrutura padrão do condominio
* Adicionado docker-compose para rodar o site locamente

---
 
As convenções seguidas para escrever esse texto estão disponíveis [aqui](https://keepachangelog.com/en/0.3.0/).
