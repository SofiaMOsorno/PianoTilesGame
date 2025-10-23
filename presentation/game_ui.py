import tkinter as tk
from business_logic.game_logic import GameLogic

class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Piano Tiles Deluxe")
        self.root.configure(bg="#2c2c2c")
        self.game_logic = GameLogic()
        self.game_data = self.game_logic.get_game_data()
        self.tile_graphics = {}
        
        self.create_ui()
        self.bind_events()
        self.start_game()
    
    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#2c2c2c")
        main_frame.pack(padx=10, pady=10)
        
        # Info Frame con estilo moderno
        info_frame = tk.Frame(main_frame, bg='#1c1c1c', height=60, bd=2, relief='ridge')
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.score_label = tk.Label(
            info_frame,
            text=f"Puntos: {self.game_data.get_score()}",
            font=('Arial', 22, 'bold'),
            bg='#1c1c1c',
            fg='#f1c40f'
        )
        self.score_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.speed_label = tk.Label(
            info_frame,
            text=f"Velocidad: {self.game_data.get_speed()}",
            font=('Arial', 18, 'bold'),
            bg='#1c1c1c',
            fg='#1abc9c'
        )
        self.speed_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Canvas con degradado simulado
        self.canvas = tk.Canvas(
            main_frame,
            width=self.game_data.get_canvas_width(),
            height=self.game_data.get_canvas_height(),
            bg='#34495e',
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.draw_column_lines()
        
        # Botón con estilo moderno y animación de hover
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
            bd=3,
            relief='raised',
            cursor='hand2'
        )
        self.restart_button.pack(pady=(10, 0))
    
    def draw_column_lines(self):
        for i in range(1, self.game_data.get_columns()):
            x = i * self.game_data.get_tile_width()
            self.canvas.create_line(
                x, 0, x, self.game_data.get_canvas_height(),
                fill='#7f8c8d',
                width=3
            )
    
    def bind_events(self):
        self.canvas.bind('<Button-1>', self.on_click)
    
    def start_game(self):
        self.game_loop()
        self.spawn_tile()
    
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
            fill='#8e44ad',
            outline='#2980b9',
            width=2
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
            self.canvas.itemconfig(rect_id, fill='#2ecc71')
    
    def update_score_display(self):
        self.score_label.config(text=f"Puntos: {self.game_data.get_score()}")
    
    def update_speed_display(self):
        self.speed_label.config(text=f"Velocidad: {self.game_data.get_speed()}")
    
    def end_game(self):
        self.game_logic.end_game()
        self.show_game_over()
    
    def show_game_over(self):
        self.canvas.create_rectangle(
            0, self.game_data.get_canvas_height() // 2 - 90,
            self.game_data.get_canvas_width(), self.game_data.get_canvas_height() // 2 + 90,
            fill="#e74c3c",
            outline='white',
            width=4
        )
        
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
        
        self.canvas.delete('all')
        self.tile_graphics.clear()
        self.draw_column_lines()
        
        self.start_game()
