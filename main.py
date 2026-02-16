import arcade, random, json, time
from levels import levels
from sprites import *

with open('game_data.json', 'r') as file:
    game_data = json.load(file)

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
        self.player = None
        self.mover = self.player
        self.ghost_charms = 0
        self.bot_timer = 0.0
        self.ghost_mode_left = 0.0

        self.drawinings()
    
    def create_wall(self, x, y, color):
        wall = Wall(x, y, color)
        self.wall_list.append(wall)
    
    def create_coin(self, x, y, color):
        coin = Coin(x, y, color, self.ghost_charms)
        if coin.ghost_charm: self.ghost_charms += 1
        self.coin_list.append(coin)
    
    def create_ghost(self, x, y, color, speed=game_data["Ghost"]["DEFAULT_GHOST_SPEED"]):
        ghost = Ghost(x, y, color, speed)
        self.ghost_list.append(ghost)
    
    def drawinings(self):
        self.player = Character(game_data["Player"]["DEFAULT_PLAYER_SPEED"], 400, 300)
        self.player_list.append(self.player)

        self.mover = self.player

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
                    self.create_ghost(x, y, arcade.color.RED, 2)
        self.ghost_charms = 0

    def setup(self):
        self.ghost_timer = 0.0
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
        if self.ghost_mode_left > 0:
            arcade.draw_text(f"Time left being ghost: {round(self.ghost_mode_left)}s", 260, 250, arcade.color.WHITE, 20)
    
    def on_update(self, delta_time):
        self.player_list.update()
        self.ghost_list.update()
        self.check_collisions()
        self.win_game()
        self.ghost_movement()
        self.player_bot_movement(delta_time)

        if self.ghost_mode_left > 0:
            self.ghost_mode_left -= delta_time
            if self.ghost_mode_left <= 0:
                self.ghost_mode_left = 0.0
                self.health -= 1
                if self.health == 0:
                    self.level = 1
                    self.score = 0
                    self.health = 3
                self.setup()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.mover.change_y = self.mover.speed
            self.mover.change_x = 0
            if self.mover == self.player:
                self.mover.angle = -90
        elif key == arcade.key.DOWN:
            self.mover.change_y = -self.mover.speed
            self.mover.change_x = 0
            if self.mover == self.player:
                self.mover.angle = 90
        elif key == arcade.key.LEFT:
            self.mover.change_x = -self.mover.speed
            self.mover.change_y = 0
            if self.mover == self.player:
                self.mover.angle = 180
        elif key == arcade.key.RIGHT:
            self.mover.change_x = self.mover.speed
            self.mover.change_y = 0
            if self.mover == self.player:
                self.mover.angle = 0
    
    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.mover.change_x = 0
        elif key in (arcade.key.UP, arcade.key.DOWN):
            self.mover.change_y = 0
    
    def check_collisions(self):
        if self.mover != self.player:
            walls_in = arcade.check_for_collision_with_list(self.player, self.wall_list)
            if walls_in:
                self.player.center_x -= self.player.change_x
                self.player.center_y -= self.player.change_y
                self.bot_timer = 0.0
        walls_in = arcade.check_for_collision_with_list(self.mover, self.wall_list)
        if walls_in:
            self.mover.center_x -= self.mover.change_x
            self.mover.center_y -= self.mover.change_y

        coins_in = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_in:
            coin.remove_from_sprite_lists()
            if self.mover == self.player:
                self.score += 1
            if coin.ghost_charm: # ghost charm
                self.score += 4
                self.mover = self.ghost_list[0]
                self.ghost_list[0].is_player = True
                self.player.change_x = 0
                self.player.change_y = 0
                self.mover.change_x = 0
                self.mover.change_y = 0
                self.ghost_mode_left = 10.0
        
        ghosts_in = arcade.check_for_collision_with_list(self.player, self.ghost_list)
        if ghosts_in and self.mover == self.player:
            self.health -= 1
            if self.health == 0:
                self.level = 1
                self.score = 0
                self.health = 3
            self.setup()

    def ghost_movement(self):
        for ghost in self.ghost_list:
            if ghost.is_player: continue
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
        
    def player_bot_movement(self, delta_time):
        if self.mover != self.player:

            self.bot_timer -= delta_time
            if self.bot_timer > 0:
                return

            self.bot_timer = 2.5

            directions = ["up", "down", "left", "right"]
            direction = random.choice(directions)
            if direction == "up":
                self.player.change_y = self.mover.speed
                self.player.change_x = 0
                self.player.angle = -90
            elif direction == "down":
                self.player.change_y = -self.mover.speed
                self.player.change_x = 0
                self.player.angle = 90
            elif direction == "left":
                self.player.change_x = -self.mover.speed
                self.player.change_y = 0
                self.player.angle = 180
            elif direction == "right":
                self.player.change_x = self.mover.speed
                self.player.change_y = 0
                self.player.angle = 0
    
    def win_game(self):
        normal_coins = []
        for coin in self.coin_list:
            if not coin.ghost_charm:
                normal_coins.append(coin)
        if len(normal_coins) == 0 and self.mover == self.player:
            self.level += 1
            self.setup()
        else:
            if len(normal_coins) == 0:
                self.ghost_mode_left = 0.0
                self.health -= 1
                if self.health == 0:
                    self.level = 1
                    self.score = 0
                    self.health = 3
                self.setup()
            players_in = arcade.check_for_collision_with_list(self.mover, self.player_list)
            if players_in:
                for player in players_in:
                    if self.mover != player:
                        self.score += 25
                        self.level += 1
                        self.ghost_mode_left = 0.0
                        self.setup()
                        break

def main():
    window = arcade.Window(game_data["General"]["SCREEN_WIDTH"], game_data["General"]["SCREEN_HEIGHT"], game_data["General"]["SCREEN_TITLE"])
    game = PacmanGame()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()