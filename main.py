import arcade
import random
from levels import levels
from sprites import *

class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.level = 1
        self.score = 0
        self.health = 3

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
        self.player = Character(3, 400, 300, arcade.color.ORANGE)
        self.player_list.append(self.player)

        for row_idx, row in enumerate(levels[f"level{self.level}"]):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (len(levels[f"level{self.level}"]) - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2
                if cell == "#":
                    self.create_wall(x, y, arcade.color.BLUE)
                elif cell == ".":
                    self.create_coin(x, y, arcade.color.GOLD)
                elif cell == "P":
                    self.player.center_x = x
                    self.player.center_y = y
                elif cell == "G":
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
        arcade.draw_text(f"Level: {self.level}", 10, 580, arcade.color.WHITE, 14)
        arcade.draw_text(f"Score: {self.score}", 10, 560, arcade.color.WHITE, 14)
        arcade.draw_text(f"Health: {self.health}/3", 10, 540, arcade.color.WHITE, 14)
    
    def on_update(self, delta_time):
        self.player_list.update()
        self.ghost_list.update()
        self.check_collisions()
        self.win_game()
        self.ghost_movement()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = self.player.speed
            self.player.change_x = 0
            self.player.angle = -90
        elif key == arcade.key.DOWN:
            self.player.change_y = -self.player.speed
            self.player.change_x = 0
            self.player.angle = 90
        elif key == arcade.key.LEFT:
            self.player.change_x = -self.player.speed
            self.player.change_y = 0
            self.player.angle = 180
        elif key == arcade.key.RIGHT:
            self.player.change_x = self.player.speed
            self.player.change_y = 0
            self.player.angle = 0
    
    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0
        elif key in (arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0
    
    def check_collisions(self):
        walls_in = arcade.check_for_collision_with_list(self.player, self.wall_list)
        if walls_in:
            self.player.center_x -= self.player.change_x
            self.player.center_y -= self.player.change_y

        coins_in = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_in:
            coin.remove_from_sprite_lists()
            self.score += 1
        
        ghosts_in = arcade.check_for_collision_with_list(self.player, self.ghost_list)
        if ghosts_in:
            self.health -= 1
            if self.health == 0:
                self.level = 1
                self.score = 0
                self.health = 3
            self.setup()

    def ghost_movement(self):
        for ghost in self.ghost_list:
            directions = ["up", "down", "left", "right"]
            if ghost.change_x == 0 and ghost.change_y == 0:
                directions_now = directions.copy()
                if ghost.last_direction:
                    directions_now.remove(ghost.last_direction)
                direction = random.choice(directions_now)
                ghost.last_direction = direction
                if direction == "up":
                    ghost.change_y = 1.85
                elif direction == "down":
                    ghost.change_y = -1.85
                elif direction == "left":
                    ghost.change_x = -1.85
                elif direction == "right":
                    ghost.change_x = 1.85
            
            walls_in = arcade.check_for_collision_with_list(ghost, self.wall_list)
            if walls_in:
                ghost.center_x -= ghost.change_x
                ghost.center_y -= ghost.change_y
                ghost.change_x = 0
                ghost.change_y = 0

    def win_game(self):
        if len(self.coin_list) == 0:
            self.level += 1
            self.setup()

def main():
    window = arcade.Window(850, 600, "Pacman Game")
    game = PacmanGame()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()