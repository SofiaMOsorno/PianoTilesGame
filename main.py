import tkinter as tk
from controllers.game import GameController
from views.views import GameView


def main():
    root = tk.Tk()
    root.title("Piano Tiles Game")
    root.resizable(False, False)

    root.update_idletasks()
    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()
    pos_x = (root.winfo_screenwidth() // 2) - (width // 2)
    pos_y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{pos_x}+{pos_y}")

    view = GameView(root)

    controller = GameController(view)

    root.mainloop()


if __name__ == "__main__":
    main()
