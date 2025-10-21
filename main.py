import tkinter as tk
from game import Game

def main():
    root = tk.Tk()
    root.title("Piano Tiles")
    root.resizable(False, False)
    
    game = Game(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()#main.py
