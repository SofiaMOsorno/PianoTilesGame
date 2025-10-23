import tkinter as tk
from business_logic.game_logic import GameLogic
import random
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pyaudio
import struct

SOUND_ENGINE = 'pyaudio'

class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Piano Tiles Deluxe")
        self.root.configure(bg="#2c2c2c")
        self.game_logic = GameLogic()
        self.game_data = self.game_logic.get_game_data()
        self.tile_graphics = {}
        
        self.notes = {
            'F4': 349,
            'G4': 392,
            'A4': 440,
            'B4': 494,
            'C5': 523,
            'D5': 587,
            'E5': 659,
            'F5': 698,
            'G5': 784
        }
        
        self.note_list = list(self.notes.values())
        
        self.sound_executor = ThreadPoolExecutor(max_workers=4)
        
        self.sample_rate = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            output=True,
            frames_per_buffer=1024
        )
        
        self.create_ui()
        self.bind_events()
        self.start_game()
    
    def generate_tone(self, frequency, duration=0.15):
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        wave = np.sin(2 * np.pi * frequency * t)
        
        envelope = np.ones(num_samples)
        fade_samples = int(0.01 * self.sample_rate)
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        wave = wave * envelope * 0.3
        return wave.astype(np.float32)
    
    def play_note(self, frequency=None):
        if frequency is None:
            frequency = random.choice(self.note_list)
        
        def play_sound_task():
            try:
                tone = self.generate_tone(frequency)
                self.stream.write(tone.tobytes())
            except Exception as e:
                print(f"Error reproduciendo sonido: {e}")
        
        self.sound_executor.submit(play_sound_task)
    
    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#2c2c2c")
        main_frame.pack(padx=10, pady=10)
        
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
        
        self.canvas = tk.Canvas(
            main_frame,
            width=self.game_data.get_canvas_width(),
            height=self.game_data.get_canvas_height(),
            bg='#34495e',
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.draw_column_lines()
        
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
        
        self.sound_label = tk.Label(
            main_frame,
            text=f"Sonido: {SOUND_ENGINE}",
            font=('Arial', 10),
            bg='#2c2c2c',
            fg='#95a5a6'
        )
        self.sound_label.pack(pady=(5, 0))
    
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
            self.play_note()
            
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
    
    def __del__(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
        except:
            pass