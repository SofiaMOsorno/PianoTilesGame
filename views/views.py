import tkinter as tk
from tkinter import messagebox


class GameView:
    def __init__(self, root):
        self.root = root
        self.click_handler = None
        self.restart_handler = None

        self.columns = 4
        self.tile_width = 100
        self.tile_height = 150
        self.canvas_width = self.columns * self.tile_width
        self.canvas_height = 600

        self.tile_graphics = {}

        self.create_ui()

    def create_ui(self):
        """Crea la interfaz de usuario"""

        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(padx=10, pady=10)

        info_frame = tk.Frame(main_frame, bg='#34495e', height=60)
        info_frame.pack(fill=tk.X, pady=(0, 5))
        info_frame.pack_propagate(False)

        self.score_label = tk.Label(
            info_frame,
            text="Puntos: 0",
            font=('Arial', 20, 'bold'),
            bg='#34495e',
            fg='white'
        )
        self.score_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.speed_label = tk.Label(
            info_frame,
            text="Velocidad: 5",
            font=('Arial', 16),
            bg='#34495e',
            fg='#3498db'
        )
        self.speed_label.pack(side=tk.RIGHT, padx=20, pady=10)

        self.canvas = tk.Canvas(
            main_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='#ecf0f1',
            highlightthickness=2,
            highlightbackground='#34495e'
        )
        self.canvas.pack()

        self.draw_column_lines()

        self.restart_button = tk.Button(
            main_frame,
            text="Reiniciar",
            command=self._on_restart_click,
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=8,
            cursor='hand2',
            relief='flat',
            borderwidth=0
        )
        self.restart_button.pack(pady=(10, 0))

        self.canvas.bind('<Button-1>', self._on_canvas_click)

        self.root.configure(bg='#2c3e50')

    def draw_column_lines(self):
        """Dibuja las líneas divisorias entre columnas"""
        for i in range(1, self.columns):
            x = i * self.tile_width
            self.canvas.create_line(
                x, 0, x, self.canvas_height,
                fill='#95a5a6',
                width=2,
                tags='grid'
            )

    def set_click_handler(self, handler):
        """Establece el manejador de clicks"""
        self.click_handler = handler

    def set_restart_handler(self, handler):
        """Establece el manejador de reinicio"""
        self.restart_handler = handler

    def _on_canvas_click(self, event):
        """Manejador interno de clicks en el canvas"""
        if self.click_handler:
            self.click_handler(event.x, event.y)

    def _on_restart_click(self):
        """Manejador interno del botón de reinicio"""
        if self.restart_handler:
            self.restart_handler()

    def add_tile(self, tile):
        """Añade una ficha visual al canvas"""
        tile_id = self.canvas.create_rectangle(
            tile.x, tile.y,
            tile.x + tile.width, tile.y + tile.height,
            fill='#2c3e50',
            outline='#34495e',
            width=2,
            tags='tile'
        )

        self.tile_graphics[tile] = tile_id

    def update_tile(self, tile):
        """Actualiza la posición visual de una ficha"""
        if tile in self.tile_graphics:
            tile_id = self.tile_graphics[tile]
            self.canvas.coords(
                tile_id,
                tile.x, tile.y,
                tile.x + tile.width, tile.y + tile.height
            )

    def mark_tile_clicked(self, tile):
        """Marca visualmente una ficha como clickeada"""
        if tile in self.tile_graphics:
            tile_id = self.tile_graphics[tile]
            self.canvas.itemconfig(tile_id, fill='#27ae60', outline='#2ecc71')

    def remove_tile(self, tile):
        """Remueve una ficha del canvas"""
        if tile in self.tile_graphics:
            tile_id = self.tile_graphics[tile]
            self.canvas.delete(tile_id)
            del self.tile_graphics[tile]

    def update_score(self, score):
        """Actualiza el display del puntaje"""
        self.score_label.config(text=f"Puntos: {score}")

    def update_speed(self, speed):
        """Actualiza el display de la velocidad"""
        self.speed_label.config(text=f"Velocidad: {speed}")

    def show_game_over(self, final_score):
        """Muestra la pantalla de game over"""
        overlay = self.canvas.create_rectangle(
            0, 0, self.canvas_width, self.canvas_height,
            fill='#2c3e50', stipple='gray50',
            tags='game_over'
        )

        msg_bg = self.canvas.create_rectangle(
            50, self.canvas_height // 2 - 100,
            self.canvas_width - 50, self.canvas_height // 2 + 100,
            fill='#e74c3c',
            outline='white',
            width=3,
            tags='game_over'
        )

        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2 - 40,
            text="¡GAME OVER!",
            font=('Arial', 28, 'bold'),
            fill='white',
            tags='game_over'
        )

        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2 + 10,
            text=f"Puntuación Final: {final_score}",
            font=('Arial', 16, 'bold'),
            fill='white',
            tags='game_over'
        )

        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2 + 50,
            text="Presiona 'Reiniciar' para jugar de nuevo",
            font=('Arial', 12),
            fill='#ecf0f1',
            tags='game_over'
        )

    def reset_game(self):
        """Resetea la vista del juego"""
        self.canvas.delete('all')
        self.tile_graphics.clear()
        self.draw_column_lines()

    def schedule_callback(self, delay, callback):
        """Programa un callback para ejecutar después de un delay"""
        self.root.after(delay, callback)


class PianoTilesView(GameView): ...