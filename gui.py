import copy
import tkinter as tk
from typing import List, Tuple, Dict
from PIL import Image, ImageTk
from tkinter import font as tkfont
from gui_helper import Timer, Misc
from boggle_board_randomizer import randomize_board
DEFAULT_FONT = ('Helvetica', 18)  # tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
BGCOLOR = '#B0C4DE'
TEXTCOLOR = '#002060'
BT_COLOR = 'blue'
BT_SELECTED_COLOR = 'gray'

BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tk.RAISED,
                "bg": BT_COLOR,
                "activebackground": BT_SELECTED_COLOR}

PACK_VARS = {'side': tk.TOP, 'fill': tk.BOTH, 'expand': True}

class GUI:
    _buttons: Dict[str, tk.Button] = {}

    def __init__(self, board: List[List[str]], again, q):
        self.__root = tk.Tk()
        self.__root.title('Boggle by Erel & Fishman')
        self.__root.geometry('1000x600')
        self.__root.resizable(False, False)

        self.__again = again
        self.__q = q

        self.__board = board

        self.__main_window = self.__root

        f = WelcomePage(self.__root, self.on_start, bg=BGCOLOR)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def on_start(self, f):
        f.pack_forget()
        f = GamePage(self.__root, self.__board, self.__again, self.__q, bg=BGCOLOR)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run(self):
        self.__main_window.mainloop()
        

def correct_word(word: str) -> bool:
    import random
    """returns if the word is correct"""
    return random.randint(0, 1) == 1


class GamePage(tk.Frame):
    def __init__(self, root, board, again, q, font=DEFAULT_FONT, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.__again = again
        self.__q = q
        self.__root = root
        self.__found = []
        self.__is_first = True
        self.__timer = Timer()
        self.__selected = []
        root.after(1000, self.tick, self.destroy)
        self.__path_s_var = tk.StringVar()
        self.__path_trace = ''
        self.__current_path = tk.Label(root, textvariable=self.__path_s_var, font=DEFAULT_FONT, bg=BGCOLOR)
        self.__current_path.pack(**PACK_VARS)
        self.update_path_view()
        select = lambda e : self.select(e)
        release = lambda e: self.release(e)
        self.__f = GridPage(root, board, select, release, font, **kwargs)
        self.__f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__s = WordsListPage(root, **kwargs)
        self.__s.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.__timer_s_var = tk.StringVar()
        self.__timer_s_var.set(str(self.__timer))
        timer = tk.Label(root, textvariable=self.__timer_s_var, font=DEFAULT_FONT, bg=BGCOLOR, fg=TEXTCOLOR)
        timer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.__score_s_var = tk.StringVar()
        self.__score_s_var.set('0')
        self.__score = tk.Label(root, textvariable=self.__score_s_var, font=DEFAULT_FONT, bg=BGCOLOR)
        self.__score.pack(**PACK_VARS)

    def destroy(self) -> None:
        self.__again()

    def tick(self, destroy):
        self.__timer.dec()
        if self.__timer.time == 0:
            destroy()
        self.update_timer()
        self.__root.after(1000, self.tick, destroy)
    
    def update_timer(self):
        self.__timer_s_var.set(str(self.__timer))

    def update_path_view(self):
        self.__path_s_var.set(self.__path_trace)

    def select(self, event):
        widget = self.__root.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button):
            coor = widget.extra
            if self.__is_first or (coor not in self.__selected and coor in list(Misc.neighbors_in_board(self.__selected[-1]))):
                widget['bg'] = 'gray'
                self.__path_trace += widget.cget('text')
                self.update_path_view()
                self.__selected.append(coor)
                self.__is_first = False
    
    def add_score(self, how_many_points: int):
        current_score = int(self.__score_s_var.get())
        self.__score_s_var.set(str(current_score + how_many_points))
    
    def release(self, event):
        word = self.__path_trace
        if self.__path_trace:
            if correct_word(word):
                if self.__path_s_var.get() not in self.__found:
                    self.__s.add_word(self.__path_s_var.get())
                    self.__found.append(self.__path_s_var.get())
                    self.add_score(len(self.__path_trace)**2)
                color = 'green'
            else:
                color = 'red'
            self.colorize_buttons(color, all=False, buttons=self.buttons_of_indices(self.__selected))
            self.__root.after(300, self.colorize_buttons, BT_COLOR)
            
            self.__path_trace = ''
            self.update_path_view()
            self.__selected = []
            self.__is_first = True

    def colorize_buttons(self, color, all=True, buttons=[]):
        if all:
            for r in self.__f.buttons:
                for b in r:
                    b.configure(bg=color)
        else:
            for b in buttons:
                b.configure(bg=color)
    
    def buttons_of_indices(self, coors):
        for coor in coors:
            yield self.__f.buttons[coor[1]][coor[0]]

                
        



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
    def __init__(self, root, board, select, release, font=DEFAULT_FONT, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self._root = root
        self.buttons = self.__make_buttons(board)
        root.bind('<B1-Motion>', select)
        root.bind('<ButtonRelease-1>', release)


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
        button.extra = (c, r)
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


class PlayAgainPage(tk.Frame):
    def __init__(self, root, again, q, font=DEFAULT_FONT, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self._root = root

        l = tk.Label(self, text="GG. Do you want to play again?", font=font, bg=BGCOLOR, fg=TEXTCOLOR)
        l.pack(**PACK_VARS)

        yes = tk.Button(self, text='Play Again', font=font, bg='#c6c1b9', fg=TEXTCOLOR, command=again)
        yes.pack(**PACK_VARS)

        no = tk.Button(self, text='Exit', font=font, bg='#c6c1b9', fg=TEXTCOLOR, command=q)
        no.pack(**PACK_VARS)


if __name__ == '__main__':
    while True:
        t = GUI(randomize_board())
        t.run()
