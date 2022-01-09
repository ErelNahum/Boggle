from gui import GUI
from boggle_board_randomizer import randomize_board
if __name__ == '__main__':
    my_game = GUI(randomize_board())
    my_game.run()