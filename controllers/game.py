import tkinter as tk
from tkinter import messagebox
import random
from models import tile

class Game:
    def __init__(self, root):
        self.root = root
        
        self.columns = 4
        self.tile_width = 100
        self.tile_height = 150
        self.canvas_width = self.columns * self.tile_width
        self.canvas_height = 600
        
        self.score = 0
        self.speed = 5
        self.spawn_delay = 800
        self.game_over = False
        self.tiles = []
        
        self.create_ui()
        
        self.canvas.bind('<Button-1>', self.on_click)
        
        self.game_loop()
        self.spawn_tile()
    
    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#450845")
        main_frame.pack(padx=10, pady=10)
        
        info_frame = tk.Frame(main_frame, bg='#34495e', height=60)
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.score_label = tk.Label(
            info_frame,
            text=f"Puntos: {self.score}",
            font=('Arial', 20, 'bold'),
            bg='#34495e',
            fg='white'
        )
        self.score_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.speed_label = tk.Label(
            info_frame,
            text=f"Velocidad: {self.speed}",
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
            highlightthickness=0
        )
        self.canvas.pack()
        
        for i in range(1, self.columns):
            x = i * self.tile_width
            self.canvas.create_line(
                x, 0, x, self.canvas_height,
                fill='#95a5a6',
                width=2
            )
        
        self.restart_button = tk.Button(
            main_frame,
            text="Reiniciar",
            command=self.restart_game,
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=5,
            cursor='hand2'
        )
        self.restart_button.pack(pady=(5, 0))
    
    def spawn_tile(self):
        if self.game_over:
            return
        
        column = random.randint(0, self.columns - 1)
        
        tile = Tile(
            self.canvas,
            column,
            self.tile_width,
            self.tile_height,
            self.speed
        )
        
        self.tiles.append(tile)
        
        self.root.after(self.spawn_delay, self.spawn_tile)
    
    def game_loop(self):
        if self.game_over:
            return
        
        tiles_to_remove = []
        
        for tile in self.tiles:
            tile.move()
            
            if tile.is_out_of_bounds(self.canvas_height):
                tiles_to_remove.append(tile)
            
            elif tile.is_missed(self.canvas_height):
                if not tile.clicked:
                    self.end_game()
                    return
        
        for tile in tiles_to_remove:
            tile.delete()
            self.tiles.remove(tile)
        
        self.root.after(30, self.game_loop)
    
    def on_click(self, event):
        if self.game_over:
            return
        
        x, y = event.x, event.y
        clicked_tile = False
        
        for tile in self.tiles:
            if not tile.clicked and tile.is_clicked_at(x, y):
                tile.mark_clicked()
                clicked_tile = True
                self.increase_score()
                break
        
        if not clicked_tile:
            visible_tiles = [t for t in self.tiles if t.y >= 0 and t.y < self.canvas_height]
            if visible_tiles:
                self.end_game()
    
    def increase_score(self):
        self.score += 1
        self.score_label.config(text=f"Puntos: {self.score}")
        
        if self.score % 5 == 0 and self.speed < 15:
            self.speed += 1
            self.speed_label.config(text=f"Velocidad: {self.speed}")
            
            for tile in self.tiles:
                tile.speed = self.speed
        
        if self.score % 10 == 0 and self.spawn_delay > 400:
            self.spawn_delay -= 50
    
    def end_game(self):
        self.game_over = True
        
        self.canvas.create_rectangle(
            0, self.canvas_height // 2 - 80,
            self.canvas_width, self.canvas_height // 2 + 80,
            fill="#ff1900",
            outline='white',
            width=3
        )
        
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2 - 30,
            text="¡GAME OVER!",
            font=('Arial', 36, 'bold'),
            fill='white'
        )
        
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2 + 20,
            text=f"Puntuación Final: {self.score}",
            font=('Arial', 20),
            fill='white'
        )
    
    def restart_game(self):
        for tile in self.tiles:
            tile.delete()
        self.tiles.clear()
        
        self.score = 0
        self.speed = 5
        self.spawn_delay = 800
        self.game_over = False
        
        self.score_label.config(text=f"Puntos: {self.score}")
        self.speed_label.config(text=f"Velocidad: {self.speed}")
        
        self.canvas.delete('all')
        
        for i in range(1, self.columns):
            x = i * self.tile_width
            self.canvas.create_line(
                x, 0, x, self.canvas_height,
                fill="#ffffff",
                width=2
            )
        
        self.game_loop()
        self.spawn_tile()