import arcade
import random

TILE_SIZE = 32

class Character(arcade.Sprite):
    def __init__(self, speed, x, y, color):
        super().__init__()
        radius = TILE_SIZE // 2 - 6
        self.texture = arcade.load_texture("pacman.png")
        self.scale = (radius * 2) / self.texture.width
        self.speed = speed
        self.center_x = x
        self.center_y = y

class Wall(arcade.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        texture = arcade.make_soft_square_texture(TILE_SIZE, color)
        self.texture = texture
        self.width = texture.width
        self.height = texture.height
        self.center_x = x
        self.center_y = y

class Coin(arcade.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        radius = TILE_SIZE // 2 - random.randint(4, 6) # randiomize size slightly
        texture = arcade.make_circle_texture(radius * 2, color)
        self.texture = texture
        self.width = texture.width - 10
        self.height = texture.height - 10
        self.center_x = x
        self.center_y = y

class Ghost(arcade.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        radius = TILE_SIZE // 2 - 6
        self.texture = arcade.load_texture("ghost.png")
        self.scale = (radius * 2) / self.texture.width
        self.center_x = x
        self.center_y = y
        self.last_direction = None