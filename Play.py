from Game import *
from UI import PlacementUI, GuessCoordsUI
from Board import *

if __name__ == "__main__":

    player_board = PlayerBoard()
    my_builder = BuildPlayerBoard(player_board)
    ui = PlacementUI(player_board, my_builder)
    ui.run()

    computer_board = ComputerBoard()
    builder = BuildComputerBoard(computer_board)
    builder.place_planes()

    print(computer_board)

    player_logic = GameLogic(computer_board)
    computer_logic = GameLogic(player_board)

    ai_agent = PlaneAI(player_board)

    game_ui = GuessCoordsUI(computer_board, player_board, player_logic, computer_logic, ai_agent)
    game_ui.run_logic()
