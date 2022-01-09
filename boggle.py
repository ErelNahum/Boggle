import sys

from gui import GUI
from boggle_board_randomizer import randomize_board

def play_again():
    my_game = GUI(randomize_board())
    my_game.run()


if __name__ == '__main__':
    my_game = GUI(randomize_board(), play_again, sys.exit)
    my_game.run()
