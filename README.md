# Magic Forest

Magic Forest é um jogo 2D desenvolvido em Python com a biblioteca Pygame. O jogador controla um guarda florestal que precisa coletar cristais, enfrentar golems e derrotar o Rei Golem para vencer a partida.

## Objetivo do jogo

O objetivo principal é coletar 10 cristais espalhados pelo cenário. Após coletar todos os cristais, o Rei Golem aparece. Para vencer, o jogador deve derrotá-lo utilizando flechas.

## Controles

- Setas do teclado: movimentam o guarda florestal
- Barra de espaço: atira flechas
- Enter: seleciona opções no menu
- Esc: retorna ou sai da fase atual

## Funcionalidades

- Menu inicial com opções de iniciar o jogo (Start Game), visualizar score (Score) e sair (Exit)
- Cenário com efeito de parallax
- Coleta de cristais
- Golems comuns com movimentação e ataque
- Sistema de flechas para atacar inimigos
- Rei Golem com barra de vida
- Sistema de pontuação
- Ranking de pontuações com SQLite3
- Uso do padrão de projeto Proxy para acesso ao banco de dados

## Sistema de pontuação

A pontuação é calculada com base no desempenho do jogador durante a partida:

- Cada cristal coletado soma 100 pontos
- Cada golem derrotado soma 50 pontos
- Cada ponto de vida restante do guarda soma 2 pontos
- Ao vencer o jogo, o jogador recebe um bônus de 1000 pontos

Ao final da partida, a pontuação é salva em um banco de dados SQLite.

## Banco de dados SQLite3

O jogo utiliza SQLite3 para armazenar as melhores pontuações. Os dados são salvos em uma tabela chamada `dados`, contendo:

- `id`: identificador da pontuação
- `name`: nome do jogador
- `score`: pontuação obtida
- `date`: data e horário da pontuação

## Design Pattern utilizado

### Proxy

O projeto utiliza o padrão de projeto Proxy por meio da classe `DBProxy`.

A classe `DBProxy` controla o acesso ao banco de dados SQLite. Em vez de outras partes do jogo acessarem diretamente o banco, elas utilizam o Proxy para salvar e buscar pontuações.

Isso melhora a organização do código, pois centraliza as operações de banco de dados em uma única classe.

## Estrutura principal do projeto

```text
MagicForest/
├── main.py
├── code/
│   ├── background.py
│   ├── config.py
│   ├── dbProxy.py
│   ├── enemy.py
│   ├── entity.py
│   ├── entityFactory.py
│   ├── game.py
│   ├── golem.py
│   ├── golemMaior.py
│   ├── guardaFlorestal.py
│   ├── level.py
│   ├── menu.py
│   ├── score.py
│   └── scoreScreen.py
└── asset/
    ├── audio/
    └── images/
   ```

## Como executar o projeto

1. Instale o Python.
2. Instale a biblioteca Pygame:

```bash
pip install pygame
```

3. Abra o projeto no PyCharm.
4. Execute o arquivo 'main.py'.

## Tecnologias utilizadas

* Python
* Pygame
* SQLite3

## Possíveis melhorias futuras

* Permitir que o jogador digite seu nome antes de salvar o score
* Adicionar barra de vida para o guarda florestal
* Criar novas fases
* Adicionar novos inimigos
* Melhorar animações e efeitos sonoros

