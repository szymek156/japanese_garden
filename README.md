# japanese_garden
## Before
![It's ugly, but works](https://github.com/szymek156/japanese_garden/blob/master/tiles/board.png)

## After some magic:
![It's ugly, but works](https://github.com/szymek156/japanese_garden/blob/master/tiles/board_and_solution.png)

# TODO:
- pep, pylint
- transpile
- refactor
- add tests
- better algorithms
- more levels
- improve getNextState function
- make searching randomized, just for fun
- use heuristics, dynamic programming
- use constrain programming (mini zinc?)
- use logger

# Heuristics:
- iterate over entrances and find pieces which are must-have (for example, pagoda, yin-yang)
- try to satisfy one constrain, freeze tiles, try to satisfy another, if fails, go back and repeat