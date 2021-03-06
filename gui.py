##############################################################################
# FILE: ex12.py
# WRITER: Yuval Fishman, yuvalfishman , 325711398. Erel Nahum, erel, 325177715
# EXERCISE: Intro2cs ex12 2021-2022
# DESCRIPTION: this file is responsible for the GUI of the game.
##############################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
DICT_FILE = "boggle_dict.txt"
import copy
import sys
import tkinter as tk
from typing import List
from PIL import Image, ImageTk
from gui_helper import Timer, Misc

##############################################################################
#                                 Constants                                  #
##############################################################################
DEFAULT_FONT = ('Helvetica', 18)
BGCOLOR = '#B0C4DE'
TEXTCOLOR = '#002060'
BT_COLOR = '#FF9933'
BT_SELECTED_COLOR = 'gray'
BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": BT_COLOR,
                "activebackground": BT_SELECTED_COLOR}

PACK_PARAMS = {'side': tk.TOP, 'fill': tk.BOTH, 'expand': True}


class GUI:
    """the main handler of the gui. create an instance of this class and call the 'run' method."""

    def __init__(self, board: List[List[str]], new_game):
        self.__root = tk.Tk()
        self.__root.title('Boggle by Erel & Fishman')
        self.__root.geometry('1000x600')
        self.__root.resizable(False, False)

        self.__new_game = lambda: new_game(self)
        self.__board = board

        self.__main_window = self.__root

        f = WelcomePage(self.__root, self.on_start, bg=BGCOLOR)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        f.tkraise()

    def on_start(self, f):
        """switches to the main game page frame"""
        f.pack_forget()
        f = GamePage(self.__root, self.__board, self.end, bg=BGCOLOR)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        f.tkraise()

    def end(self, f):
        """switches to the end game titles frame"""
        f.pack_forget()
        f = EndGameFrame(self.__root, self.__new_game, sys.exit)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run(self):
        """call this method to start the game"""
        self.__main_window.mainloop()

    def destroy(self):
        self.__root.destroy()


class WelcomePage(tk.Frame):
    def __init__(self, root, on_start, font=DEFAULT_FONT, **kwargs):
        """on_start: a function that closes this frame and opens the game"""
        tk.Frame.__init__(self, root, **kwargs)
        self._root = root

        img = Image.open('logo.PNG')
        img = img.resize((200, 150))
        logo_img = ImageTk.PhotoImage(image=img)
        li = tk.Label(self, image=logo_img)
        li.image = logo_img
        li.pack()

        hello_label = tk.Label(self, text="Welcome to Boggle!", font=font, bg=BGCOLOR, fg=TEXTCOLOR)
        hello_label.pack(side="top", fill="x", pady=10)

        instructions_label = tk.Label(self, text="You have 3 minutes to find as many words as you can.", font=font,
                                      bg=BGCOLOR, fg=TEXTCOLOR)
        instructions_label.pack(side='top', fill='x', pady=10)

        luck_label = tk.Label(self, text="Good Luck!", font=font, bg=BGCOLOR, fg=TEXTCOLOR)
        luck_label.pack(side='top', fill='x', pady=10)

        start_button = tk.Button(self, text='Start Game', font=font, bg='#c6c1b9', fg=TEXTCOLOR,
                                 command=lambda: on_start(self))
        start_button.pack(side='top', fill='x', pady=10)


class GamePage(tk.Frame):
    """the main game frame. contains a grid frame and a word list frame."""

    def __init__(self, root, board, end_f, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.__root = root
        self.__end_f = end_f

        self.wlp = WordsListPage(root, bg=BGCOLOR)
        self.wlp.pack(side=tk.LEFT)

        self.gp = GridPage(root, board, self.process_word, bg=BGCOLOR)
        self.gp.focus_set()
        self.gp.pack(**PACK_PARAMS)

        self.tl = TimerLabel(root)
        root.after(1000, self.tick)
        self.tl.pack(**PACK_PARAMS)

        self.sl = ScoreLabel(root)
        self.sl.pack(**PACK_PARAMS)

    def tick(self):
        """a method that should be called every second to progress the timer."""
        if self.tl.tick():  # calling the timer 'tick' method, while checking that the game if the game is over.
            self.__root.unbind('<B1-Motion>')
            self.__root.unbind('<ButtonRelease-1>')
            self.__end_f(self)
            return
        self.__root.after(1000, self.tick)

    def process_word(self, word, length_of_route):
        """gets a word and returns if the word is real or not. In the background, it updates the score."""
        if not Misc.correct_word(word):
            return False
        if not self.wlp.already_found(word):
            self.wlp.add_word(word)
            self.sl.add_score(length_of_route ** 2)
        return True


class WordsListPage(tk.Frame):
    """this frame is responsible for saving the correct words."""

    def __init__(self, root, font=DEFAULT_FONT, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.__root = root
        self.__lb = tk.Listbox(self, bg=BGCOLOR, font=('Helvetica', 13))
        self.__next_to_append = 1
        self.__lb.pack(side=tk.LEFT)
        self.__found = []

    def add_word(self, word):
        self.__lb.insert(self.__next_to_append, word)
        self.__found.append(word)
        self.__next_to_append += 1
        self.__lb.pack(side=tk.LEFT)

    def already_found(self, word):
        return word in self.__found


class TracerLabel(tk.Label):
    """this is a special label that can be updated."""

    def __init__(self, root, font=DEFAULT_FONT):
        self.__s_var = tk.StringVar()
        tk.Label.__init__(self, root, textvariable=self.__s_var, font=font)

    def update_word(self, word: str):
        self.__s_var.set(word)


class GridPage(tk.Frame):
    """this frame view the board and the tracer label."""

    def __init__(self, root, board, process_word, font=DEFAULT_FONT, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.__root = root
        self.buttons = self.__make_buttons(board)
        root.bind('<B1-Motion>', self.select)
        root.bind('<ButtonRelease-1>', self.release)

        self.__letters_trace = ''
        self.__selected_coors = []
        self.lab = TracerLabel(root)
        self.lab.pack(**PACK_PARAMS)

        self.__process_word = process_word

    def select(self, event):
        """this method is being called when the curser is drag over"""
        widget = self.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button):
            coor = widget.extra
            is_new_word = len(self.__letters_trace) == 0
            if is_new_word or (
                    coor not in self.__selected_coors and coor in list(
                Misc.neighbors_in_board(self.__selected_coors[-1]))):
                widget['bg'] = 'gray'
                self.__selected_coors.append(coor)
                self.__letters_trace += widget.cget('text')
                self.lab.update_word(self.__letters_trace)

    def release(self, event):
        """this method is being called when the mouse is released."""
        word = self.__letters_trace
        if word:
            correct = self.__process_word(word, len(self.__selected_coors))
            self.try_color('green' if correct else 'red')
        self.__letters_trace = ''
        self.__selected_coors = []
        self.lab.update_word('')

    def __make_buttons(self, board):
        """this method creates the buttons and packs them"""
        for i in range(4):
            tk.Grid.columnconfigure(self, i, weight=1)
        for i in range(4):
            tk.Grid.rowconfigure(self, i, weight=1)

        buttons = copy.deepcopy(board)
        for y in range(len(board)):
            for x in range(len(board[0])):
                buttons[y][x] = self.__make_button(board[y][x], y, x)
        return buttons

    def __make_button(self, name, r, c):
        """this method creates a single button"""
        button = tk.Button(self, text=name, **BUTTON_STYLE)
        button.extra = (c, r)
        button.grid(row=r, column=c, sticky=tk.NSEW, padx=10, pady=10)
        return button

    def colorize_buttons(self, color, buttons=None):
        """this method colorizes all the buttons given to the color given. if no buttons are given, it colorizes all
        buttons """
        if buttons is None:
            for r in self.buttons:
                for b in r:
                    b.configure(bg=color)
        else:
            for b in buttons:
                b.configure(bg=color)

    def buttons_of_indices(self, coors):
        """returns corresponding buttons"""
        for coor in coors:
            yield self.buttons[coor[1]][coor[0]]

    def try_color(self, color):
        self.colorize_buttons(color, buttons=self.buttons_of_indices(self.__selected_coors))
        self.after(300, self.colorize_buttons, BT_COLOR)


class TimerLabel(tk.Label):
    """a special label that shows the time left"""
    def __init__(self, root):
        self.__s_var = tk.StringVar()
        self.__timer = Timer()
        self.__s_var.set(f'Remaining Time: {self.__timer}')
        tk.Label.__init__(self, root, textvariable=self.__s_var, font=DEFAULT_FONT, bg=BGCOLOR, fg=TEXTCOLOR)

    def tick(self):
        self.__timer.dec()
        self.__s_var.set(f'Remaining Time: {self.__timer}')
        return self.__timer.time <= 0


class ScoreLabel(tk.Label):
    """a special label that tracks the score"""
    def __init__(self, root):
        self.__score = 0
        self.__s_var = tk.StringVar()
        self.__s_var.set('Score: 0')
        tk.Label.__init__(self, root, textvariable=self.__s_var, font=DEFAULT_FONT, bg=BGCOLOR, fg=TEXTCOLOR)

    def add_score(self, score):
        self.__score += score
        self.__s_var.set(f'Score: {self.__score}')


class EndGameFrame(tk.Frame):
    """this frame asks the user if he wants to play again or close the game"""
    def __init__(self, root, yes_f, no_f, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.__root = root

        ql = tk.Label(self, text='GG. Do you want to play another game?', font=DEFAULT_FONT, bg=BGCOLOR, fg=TEXTCOLOR)
        ql.pack(**PACK_PARAMS)

        yes = tk.Button(self, text='YES', bg=BT_COLOR, fg=TEXTCOLOR, font=DEFAULT_FONT, command=yes_f)
        yes.pack(**PACK_PARAMS)

        no = tk.Button(self, text='NO', bg=BT_COLOR, fg=TEXTCOLOR, font=DEFAULT_FONT, command=no_f)
        no.pack(**PACK_PARAMS)
