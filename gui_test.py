import time
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from gui_helper import Timer

BGCOLOR = '#B0C4DE'
TEXTCOLOR = '#002060'

class BoggleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        """the constructor. Initializes properties."""
        tk.Tk.__init__(self, *args, **kwargs)
        self.bgcolor = BGCOLOR

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('700x400')

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WelcomePage, MainGamePage): # put all pages!
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background=BGCOLOR)


        img = Image.open('logo.PNG')
        img = img.resize((200,150))
        logo_img = ImageTk.PhotoImage(image=img)

        li = tk.Label(self, image=logo_img)
        li.image = logo_img
        li.pack()

        hello_label = tk.Label(self, text="Welcome to Boggle!", font=controller.title_font, bg=BGCOLOR, fg=TEXTCOLOR)
        hello_label.pack(side="top", fill="x", pady=10)

        instructions_label = tk.Label(self, text="You have 3 minutes to find as many words as you can.", font=controller.title_font, bg=BGCOLOR, fg=TEXTCOLOR)
        instructions_label.pack(side='top', fill='x', pady=10)

        luck_label = tk.Label(self, text="Good Luck!",
                                      font=controller.title_font, bg=BGCOLOR, fg=TEXTCOLOR)
        luck_label.pack(side='top', fill='x', pady=10)


        start_button = tk.Button(self, text='Start Game', font=controller.title_font, bg='#c6c1b9', fg=TEXTCOLOR, command=lambda: controller.show_frame('MainGamePage'))
        start_button.pack(side='top', fill='x', pady=10)


class MainGamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background=BGCOLOR)

        self.timer = Timer()
        self.timer_l = tk.Label(self, text=f'Remaining Time: {self.timer}', font=controller.title_font, bg=BGCOLOR, fg=TEXTCOLOR)
        self.timer_l.pack(side='top', fill='x', pady=10)

        self.update_timer()

    def update_timer(self):
        print(self.timer)
        self.timer.dec()
        print(self.timer)

        self.timer_l.text = 'Remaining Time: ' + str(self.timer)
        self.timer_l.pack(side='top', fill='x', pady=10)
        #self.after(1000, self.update_timer())


if __name__ == "__main__":
    app = BoggleApp()
    app.mainloop()
