# Planes-Battleship-AI(Avioane)

A console-based, human-vs-computer variant of Battleship, built for the **Object-Oriented Programming** course. Instead of ships, each player hides 3 planes on a 10×10 grid; instead of sinking a hull, you have to find and strike each plane's **head** to bring it down. The computer opponent uses a heuristic targeting strategy (no minimax, since Battleship-style games are imperfect-information — see [AI Strategy](#computer-ai-strategy)).

## How to play

1. **Placement phase** — you place 3 planes on your own board, one at a time, by giving the head's coordinates (row letter A–J, column number 1–10) and a facing direction (`UP`, `DOWN`, `LEFT`, `RIGHT`).
2. The computer randomly places its own 3 planes.
3. **Attack phase** — you and the computer alternate turns calling out coordinates on each other's board, trying to down all 3 opposing planes first.

### Plane shape

Each plane occupies 8 cells: a head, a row of 3 "wing" cells, a single body cell, and a row of 3 "tail" cells. Oriented `UP`, it looks like this (relative to the head):

```
   .  ^  .     <- head
   x  x  x     <- wings
   .  x  .     <- body
   x  x  x     <- tail
```

The head is drawn as `^`, `v`, `<`, or `>` depending on the direction it's facing; every other plane cell is drawn as `x`.

### The key rule: only the head counts as a kill

Shooting a wing/body/tail cell (`x`) registers as a **hit**, but the plane survives. A plane is only **downed** when its **head** cell is struck — so both players are really hunting for the head, using wing/body hits as clues to where it might be.

## Architecture

The project is split into layers, following the course's layered-architecture requirement:

```
UI layer        UI.py            console I/O, input validation, turn loop
                    │
Logic layer     Game.py          plane geometry, placement rules, hit/down/AI logic
                    │
Data layer      Board.py         the 10x10 grid itself
                    │
Entry point     Play.py          wires the layers together and starts the game

Tests.py                          unit tests for Board and Game (non-UI) layers
```

## Project structure

```
.
├── Board.py    # Board, PlayerBoard, ComputerBoard — the grid and cell access
├── Game.py     # PlaneBuilder / BuildPlayerBoard / BuildComputerBoard — placement & validation
│               # GameLogic — shot resolution (hit / down / empty)
│               # PlaneAI(GameLogic) — computer targeting strategy
├── UI.py       # PlacementUI — console flow for placing planes
│               # GuessCoordsUI — console flow for the attack phase
├── Play.py     # Entry point: builds boards, boards' builders, and starts the game
├── Tests.py    # PyUnit tests for Board, BuildPlayerBoard, GameLogic, PlaneAI
└── README.md
```

**Class relationships:**
- `PlayerBoard` / `ComputerBoard` both extend `Board`.
- `BuildPlayerBoard` / `BuildComputerBoard` both extend `PlaneBuilder`, sharing the plane-shape math (`get_plane_coordinates`) and placement validation (`is_valid`).
- `PlaneAI` extends `GameLogic`, adding the targeting strategy on top of shared shot-resolution logic.

## Computer AI strategy

Since Battleship-type games hide information from both players, minimax doesn't directly apply. `PlaneAI` instead picks its next move by working through a priority list, from most to least certain:

1. **Forced head** — if the computer is down to the opponent's last plane and there's exactly one coordinate consistent with all hits/misses so far that could be its head, fire there to try to end the game immediately.
2. **Best destroy** — otherwise, if any board position is a plausible head location for *some* remaining plane (consistent with current hits and misses), target it.
3. **Adjacent targeting** — if there are unresolved wing/body hits, fire at a random cell orthogonally adjacent to one of them, since the head must be nearby.
4. **Hunt** — with no leads at all, fire at an unshot cell from a checkerboard (parity) pattern first, which covers the board more efficiently than a fully random search, falling back to any remaining cell.

## Running the game

Requires Python 3 (standard library only — no external dependencies).

```
python Play.py
```

Follow the on-screen prompts: place your 3 planes, then trade shots with the computer until one side loses all 3 planes.

## Running the tests

```
python -m unittest Tests.py
```

Covers `Board` (grid setup, cell access, string rendering), `BuildPlayerBoard` (plane geometry and placement validation), `GameLogic` (hit/down/empty resolution), and `PlaneAI` (result tracking, hunt, and head-inference logic). The UI layer is intentionally left untested, per the assignment's requirements.

## Notes

- Only a console UI is implemented; there's no graphical interface.
- The computer's placement and hunting both use `random`, so no two games play out the same way.
- `Board.set_cell(row, column)` writes to `_board[column][row]` — transposed relative to `get_cell(row, column)`. Nothing in `Game.py` calls `set_cell` (plane placement writes to `_board` directly), so this doesn't affect actual gameplay, but it's worth knowing about if you extend the code.

## About

Built as an OOP course assignment: a layered human-vs-computer board game with a rule-based AI opponent, backed by unit tests for all non-UI logic.
