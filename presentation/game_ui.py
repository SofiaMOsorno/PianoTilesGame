import tkinter as tk
from business_logic.game_logic import GameLogic

class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Piano Tiles Deluxe")
        self.root.configure(bg="#1e1e1e")
        self.game_logic = GameLogic()
        self.game_data = self.game_logic.get_game_data()
        self.tile_graphics = {}

        self.create_ui()
        self.bind_events()

    def create_ui(self):
        # Canvas principal
        self.canvas = tk.Canvas(
            self.root,
            width=self.game_data.get_canvas_width(),
            height=self.game_data.get_canvas_height(),
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack()

        self.draw_gradient_background()
        self.draw_column_lines()

        # Texto superior (número central de puntuación)
        self.score_text = self.canvas.create_text(
            self.game_data.get_canvas_width() // 2,
            25,
            text=str(self.game_data.get_score()),
            font=("Arial", 28, "bold"),
            fill="#7b3ffb"
        )

        # Frame inferior con info
        info_frame = tk.Frame(self.root, bg="#1e1e1e")
        info_frame.pack(pady=(5, 10))

        # Etiquetas de puntuación y velocidad
        self.score_label = tk.Label(
            info_frame,
            text=f"Puntos: {self.game_data.get_score()}",
            font=('Arial', 22, 'bold'),
            bg='#1c1c1c',
            fg='#f1c40f'
        )
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.speed_label = tk.Label(
            info_frame,
            text=f"Velocidad: {self.game_data.get_speed()}",
            font=('Arial', 18, 'bold'),
            bg='#1c1c1c',
            fg='#1abc9c'
        )
        self.speed_label.pack(side=tk.RIGHT, padx=20)

        # Botón de inicio redondo
        self.start_button = tk.Button(
            self.root,
            text="START",
            font=("Arial", 16, "bold"),
            bg="#4a90e2",
            fg="white",
            activebackground="#357ABD",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.start_game,
            cursor="hand2"
        )
        self.start_button.pack(pady=5)

        # Botón de reinicio (rojo)
        self.restart_button = tk.Button(
            main_frame,
            text="Reiniciar",
            command=self.restart_game,
            font=('Arial', 14, 'bold'),
            bg='#e74c3c',
            fg='black',
            activebackground='#c0392b',
            activeforeground='white',
            padx=25,
            pady=8,
            command=self.restart_game,
            cursor="hand2"
        )
        self.restart_button.pack(pady=(0, 10))

    def draw_gradient_background(self):
        """Dibuja el degradado vertical azul → violeta."""
        width = self.game_data.get_canvas_width()
        height = self.game_data.get_canvas_height()
        r1, g1, b1 = (52, 152, 219)   # Azul claro
        r2, g2, b2 = (155, 89, 182)   # Violeta
        steps = height
        for i in range(steps):
            r = int(r1 + (r2 - r1) * (i / steps))
            g = int(g1 + (g2 - g1) * (i / steps))
            b = int(b1 + (b2 - b1) * (i / steps))
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

    def draw_column_lines(self):
        for i in range(1, self.game_data.get_columns()):
            x = i * self.game_data.get_tile_width()
            self.canvas.create_line(
                x, 0, x, self.game_data.get_canvas_height(),
                fill="#d0d0d0",
                width=1
            )

    def bind_events(self):
        self.canvas.bind('<Button-1>', self.on_click)

    def start_game(self):
        self.start_button.pack_forget()
        self.spawn_tile()
        self.game_loop()

    def spawn_tile(self):
        if self.game_data.is_game_over():
            return

        tile = self.game_logic.create_new_tile()
        self.create_tile_graphic(tile)
        self.root.after(self.game_data.get_spawn_delay(), self.spawn_tile)

    def create_tile_graphic(self, tile):
        rect_id = self.canvas.create_rectangle(
            tile.x, tile.y,
            tile.x + tile.width, tile.y + tile.height,
            fill="black",
            outline=""
        )
        self.tile_graphics[tile] = rect_id

    def game_loop(self):
        if self.game_data.is_game_over():
            return

        game_continues, tiles_to_remove = self.game_logic.move_tiles()
        if not game_continues:
            self.end_game()
            return

        for tile in self.game_data.get_tiles():
            self.update_tile_graphic(tile)

        for tile in tiles_to_remove:
            self.delete_tile_graphic(tile)

        self.game_logic.remove_tiles(tiles_to_remove)
        self.root.after(30, self.game_loop)

    def update_tile_graphic(self, tile):
        if tile in self.tile_graphics:
            rect_id = self.tile_graphics[tile]
            self.canvas.coords(
                rect_id,
                tile.x, tile.y,
                tile.x + tile.width, tile.y + tile.height
            )

    def delete_tile_graphic(self, tile):
        if tile in self.tile_graphics:
            rect_id = self.tile_graphics[tile]
            self.canvas.delete(rect_id)
            del self.tile_graphics[tile]

    def on_click(self, event):
        if self.game_data.is_game_over():
            return

        x, y = event.x, event.y
        clicked_tile = self.game_logic.check_click(x, y)
        if clicked_tile:
            self.mark_tile_clicked(clicked_tile)
            self.game_logic.increase_score()
            self.update_score_display()
            self.update_speed_display()
        else:
            if self.game_logic.has_visible_tiles():
                self.end_game()

    def mark_tile_clicked(self, tile):
        if tile in self.tile_graphics:
            rect_id = self.tile_graphics[tile]
            self.canvas.itemconfig(rect_id, fill="#2ecc71")

    def update_score_display(self):
        self.canvas.itemconfig(self.score_text, text=str(self.game_data.get_score()))
        self.score_label.config(text=f"Puntos: {self.game_data.get_score()}")

    def update_speed_display(self):
        self.speed_label.config(text=f"Velocidad: {self.game_data.get_speed()}")

    def end_game(self):
        self.game_logic.end_game()
        self.show_game_over()

    def show_game_over(self):
        self.canvas.create_text(
            self.game_data.get_canvas_width() // 2,
            self.game_data.get_canvas_height() // 2 - 40,
            text="¡GAME OVER!",
            font=('Arial', 36, 'bold'),
            fill='white'
        )
        
        self.canvas.create_text(
            self.game_data.get_canvas_width() // 2,
            self.game_data.get_canvas_height() // 2 + 30,
            text=f"Puntuación Final: {self.game_data.get_score()}",
            font=('Arial', 22, 'bold'),
            fill='white'
        )
    
    def restart_game(self):
        for tile in list(self.tile_graphics.keys()):
            self.delete_tile_graphic(tile)

        self.game_logic.reset_game()
        self.update_score_display()
        self.update_speed_display()

        self.canvas.delete("all")
        self.tile_graphics.clear()
        self.draw_gradient_background()
        self.draw_column_lines()
        
        self.start_game()
