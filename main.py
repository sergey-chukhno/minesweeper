import customtkinter as ctk
from game.minesweeper import Minesweeper

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = Minesweeper()
    app.mainloop() 