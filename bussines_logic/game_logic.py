import random
from data.entities import Tile
from data.repository import GameRepository

class GameLogic:
    def __init__(self):
        self.repository = GameRepository()
        self.game_data = self.repository.get_game_data()
    
    def create_new_tile(self):
        column = random.randint(0, self.game_data.get_columns() - 1)
        tile = Tile(
            column,
            self.game_data.get_tile_width(),
            self.game_data.get_tile_height(),
            self.game_data.get_speed()
        )
        self.repository.save_tile(tile)
        return tile
    
    def move_tiles(self):
        tiles_to_remove = []
        
        for tile in self.repository.get_all_tiles():
            new_y = tile.y + tile.get_speed()
            tile.update_position(new_y)
            
            if self.is_tile_out_of_bounds(tile):
                tiles_to_remove.append(tile)
            elif self.is_tile_missed(tile):
                if not tile.is_clicked():
                    return False, tiles_to_remove
        
        return True, tiles_to_remove
    
    def is_tile_out_of_bounds(self, tile):
        return tile.y > self.game_data.get_canvas_height()
    
    def is_tile_missed(self, tile):
        return (not tile.is_clicked() and 
                tile.y + tile.height > self.game_data.get_canvas_height())
    
    def remove_tiles(self, tiles_to_remove):
        for tile in tiles_to_remove:
            self.repository.delete_tile(tile)
    
    def check_click(self, x, y):
        for tile in self.repository.get_all_tiles():
            if not tile.is_clicked():
                if self.is_click_inside_tile(tile, x, y):
                    tile.set_clicked(True)
                    return tile
        return None
    
    def is_click_inside_tile(self, tile, x, y):
        return (tile.x <= x <= tile.x + tile.width and
                tile.y <= y <= tile.y + tile.height)
    
    def has_visible_tiles(self):
        for tile in self.repository.get_all_tiles():
            if tile.y >= 0 and tile.y < self.game_data.get_canvas_height():
                return True
        return False
    
    def increase_score(self):
        new_score = self.game_data.get_score() + 1
        self.repository.update_score(new_score)
        
        if new_score % 5 == 0 and self.game_data.get_speed() < 15:
            new_speed = self.game_data.get_speed() + 1
            self.repository.update_speed(new_speed)
            
            for tile in self.repository.get_all_tiles():
                tile.set_speed(new_speed)
        
        if new_score % 10 == 0 and self.game_data.get_spawn_delay() > 400:
            new_delay = self.game_data.get_spawn_delay() - 50
            self.repository.update_spawn_delay(new_delay)
    
    def end_game(self):
        self.game_data.set_game_over(True)
    
    def reset_game(self):
        self.repository.reset_game_data()
    
    def get_game_data(self):
        return self.game_data