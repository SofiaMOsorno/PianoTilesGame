from data.entities import GameData

class GameRepository:
    def __init__(self):
        self.game_data = GameData()
    
    def get_game_data(self):
        return self.game_data
    
    def reset_game_data(self):
        self.game_data.set_score(0)
        self.game_data.set_speed(5)
        self.game_data.set_spawn_delay(800)
        self.game_data.set_game_over(False)
        self.game_data.clear_tiles()
    
    def save_tile(self, tile):
        self.game_data.add_tile(tile)
    
    def delete_tile(self, tile):
        self.game_data.remove_tile(tile)
    
    def get_all_tiles(self):
        return self.game_data.get_tiles()
    
    def update_score(self, score):
        self.game_data.set_score(score)
    
    def update_speed(self, speed):
        self.game_data.set_speed(speed)
    
    def update_spawn_delay(self, delay):
        self.game_data.set_spawn_delay(delay)
