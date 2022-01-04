import copy
import tkinter as tk
from typing import List, Tuple, Dict
from PIL import Image, ImageTk
from tkinter import font as tkfont
from gui_helper import Timer
from boggle_board_randomizer import randomize_board
DEFAULT_FONT = ('Helvetica', 18)  # tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
BGCOLOR = '#B0C4DE'
TEXTCOLOR = '#002060'
BT_COLOR = 'blue'
BT_SELECTED_COLOR = 'red'

BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": BT_COLOR,
                "activebackground": BT_SELECTED_COLOR}

PACK_VARS = {'side': tk.TOP, 'fill': tk.BOTH, 'expand': True}

class GUI:
    _buttons: Dict[str, tk.Button] = {}

    def __init__(self, board: List[List[str]]):
        self.__root = tk.Tk()
        self.__root.title('Boggle by Erel & Fishman')
        self.__root.geometry('1000x600')
        self.__root.resizable(False, False)

        self.__board = board

        self.__main_window = self.__root

        f = WelcomePage(self.__root, self.on_start, bg=BGCOLOR)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def on_start(self, f):
        f.pack_forget()
        f = GamePage(self.__root, self.__board, bg=BGCOLOR)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run(self):
        self.__main_window.mainloop()


class GamePage(tk.Frame):
    def __init__(self, root, board, font=DEFAULT_FONT, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.__root = root
        self.__timer = Timer()
        self.__path_s_var = tk.StringVar()
        self.__current_path = tk.Label(root, textvariable=self.__path_s_var, font=DEFAULT_FONT, bg=BGCOLOR)
        self.__current_path.pack(**PACK_VARS)
        self.update_path_view('hee')
        select = lambda e : self.select(e)
        f = GridPage(root, board, select, font, **kwargs)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        s = WordsListPage(root, **kwargs)
        s.add_word('hello')
        s.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.__timer_s_var = tk.StringVar()
        self.__timer_s_var.set(str(self.__timer))
        timer = tk.Label(root, textvariable=self.__timer_s_var, font=DEFAULT_FONT, bg=BGCOLOR, fg=TEXTCOLOR)
        timer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        submit = tk.Button(root, text='SUBMIT', font=DEFAULT_FONT)
        submit.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_path_view(self, word):
        self.__path_s_var.set(word)

    def select(self, event):
        widget = self.__root.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button):
            widget['bg'] = 'green'


class WordsListPage(tk.Frame):
    def __init__(self, root, font=DEFAULT_FONT, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.__root = root
        self.__lb = tk.Listbox(root, bg=BGCOLOR, font=('Helvetica', 13))
        self.__next_to_append = 1
        self.__lb.pack(side=tk.LEFT)

    def add_word(self, word):
        self.__lb.insert(self.__next_to_append, word)
        self.__next_to_append += 1
        self.__lb.pack(side=tk.LEFT)



class GridPage(tk.Frame):
    def __init__(self, root, board, select, font=DEFAULT_FONT, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self._root = root
        self.__buttons = self.__make_buttons(board)
        root.bind('<B1-Motion>', select)


    def __make_buttons(self, board):
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
        button = tk.Button(self, text=name, **BUTTON_STYLE)
        button.grid(row=r, column=c, sticky=tk.NSEW, padx=10, pady=10)
        return button


class WelcomePage(tk.Frame):
    def __init__(self, root, on_start, font=DEFAULT_FONT, **kwargs):
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


if __name__ == '__main__':
    t = GUI(randomize_board())
    t.run()
