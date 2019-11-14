# Changelog


 ## Release 1 - 10 Outubro de 2019
 ### Adicionado
 * Guia de contribuição do projeto
 * Estrutura padrão do condominio
 * Adicionado docker-compose para rodar o site locamente

## [Unreleased]
* Correção do bug na query de admins

### Adicionado
* Na *mutation* **createResident** e na *query* **voiceBelongsUser**, agora são pedidos os atributos *audioSpeakingName* e *audioSamplerate*
* A *query* **voiceBelongsUser** agora possui um novo estágio de filtragem baseado no atributo *audioSpeakingName*

### Alterado
* Ajustes do código a um novo padrão de lint e remoção de algumas regras
* Atributos que representam características de áudio agora são armazenados como *Array* de *Float*
* Os campos de áudio na *mutation* **createResident** e na *query* **voiceBelongsUser** agora obedecem ou tipo **[Float]!** ou o tipo **[Float]** 


## [0.2.0] - 2019-10-15
### Adicionado
*  Melhores regras no pytlintrc
*  Novo atributo na model User que carrega os dados MFCC do áudio do usuário dizendo o próprio nome. Juntamente de um campo na mutation de criação de User pra esse novo atributo.
*  Adicionado query e mutation para criar e buscar feedbacks do sistema
*  Adição das fixtures e comando para popular o banco de forma cômoda.

## [0.2.0] - 2019-10-15
### Adicionado
*  Novo modelo que permite registrar o horário de entrada toda vez que um Morador entrar no condomínio
*  Criação de UPDATE e DELETE no schema para a API.
*  Criação da autenticação por models
*  Criação da mutation para ativar o usuário

## [0.2.0] - 2019-10-20
### Adicionado
*  Funcionalidade para armazenamento de dados de entrada de visitante

## [0.2.0] - 2019-10-24
### Adicionado
*  Nova query que permite listar o usuários não ativados.
*  Remoção de alguns campos da model Visitor

## [0.2.0] - 2019-10-30
### Adicionado
* Nova model de Admin.
* Nova query que permite a listagem de Admins.
* Nova query que informa acerca de um dado Admin.
* Nova mutation que cria novos Admins.
* Nova mutation que exclui Admins.

## [0.2.0] - 2019-10-31
### Alterado
*  Argumento "python -m" adicionado antes do "pip install" no Dockerfile

## [0.2.0] - 2019-11-02
### Alterado
* Mudança na organização dos arquivos do schema e do teste de accounts.

## [0.2.0] - 2019-11-03
### Adicionado
*  Nova mutation update e delete da model EntryVisitor.


 ---
 
 Modelo padrão do changelog disponível [aqui](https://keepachangelog.com/en/0.3.0/).
