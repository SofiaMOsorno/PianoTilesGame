import random
from models.tile import Tile


class GameController:
    def __init__(self, view):
        self.view = view
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

        self.view.set_click_handler(self.on_click)
        self.view.set_restart_handler(self.restart_game)

        self.start_game()

    def start_game(self):
        """Inicia el juego"""
        self.game_loop()
        self.spawn_tile()

    def spawn_tile(self):
        """Genera una nueva ficha"""
        if self.game_over:
            return

        column = random.randint(0, self.columns - 1)
        tile = Tile(column, self.tile_width, self.tile_height, self.speed)
        self.tiles.append(tile)

        self.view.add_tile(tile)

        self.view.schedule_callback(self.spawn_delay, self.spawn_tile)

    def game_loop(self):
        """Bucle principal del juego"""
        if self.game_over:
            return

        tiles_to_remove = []

        for tile in self.tiles:
            tile.move()

            self.view.update_tile(tile)

            if tile.is_out_of_bounds(self.canvas_height):
                tiles_to_remove.append(tile)
            elif tile.is_missed(self.canvas_height):
                if not tile.clicked:
                    self.end_game()
                    return

        for tile in tiles_to_remove:
            self.view.remove_tile(tile)
            self.tiles.remove(tile)

        self.view.schedule_callback(30, self.game_loop)

    def on_click(self, x, y):
        """Maneja los clicks del usuario"""
        if self.game_over:
            return

        clicked_tile = False

        for tile in self.tiles:
            if not tile.clicked and tile.is_clicked_at(x, y):
                tile.mark_clicked()
                self.view.mark_tile_clicked(tile)
                clicked_tile = True
                self.increase_score()
                break

        if not clicked_tile:
            # Verificar si hay fichas visibles
            visible_tiles = [t for t in self.tiles if t.y >=
                             0 and t.y < self.canvas_height]
            if visible_tiles:
                self.end_game()

    def increase_score(self):
        """Aumenta la puntuación y ajusta la dificultad"""
        self.score += 1
        self.view.update_score(self.score)

        if self.score % 5 == 0 and self.speed < 15:
            self.speed += 1
            self.view.update_speed(self.speed)

            for tile in self.tiles:
                tile.speed = self.speed

        if self.score % 10 == 0 and self.spawn_delay > 400:
            self.spawn_delay -= 50

    def end_game(self):
        """Termina el juego"""
        self.game_over = True
        self.view.show_game_over(self.score)

    def restart_game(self):
        """Reinicia el juego"""
        for tile in self.tiles:
            self.view.remove_tile(tile)
        self.tiles.clear()

        self.score = 0
        self.speed = 5
        self.spawn_delay = 800
        self.game_over = False

        self.view.reset_game()
        self.view.update_score(self.score)
        self.view.update_speed(self.speed)

        self.start_game()


Game = GameController
