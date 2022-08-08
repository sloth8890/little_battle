# Little Battle
## Introduction
A turn-based strategy (TBS) game that has the following [features](#rule).

```little_battle.py``` is a main file where contain whole code to implement the game features.

```file_loading_tests.py``` is a test driver for the function ```load_config_file(filepath)```. In other words, ```load_config_file(filepath)``` needs to be called in each test, and then complete the tests to check if the function can raise the expected errors with the expected messages for different kinds of invalid files.


## Rule
- The game is initialized with a map with resources and two players (Player 1 and Player 2).
- Each player has a home base. Player 1 and Player 2’s home bases should always be in positions (1,1) and (map_width-2, map_height-2), respectively. (coordinates start from (0, 0))
- The winning condition is to capture the other player’s home base by an army.
- There are two stages including “Recruit Armies” and “Move Armies” in a player’s turn.
- In stage “Recruit Armies”, each player can recruit armies and only place the newly recruited armies
next to their home base (4 positions surrounding the home base).
- Recruiting armies costs resources.
- There are three types of resources on the map: wood (W), food(F), gold(G).
- Each player initially has 2W, 2F and 2G.
- There are four types of soldiers: Spearman (S) costs 1W, 1F; Archer (A) costs 1W, 1G; Knight (K)
costs 1F, 1G, Scout (T) costs 1W, 1F, 1G.

- Spearman (S) counters Knight (K); Knight (K) counters Archer (A); Archer (A) counters Spearman.
(S); All other types of armies counter Scout (T); The table below shows the outcome of a fight:

||Spearman (S) | Knight (K) | Archer (A) | Scout (T) |
|---|---|---|---|---|
|Spearman (S)|Both disappear |K disappear | S disappear |T disappear |
|Knight (K)| K disappear |Both disappear |A disappear |T disappear|
|Archer (A) |S disappear |A disappear |Both disappear |T disappear|
|Scout (T) |T disappear |T disappear |T disappear |Both disappear|

- In stage “Move Armies”, each Spearman (S), Archer (A), and Knight (K) can move one step in
each turn while Scout (T) can move up to two steps (one step or two steps in the same direction)
but move only once.
- Each player can command an army to collect resources.

## Commands

1. Read configure file to start game.
    ```
    python3 little_battle.py <filepath>
    ```
2. User can enter ```QUIT```, ```DIS```, or ```PRIS``` any time to quit the game, display the map, or print the prices except aftering winning.
3. User can enter ```S```, ```A```, ```K```, or ```T``` to specify which troop wants to be moved followed by typing ```x``` and ```y``` coordinate.

## Example Game Play
[Winning Example](examples/Winning.txt)

[Terminating Game Example](examples/Terminating.txt)

[Recruiting Army Example](examples/Recruiting.txt)

## Reference
Assignment2 for 2021 INFO11110
