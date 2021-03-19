# japanese_garden
Solver for board game I had a pleasure to play - "Brains Japanese Garden".
Written in Python - fast development was my priority there. 

Some cool features of a game were discovered during implementation - for example number of combinations is not that huge as might looks like at the beginning.

Naiive algorithm is not that naiive - modeling the board, and encoding states took me some time to figure.

Digging in the Net shows some interesting algorithms to be used to solve it (Knuth's Dancing Links maybe?).

## Before
![It's ugly, but works](https://github.com/szymek156/japanese_garden/blob/master/tiles/board.png)

## After some magic:
![It's ugly, but works](https://github.com/szymek156/japanese_garden/blob/master/tiles/board_and_solution.png)

# TODO:
- pep, pylint
- transpile
- refactor
- add tests
- more levels
- improve getNextState function
- use heuristics, dynamic programming
- use constrain programming (mini zinc?)
- use logger
- https://en.wikipedia.org/wiki/Dancing_Links
# Heuristics:
- iterate over entrances and find pieces which are must-have (for example, pagoda, yin-yang)
- try to satisfy one constrain, freeze tiles, try to satisfy another, if fails, go back and repeat
