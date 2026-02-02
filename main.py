import arcade
import random

TILE_SIZE = 32

LEVEL_MAP = [
    "########################",
    "#..........##..........#",
    "#.####.###.##.###.####.#",
    "#P....................G#",
    " ######################",
]

class Character(arcade.Sprite):
    def __init__(self, speed, x, y, color):
        super().__init__()
        radius = TILE_SIZE // 2 - 1
        texture = arcade.make_circle_texture(radius * 2, color)
        self.texture = texture
        self.width = texture.width - 9
        self.height = texture.height - 9
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
        radius = TILE_SIZE // 2 - random.randint(3, 5) # better look
        texture = arcade.make_circle_texture(radius * 2, color)
        self.texture = texture
        self.width = texture.width - 10
        self.height = texture.height - 10
        self.center_x = x
        self.center_y = y

class Ghost(arcade.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        radius = TILE_SIZE // 2 - 1
        texture = arcade.make_circle_texture(radius * 2, color)
        self.texture = texture
        self.width = texture.width - 9
        self.height = texture.height - 9
        self.center_x = x
        self.center_y = y

class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()

        self.drawinings()
    
    def create_wall(self, x, y, color):
        wall = Wall(x, y, color)
        self.wall_list.append(wall)
    
    def create_coin(self, x, y, color):
        coin = Coin(x, y, color)
        self.coin_list.append(coin)
    
    def create_ghost(self, x, y, color):
        ghost = Ghost(x, y, color)
        self.ghost_list.append(ghost)
    
    def create_character(self, speed, x, y, color):
        character = Character(speed, x, y, color)
        self.player_list.append(character)
    
    def drawinings(self):
        self.player = Character(2, 400, 300, arcade.color.ORANGE)
        self.player_list.append(self.player)

        for thing in LEVEL_MAP:
            for i, the_thing in enumerate(thing):
                x = (i * TILE_SIZE+TILE_SIZE)
                y = ((len(LEVEL_MAP)-LEVEL_MAP.index(thing)-1) * TILE_SIZE+TILE_SIZE)
                if the_thing == "#":
                    self.create_wall(x, y, arcade.color.BLUE)
                elif the_thing == ".":
                    self.create_coin(x, y, arcade.color.GOLD)
                elif the_thing == "P":
                    self.player.center_x = x
                    self.player.center_y = y
                elif the_thing == "G":
                    self.create_ghost(x, y, arcade.color.RED)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.drawinings()
    
    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()


window = arcade.Window(800, 600, "Pacman Game")
game = PacmanGame()
game.setup()
window.show_view(game)
arcade.run()