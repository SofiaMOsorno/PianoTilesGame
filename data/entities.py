class Tile:
    def __init__(self, column, tile_width, tile_height, speed):
        self.column = column
        self.width = tile_width
        self.height = tile_height
        self.speed = speed
        self.clicked = False
        self.x = column * tile_width
        self.y = -tile_height
        
    def get_position(self):
        return self.x, self.y
    
    def get_dimensions(self):
        return self.width, self.height
    
    def is_clicked(self):
        return self.clicked
    
    def set_clicked(self, clicked):
        self.clicked = clicked
    
    def set_speed(self, speed):
        self.speed = speed
    
    def get_speed(self):
        return self.speed
    
    def update_position(self, new_y):
        self.y = new_y


class GameData:
    def __init__(self):
        self.score = 0
        self.speed = 5
        self.spawn_delay = 800
        self.game_over = False
        self.tiles = []
        self.columns = 4
        self.tile_width = 100
        self.tile_height = 150
        self.canvas_width = self.columns * self.tile_width
        self.canvas_height = 600
    
    def get_score(self):
        return self.score
    
    def set_score(self, score):
        self.score = score
    
    def get_speed(self):
        return self.speed
    
    def set_speed(self, speed):
        self.speed = speed
    
    def get_spawn_delay(self):
        return self.spawn_delay
    
    def set_spawn_delay(self, delay):
        self.spawn_delay = delay
    
    def is_game_over(self):
        return self.game_over
    
    def set_game_over(self, game_over):
        self.game_over = game_over
    
    def get_tiles(self):
        return self.tiles
    
    def add_tile(self, tile):
        self.tiles.append(tile)
    
    def remove_tile(self, tile):
        self.tiles.remove(tile)
    
    def clear_tiles(self):
        self.tiles.clear()
    
    def get_columns(self):
        return self.columns
    
    def get_tile_width(self):
        return self.tile_width
    
    def get_tile_height(self):
        return self.tile_height
    
    def get_canvas_width(self):
        return self.canvas_width
    
    def get_canvas_height(self):
        return self.canvas_height
