### Issues

A issue é o principal elemento de acompanhanto do projeto. Portanto tenha muito cuidado na escrita da mesma e preencha todas as informações necessárias para o acompanhamento como:

* milestones - sempre escolha a última milestone criada (cada milestone representa uma sprint)
* labels - Coloque labels significativa para a tarefa
* assigne - Pessoa (ou equipe) responsável por trabalhar naquela issue.
* epico - Caso a sua issue não seja uma issue de bug ou melhoria é altamente recomendado estar sempre ligado a um épico.
* estimate - Pontuação que o time elegeu para esse trabalho

#### Criando uma issue e templates

Nosso projeto tem vários templates de issue para diferentes situações, acreditamos que para maioria das situações você terá um template que atenderá sua necessidade, porém caso não encontre sinta-se livre para escrever uma com o máximo de detalhes possíveis.

#### Referenciando uma issue em um commit

Ainda sobre as issue, na mensagem de cada commit pedimos que o contribuidor referencie a issue pelo seu número. Essa abordagem ajuda nossa equipe a ter maior controle do código e identificar rapidamente as contribuições do projeto.

### Branches

Nossa politica de branch é muito simples, caso queira contribuir é totalmente indicado realizar um fork do projeto e realizar um pull request para a branch *devel*. No caso de um membro da equipe mantenedora do projeto é permitido que crie uma branch no proprio repositório também a partir da devel.

Independente do seu quadro de contribuição é norma do projeto nomear as branches com um nome significativo (baseado no texto da issue). Por exemplo a issue **Criar página de login** com número 13 seria nomeada da seguinte forma:

```bash
13-criar-pagina-login
```

De forma mais genérica a nossa normalização é:

```
<numero da issue>-<primeiro nome>-<segundo nome>-<terceiro ...>
```

### Pull Request

Agora que você já conhece como fazer sua issue, gerou uma branch e escreveu o seu maravilhoso código vamos realizar sua contribuição no repositório!

#### Criando um PR

Assim como nas issues o projeto tem um template de PR que lhe auxiliará na escrita do mesmo. O importante é deixar claro sua contribuição e o que foi feito, dessa forma estará facilitando muito a vida de todos os nossos revisores :).

Fora casos extremamente especificos todos os PRs devem ser realizados baseados na branch *devel*.
