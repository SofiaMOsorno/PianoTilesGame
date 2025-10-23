import tkinter as tk
from presentation.game_ui import GameUI

def main():
    root = tk.Tk()
    root.title("Piano Tiles")
    root.resizable(False, False)
    
    game_ui = GameUI(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()#main.py
