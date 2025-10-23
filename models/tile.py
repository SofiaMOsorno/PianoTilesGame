# tile.py (Capa de Entidades)

class Tile:
    def __init__(self, column, tile_width, tile_height, speed):
        self.column = column
        self.width = tile_width
        self.height = tile_height
        self.speed = speed
        self.clicked = False

        self.x = column * tile_width
        self.y = -tile_height

    def move(self):
        """Actualiza la posición lógica de la ficha."""
        self.y += self.speed

    def is_clicked_at(self, x_click, y_click):
        """Verifica si las coordenadas lógicas del click están dentro de la ficha."""
        return (self.x <= x_click <= self.x + self.width and
                self.y <= y_click <= self.y + self.height)

    def mark_clicked(self):
        """Marca el estado lógico como clickeado."""
        self.clicked = True

    def is_out_of_bounds(self, canvas_height):
        """Verifica si la ficha ha pasado completamente la zona de juego."""
        return self.y > canvas_height

    def is_missed(self, canvas_height):
        """Verifica si la ficha fue fallada (llegó al final sin ser clickeada)."""
        return not self.clicked and self.y + self.height > canvas_height
