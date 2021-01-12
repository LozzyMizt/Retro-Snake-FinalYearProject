import tkinter as tk
from tkinter import *


class Menu(tk.Canvas):
    # Setting up the Menu border
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)
        self.create_objects()
        self.create_buttons()

    # Creating "Retro Snake" as title introduction
    def create_objects(self):
        self.create_text(
            300, 50, text=f"Retro", tag="retro", fill="#fff", font=("Retro", 90)
        )
        self.create_text(
            300, 130, text=f"Snake", tag="rsnake", fill="#fff", font=("Retro", 90)
        )

    # Creating buttons to Play yourself or let the computer play
    def create_buttons(self):
        playButton = Button(self, text="Play Game!", fg="black", font=("Retro", 25))
        playButton.place(x=100, y=300)

        aiButton = Button(self, text="   AI!   ", fg="black", font=("Retro", 25))
        aiButton.place(x=400, y=300)


root = tk.Tk()
root.title("Retro Snake")
root.resizable(False, False)


board = Menu()
board.pack()


root.mainloop()
