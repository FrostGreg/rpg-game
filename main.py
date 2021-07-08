from classes.interface import Interface
from classes.game import Game

valid = False
game_modes = [1, 2]
mode_select = 0

while not valid:
    try:
        # int() already strips whitespace
        mode_select = int(input("Select a mode in which you would like to play?:\n1: Text-based\n2: Graphical\n"))
    except ValueError as e:
        print("Invalid input Try Again")
        continue

    if mode_select in game_modes:
        valid = True
    else:
        print("Invalid game mode Try Again")

game = Game()

if mode_select == 1:
    game.run()

elif mode_select == 2:
    gui = Interface(game)
    gui.run()
