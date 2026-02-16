import arcade, random, json

with open('game_data.json', 'r') as file:
    game_data = json.load(file)

TILE_SIZE = game_data["General"]["TILE_SIZE"]

class Character(arcade.Sprite):
    def __init__(self, speed, x, y):
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
    def __init__(self, x, y, color, ghost_charms):
        super().__init__()
        self.ghost_charm = random.randint(1, 100) <= 1 and ghost_charms <= 0 # chance for coin to be a ghost charm
        radius = TILE_SIZE // 2 - random.randint(4, 6) if not self.ghost_charm else TILE_SIZE // 2
        texture = arcade.make_circle_texture(radius * 2, color) if not self.ghost_charm else arcade.make_circle_texture(radius * 2, arcade.color.PURPLE)
        self.texture = texture
        self.width = texture.width - 10
        self.height = texture.height - 10
        self.center_x = x
        self.center_y = y

class Ghost(arcade.Sprite):
    def __init__(self, x, y, color, speed):
        super().__init__()
        radius = TILE_SIZE // 2 - 6
        self.texture = arcade.load_texture("ghost.png")
        self.scale = (radius * 2) / self.texture.width
        self.speed = speed
        self.center_x = x
        self.center_y = y
        self.last_direction = None
        self.is_player = False