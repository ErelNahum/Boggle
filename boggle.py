from gui import GUI
from boggle_board_randomizer import randomize_board


def new_game(previous=None):
    if previous is not None:
        previous.destroy()
    g = GUI(randomize_board(), new_game)
    g.run()


if __name__ == '__main__':
    new_game()
