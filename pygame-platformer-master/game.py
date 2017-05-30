#!/usr/bin/env python3


#LE LAVA GIVES LIVES??


import json
import pygame
import sys

pygame.mixer.pre_init()
pygame.init()

# Window settings
TITLE = "CraftMiner"
WIDTH = 1152
HEIGHT = 640
FPS = 60
GRID_SIZE = 64

# Options
sound_on = True

# Controls
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
JUMP = pygame.K_SPACE

# Levels
levels = ["levels/world-1.json",
          "levels/world-2.json",
          "levels/world-3.json"]

# Colors
TRANSPARENT = (0, 0, 0, 0)
DARK_BLUE = (16, 86, 103)
WHITE = (255, 255, 255)

# Fonts
FONT_SM = pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", 32)
FONT_MD = pygame.font.Font("assets/fonts/MINECRAFT PE.ttf", 64)
FONT_LG = pygame.font.Font("assets/fonts/MINECRAFT PE.ttf", 72)

# Helper functions
def load_image(file_path, width=GRID_SIZE, height=GRID_SIZE):
    img = pygame.image.load(file_path)
    img = pygame.transform.scale(img, (width, height))

    return img

def play_sound(sound, loops=0, maxtime=0, fade_ms=0):
    if sound_on:
        if maxtime == 0:
            sound.play(loops, maxtime, fade_ms)
        else:
            sound.play(loops, maxtime, fade_ms)

def play_music():
    if sound_on:
        pygame.mixer.music.play(-1)

# Images
splash = load_image("assets/backgrounds/splash.jpg", WIDTH, HEIGHT)

hero_walk1 = load_image("assets/character/adventurer_walk1.png")
hero_walk2 = load_image("assets/character/adventurer_walk2.png")
hero_jump = load_image("assets/character/adventurer_jump.png")
hero_idle = load_image("assets/character/adventurer_idle.png")
hero_images = {"run": [hero_walk1, hero_walk2],
               "jump": hero_jump,
               "idle": hero_idle}

block_images = {"GR": load_image("assets/tiles/grass.png"),
                "DR": load_image("assets/tiles/dirt.png"),
                "WD": load_image("assets/tiles/wood.png"),
                "LE": load_image("assets/tiles/leaves.png"),
                "W": load_image("assets/tiles/oak.png"),
                "ST": load_image("assets/tiles/stone.png")}

b_rectangle = load_image("assets/fonts/rectangle.png")

lava_img = load_image("assets/tiles/lava.png")

backwood_img = load_image("assets/tiles/backwood.png")
backstone_img = load_image("assets/tiles/backstone.png")

hearts_img = load_image("assets/items/heart.png")
black_heart_img = load_image("assets/items/black_heart.png")
lives_img = load_image("assets/items/lives.png")

fakecoin_img = load_image("assets/coins/gold_fake.png")

coin_img0 = load_image("assets/coins/gold_0.png")
coin_img1 = load_image("assets/coins/gold_1.png")
coin_img2 = load_image("assets/coins/gold_2.png")
coin_img3 = load_image("assets/coins/gold_3.png")
coin_img4 = load_image("assets/coins/gold_4.png")
coin_img5 = load_image("assets/coins/gold_5.png")
coin_img6 = load_image("assets/coins/gold_6.png")
coin_img7 = load_image("assets/coins/gold_7.png")
coin_img8 = load_image("assets/coins/gold_8.png")
coin_img9 = load_image("assets/coins/gold_9.png")
coin_animate = [coin_img0, coin_img1, coin_img2, coin_img3, coin_img4, coin_img5, coin_img6, coin_img7, coin_img8, coin_img9]

gem_img0 = load_image("assets/coins/gem_0.png")
gem_img1 = load_image("assets/coins/gem_1.png")
gem_img2 = load_image("assets/coins/gem_2.png")
gem_img3 = load_image("assets/coins/gem_3.png")
gem_img4 = load_image("assets/coins/gem_4.png")
gem_img5 = load_image("assets/coins/gem_5.png")
gem_img6 = load_image("assets/coins/gem_6.png")
gem_img7 = load_image("assets/coins/gem_7.png")
gem_img8 = load_image("assets/coins/gem_8.png")
gem_img9 = load_image("assets/coins/gem_9.png")
gem_animate = [gem_img0, gem_img1, gem_img2, gem_img3, gem_img4, gem_img5, gem_img6, gem_img7, gem_img8, gem_img9]

heart_img = load_image("assets/powerups/bandaid.png")
oneup_img = load_image("assets/powerups/first_aid.png")
flesh_img = load_image("assets/powerups/flesh.png")

fake_img = load_image("assets/tiles/oak.png")

invinc_img0 = load_image("assets/powerups/invinc_0.png")
invinc_img1 = load_image("assets/powerups/invinc_1.png")
invinc_img2 = load_image("assets/powerups/invinc_2.png")
invinc_animate = [invinc_img0, invinc_img1, invinc_img2]

flag_img = load_image("assets/items/flag.png")
flagpole_img = load_image("assets/items/flagpole.png")

no_fall_enemy_images = {"SP": load_image("assets/enemies/spider-1.png"),
                        "SF": load_image("assets/enemies/silverfish-1.png")}
                        
fall_enemy_images = {"CR": load_image("assets/enemies/creeper-1.png"),
                     "ZM": load_image("assets/enemies/zombie-1.png")}


# Sounds
JUMP_SOUND = pygame.mixer.Sound("assets/sounds/jump.wav")
COIN_SOUND = pygame.mixer.Sound("assets/sounds/pickup_coin.wav")
POWERUP_SOUND = pygame.mixer.Sound("assets/sounds/powerup.wav")
HURT_SOUND = pygame.mixer.Sound("assets/sounds/hurt.wav")
DIE_SOUND = pygame.mixer.Sound("assets/sounds/death.wav")
LEVELUP_SOUND = pygame.mixer.Sound("assets/sounds/level_up.wav")
GAMEOVER_SOUND = pygame.mixer.Sound("assets/sounds/game_over.wav")
VICTORY_SOUND = pygame.mixer.Sound("assets/sounds/victory.wav")

class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vy = 0
        self.vx = 0

    def apply_gravity(self, level):
        self.vy += level.gravity
        self.vy = min(self.vy, level.terminal_velocity)

    def is_near(self, hero):
        return abs(self.rect.x - hero.rect.x) < 2 * WIDTH

class Block(Entity):

    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Character(Entity):

    def __init__(self, images):
        super().__init__(0, 0, images['idle'])

        self.image_idle = images['idle']
        self.images_run_right = images['run']
        self.images_run_left = [pygame.transform.flip(img, 1, 0) for img in self.images_run_right]
        self.image_jump_right = images['jump']
        self.image_jump_left = pygame.transform.flip(self.image_jump_right, 1, 0)

        self.running_images = self.images_run_right
        self.image_index = 0
        self.steps = 0

        self.speed = 5
        self.jump_power = 20

        self.vx = 0
        self.vy = 0
        self.facing_right = True
        self.on_ground = True

        self.score = 0
        self.lives = 1
        self.hearts = 1
        self.max_hearts = 3
        self.invincibility = 0

    def move_left(self):
        self.vx = -self.speed
        self.facing_right = False

    def move_right(self):
        self.vx = self.speed
        self.facing_right = True

    def stop(self):
        self.vx = 0

    def jump(self, blocks):
        self.rect.y += 1

        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        if len(hit_list) > 0:
            self.vy = -1 * self.jump_power
            play_sound(JUMP_SOUND)

        self.rect.y -= 1

    def check_world_boundaries(self, level):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > level.width:
            self.rect.right = level.width
        elif self.rect.top > level.height:
            self.respawn(level)

    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.vx = 0
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.vx = 0

        self.on_ground = False
        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
                self.on_ground = True
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

    def process_coins(self, coins):
        hit_list = pygame.sprite.spritecollide(self, coins, True)

        for coin in hit_list:
            play_sound(COIN_SOUND)
            self.score += coin.value
	
    def process_gems(self, gems):
        hit_list = pygame.sprite.spritecollide(self, gems, True)

        for gem in hit_list:
            play_sound(COIN_SOUND)
            self.score += gem.value

    def process_enemies(self, enemies):
        hit_list = pygame.sprite.spritecollide(self, enemies, False)

        if len(hit_list) > 0 and self.invincibility == 0:
            play_sound(HURT_SOUND)
            self.hearts -= 1
            self.invincibility = int(0.75 * FPS)

    def process_powerups(self, powerups):
        hit_list = pygame.sprite.spritecollide(self, powerups, True)

        for p in hit_list:
            play_sound(POWERUP_SOUND)
            p.apply(self)
            self.score += p.value

    def check_flag(self, level):
        hit_list = pygame.sprite.spritecollide(self, level.flag, False)

        if len(hit_list) > 0:
            level.completed = True
            play_sound(LEVELUP_SOUND)

    def set_image(self):
        if self.on_ground:
            if self.vx != 0:
                if self.facing_right:
                    self.running_images = self.images_run_right
                else:
                    self.running_images = self.images_run_left

                self.steps = (self.steps + 1) % self.speed # Works well with 2 images, try lower number if more frames are in animation

                if self.steps == 0:
                    self.image_index = (self.image_index + 1) % len(self.running_images)
                    self.image = self.running_images[self.image_index]
            else:
                self.image = self.image_idle
        else:
            if self.facing_right:
                self.image = self.image_jump_right
            else:
                self.image = self.image_jump_left

    def die(self, level):
        self.lives -= 1
        self.rect.x = level.start_x
        self.rect.y = level.start_y

        if self.lives > 0:
            play_sound(DIE_SOUND)
            self.hearts = self.max_hearts
        else:
            play_sound(GAMEOVER_SOUND)

    def respawn(self, level):
        self.rect.x = level.start_x
        self.rect.y = level.start_y
        self.invincibility = 0
        self.hearts = self.hearts


    def update(self, level):
        self.process_coins(level.coins)
        self.process_gems(level.gems)
        self.process_powerups(level.powerups)
        self.process_enemies(level.enemies)
        self.apply_gravity(level)
        self.move_and_process_blocks(level.blocks)
        self.check_world_boundaries(level)
        self.set_image()

        if self.hearts > 0:
            self.process_coins(level.coins)
            self.process_gems(level.gems)
            self.process_powerups(level.powerups)
            self.check_flag(level)

            if self.invincibility > 0:
                self.invincibility -= 1
        else:
            self.die(level)

class Coin(Entity):
    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])

        self.images = images
        self.image_index = 0
        self.steps = 0
        self.value = 100


    def set_image(self):
        if self.steps == 0:
            self.image = self.images[self.image_index]
            self.image_index = (self.image_index + 1) % len(self.images)

        self.steps = (self.steps + 1) % 5

    def update(self, hero):
        if self.is_near(hero):
            self.set_image()


class Gem(Entity):
    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])

        self.images = images
        self.image_index = 0
        self.steps = 0
        self.value = 500


    def set_image(self):
        if self.steps == 0:
            self.image = self.images[self.image_index]
            self.image_index = (self.image_index + 1) % len(self.images)

        self.steps = (self.steps + 1) % 5

    def update(self, hero):
        if self.is_near(hero):
            self.set_image()

class Invincibility(Entity):
    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])

        self.images = images
        self.image_index = 0
        self.steps = 0
        self.value = 200

    def apply(self, character):
        character.invincibility = int(12 * FPS)


    def set_image(self):
        if self.steps == 0:
            self.image = self.images[self.image_index]
            self.image_index = (self.image_index + 1) % len(self.images)

        self.steps = (self.steps + 1) % 10

    def update(self, hero):
        if self.is_near(hero):
            self.set_image()

class Enemy(Entity):
    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])

        self.images_left = images
        self.images_right = [pygame.transform.flip(img, 1, 0) for img in images]
        self.current_images = self.images_left
        self.image_index = 0
        self.steps = 0

    def reverse(self):
        self.vx *= -1

        if self.vx < 0:
            self.current_images = self.images_left
        else:
            self.current_images = self.images_right

        self.image = self.current_images[self.image_index]

    def check_world_boundaries(self, level):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > level.width:
            self.rect.right = level.width
            self.reverse()
        elif self.rect.top > level.height:
            self.kill()

    def move_and_process_blocks(self):
        pass

    def set_images(self):
        if self.steps == 0:
            self.image = self.current_images[self.image_index]
            self.image_index = (self.image_index + 1) % len(self.current_images)

        self.steps = (self.steps + 1) % 20 # Nothing significant about 20. It just seems to work okay.


    def update(self, level, hero):
        if self.is_near(hero):
            self.apply_gravity(level)
            self.move_and_process_blocks(level.blocks)
            self.check_world_boundaries(level)
            self.set_images()

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vx = self.start_vx
        self.vy = self.start_vy
        self.image = self.images_left[0]
        self.steps = 0

class Fall_enemy(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.start_x = x
        self.start_y = y
        self.start_vx = -3
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

class No_fall_enemy(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.start_x = x
        self.start_y = y
        self.start_vx = -4
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

    def move_and_process_blocks(self, blocks):
        reverse = False

        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        reverse = True

        for block in hit_list:
            if self.vy >= 0:
                self.rect.bottom = block.rect.top
                self.vy = 0

                if self.vx > 0 and self.rect.right <= block.rect.right:
                    reverse = False

                elif self.vx < 0 and self.rect.left >= block.rect.left:
                    reverse = False

            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

        if reverse:
            self.reverse()

class OneUp(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 0

    def apply(self, character):
        character.lives += 1

class Lava(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Heart(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 0

    def apply(self, character):
        if character.hearts < character.max_hearts:
            character.hearts += 1
        else:
            character.hearts +=0

class Fake(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 0
        
    def apply(self, character):
        character.lives -= 0
            
class Flesh(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 500

    def apply(self, character):
        character.max_hearts -=1
        if character.hearts > 2:
            character.hearts = 2
        else:
            character.hearts +=0

class Flag(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Backwood(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Backstone(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Fakecoin(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = -50

    def apply(self, character):
        character.lives -= 0

class Level():

    def __init__(self, file_path):
        self.starting_blocks = []
        self.starting_enemies = []
        self.starting_coins = []
        self.starting_gems = []
        self.starting_powerups = []
        self.starting_flag = []
        self.starting_lava = []
        self.starting_flesh = []
        self.starting_fake = []
        self.starting_backwood = []
        self.starting_backstone = []

        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.gems = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.flag = pygame.sprite.Group()
        self.lava = pygame.sprite.Group()
        self.flesh = pygame.sprite.Group()
        self.fake = pygame.sprite.Group()
        self.backwood = pygame.sprite.Group()
        self.backstone = pygame.sprite.Group()

        self.active_sprites = pygame.sprite.Group()
        self.inactive_sprites = pygame.sprite.Group()

        with open(file_path, 'r') as f:
            data = f.read()

        map_data = json.loads(data)

        self.width = map_data['width'] * GRID_SIZE
        self.height = map_data['height'] * GRID_SIZE

        self.start_x = map_data['start'][0] * GRID_SIZE
        self.start_y = map_data['start'][1] * GRID_SIZE

        for item in map_data['blocks']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            img = block_images[item[2]]
            self.starting_blocks.append(Block(x, y, img))

        for item in map_data['lava']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_lava.append(Lava(x, y, lava_img))

        for item in map_data['backwood']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_backwood.append(Backwood(x, y, backwood_img))

        for item in map_data['backstone']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_backstone.append(Backstone(x, y, backstone_img))
            
        for item in map_data['fall_enemies']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            img = fall_enemy_images[item[2]]
            self.starting_enemies.append(Fall_enemy(x, y, [img]))

        for item in map_data['no_fall_enemies']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            img = no_fall_enemy_images[item[2]]
            self.starting_enemies.append(No_fall_enemy(x, y, [img]))

        for item in map_data['coins']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_coins.append(Coin(x, y, coin_animate))

        for item in map_data['fakecoins']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(Fakecoin(x, y, fakecoin_img))

        for item in map_data['gems']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_gems.append(Gem(x, y, gem_animate))

        for item in map_data['oneups']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(OneUp(x, y, oneup_img))

        for item in map_data['hearts']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(Heart(x, y, heart_img))

        for item in map_data['invinc']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(Invincibility(x, y, invinc_animate))
            
        for item in map_data['flesh']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(Flesh(x, y, flesh_img))

        for item in map_data['fake']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(Fake(x, y, fake_img))

        for i, item in enumerate(map_data['flag']):
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE

            if i == 0:
                img = flag_img
            else:
                img = flagpole_img

            self.starting_flag.append(Flag(x, y, img))

        self.background_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.scenery_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.foreground_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.inactive_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.active_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)

        if map_data['background-color'] != "":
            self.background_layer.fill(map_data['background-color'])

        if map_data['background-img'] != "":
            background_img = pygame.image.load(map_data['background-img'])

            if map_data['background-fill-y']:
                h = background_img.get_height()
                w = int(background_img.get_width() * HEIGHT / h)
                background_img = pygame.transform.scale(background_img, (w, HEIGHT))

            if "top" in map_data['background-position']:
                start_y = 0
            elif "bottom" in map_data['background-position']:
                start_y = self.height - background_img.get_height()

            if map_data['background-repeat-x']:
                for x in range(0, self.width, background_img.get_width()):
                    self.background_layer.blit(background_img, [x, start_y])
            else:
                self.background_layer.blit(background_img, [0, start_y])

        if map_data['scenery-img'] != "":
            scenery_img = pygame.image.load(map_data['scenery-img'])

            if map_data['scenery-fill-y']:
                h = scenery_img.get_height()
                w = int(scenery_img.get_width() * HEIGHT / h)
                scenery_img = pygame.transform.scale(scenery_img, (w, HEIGHT))

            if "top" in map_data['scenery-position']:
                start_y = 0
            elif "bottom" in map_data['scenery-position']:
                start_y = self.height - scenery_img.get_height()

            if map_data['scenery-repeat-x']:
                for x in range(0, self.width, scenery_img.get_width()):
                    self.scenery_layer.blit(scenery_img, [x, start_y])
            else:
                self.scenery_layer.blit(scenery_img, [0, start_y])

        if map_data['foreground-img'] != "":
            foreground_img = pygame.image.load(map_data['foreground-img'])

            if map_data['foreground-fill-y']:
                h = foreground_img.get_height()
                w = int(foreground_img.get_width() * HEIGHT / h)
                foreground_img = pygame.transform.scale(foreground_img, (w, HEIGHT))

            if "top" in map_data['foreground-position']:
                start_y = 0
            elif "bottom" in map_data['foreground-position']:
                start_y = self.height - foreground_img.get_height()

            if map_data['foreground-repeat-x']:
                for x in range(0, self.width, foreground_img.get_width()):
                    self.foreground_layer.blit(foreground_img, [x, start_y])
            else:
                self.foreground_layer.blit(foreground_img, [0, start_y])

        pygame.mixer.music.load(map_data['music'])

        self.gravity = map_data['gravity']
        self.terminal_velocity = map_data['terminal-velocity']

        self.completed = False

        self.blocks.add(self.starting_blocks)
        self.enemies.add(self.starting_enemies)
        self.coins.add(self.starting_coins)
        self.gems.add(self.starting_gems)
        self.powerups.add(self.starting_powerups)
        self.flag.add(self.starting_flag)
        self.lava.add(self.starting_lava)
        self.backwood.add(self.starting_backwood)
        self.backstone.add(self.starting_backstone)

        self.active_sprites.add(self.coins, self.gems, self.enemies, self.powerups, self.lava)
        self.inactive_sprites.add(self.blocks, self.flag, self.backwood, self.backstone)

        self.inactive_sprites.draw(self.inactive_layer)

    def reset(self):
        self.enemies.add(self.starting_enemies)
        #self.powerups.add(self.starting_powerups)

        self.active_sprites.add(self.coins, self.gems, self.enemies, self.powerups, self.lava)

        for e in self.enemies:
            e.reset()

class Game():

    SPLASH = 0
    START = 1
    PLAYING = 2
    PAUSED = 3
    LEVEL_COMPLETED = 4
    GAME_OVER = 5
    VICTORY = 6

    def __init__(self):
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.done = False

        self.reset()

    def start(self):
        self.level = Level(levels[self.current_level])
        self.level.reset()
        self.hero.respawn(self.level)

    def advance(self):
        self.current_level += 1
        self.start()
        self.stage = Game.START

    def reset(self):
        self.hero = Character(hero_images)
        self.current_level = 0
        self.start()
        self.stage = Game.SPLASH

    def display_splash(self, surface):
        line1 = FONT_LG.render(TITLE, 1, WHITE)
        line2 = FONT_SM.render("Press any key to start.", 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2;
        y1 = HEIGHT / 3 - line1.get_height() / 2;

        x2 = WIDTH / 2 - line2.get_width() / 2;
        y2 = y1 + line1.get_height() + 16;

        surface.blit(splash, (0, 0))
        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))

    def display_message(self, surface, primary_text, secondary_text):
        line1 = FONT_MD.render(primary_text, 1, WHITE)
        line2 = FONT_SM.render(secondary_text, 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2;
        y1 = HEIGHT / 3 - line1.get_height() / 2;

        x2 = WIDTH / 2 - line2.get_width() / 2;
        y2 = y1 + line1.get_height() + 16;

        first_rectangle = pygame.transform.scale(b_rectangle, (line1.get_width()+20, line1.get_height()+10))                                      
        surface.blit(first_rectangle, (x1-12, y1-12))
        surface.blit(line1, (x1, y1))
        
        second_rectangle = pygame.transform.scale(b_rectangle, (line2.get_width()+20, line2.get_height()+10))   
        surface.blit(second_rectangle, (x2-12, y2-8))
        surface.blit(line2, (x2, y2))

    def display_stats(self, surface):
        #hearts_text = FONT_SM.render("Hearts: " + str(self.hero.hearts) + " of " + str(self.hero.max_hearts), 1, WHITE)
        lives_text = FONT_SM.render("x" + str(self.hero.lives), 1, WHITE)
        score_text = FONT_SM.render("Score: " + str(self.hero.score), 1, WHITE)
        level_text = FONT_SM.render("World: " + str(int(self.current_level) + 1) , 1, WHITE)

        
        surface.blit(level_text, (WIDTH - level_text.get_width() - 16, HEIGHT - 54))
        surface.blit(score_text, (WIDTH - score_text.get_width() - 16, 16))
        #surface.blit(hearts_text, (32, 32))
        surface.blit(lives_img,(160, HEIGHT - 62))
        surface.blit(lives_text, (230, HEIGHT - 54))
        for x in range(self.hero.max_hearts):
            if x < self.hero.hearts:
                surface.blit(hearts_img, (x * 40 + 16, HEIGHT - 58))
            else:
                surface.blit(black_heart_img, (x * 40 + 16, HEIGHT - 58))
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            elif event.type == pygame.KEYDOWN:
                if self.stage == Game.SPLASH or self.stage == Game.START:
                    self.stage = Game.PLAYING
                    play_music()

                elif self.stage == Game.PLAYING:
                    if event.key == JUMP:
                        self.hero.jump(self.level.blocks)

                elif self.stage == Game.PAUSED:
                    pass

                elif self.stage == Game.LEVEL_COMPLETED:
                    self.advance()

                elif self.stage == Game.VICTORY or self.stage == Game.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset()

        pressed = pygame.key.get_pressed()

        if self.stage == Game.PLAYING:
            if pressed[LEFT]:
                self.hero.move_left()
            elif pressed[RIGHT]:
                self.hero.move_right()
            else:
                self.hero.stop()

    def update(self):
        if self.stage == Game.PLAYING:
            self.hero.update(self.level)
            self.level.enemies.update(self.level, self.hero)
            self.level.coins.update(self.hero)
            self.level.gems.update(self.hero)
            self.level.powerups.update(self.hero)

        if self.level.completed:
            if self.current_level < len(levels) - 1:
                self.stage = Game.LEVEL_COMPLETED
            else:
                self.stage = Game.VICTORY
            pygame.mixer.music.stop()

        elif self.hero.lives == 0:
            self.stage = Game.GAME_OVER
            pygame.mixer.music.stop()

        elif self.hero.hearts == 0:
            self.level.reset()
            self.hero.respawn(self.level)

    def calculate_offset(self):
        x = -1 * self.hero.rect.centerx + WIDTH / 2

        if self.hero.rect.centerx < WIDTH / 2:
            x = 0
        elif self.hero.rect.centerx > self.level.width - WIDTH / 2:
            x = -1 * self.level.width + WIDTH

        return x, 0

    def draw(self):
        offset_x, offset_y = self.calculate_offset()

        self.level.active_layer.fill(TRANSPARENT)
        self.level.active_sprites.draw(self.level.active_layer)

        if self.hero.invincibility % 3 < 2:
            self.level.active_layer.blit(self.hero.image, [self.hero.rect.x, self.hero.rect.y])

        self.window.blit(self.level.background_layer, [offset_x / 4, offset_y])
        self.window.blit(self.level.scenery_layer, [offset_x / 3, offset_y])
        self.window.blit(self.level.foreground_layer, [offset_x / 2, offset_y])
        self.window.blit(self.level.inactive_layer, [offset_x, offset_y])
        self.window.blit(self.level.active_layer, [offset_x, offset_y])

        self.display_stats(self.window)

        if self.stage == Game.SPLASH:
            self.display_splash(self.window)
        elif self.stage == Game.START:
            self.display_message(self.window, "Ready", "Press any key to start")
        elif self.stage == Game.PAUSED:
            pass
        elif self.stage == Game.LEVEL_COMPLETED:
            self.display_message(self.window, "Level Complete", "Press any key to continue")
        elif self.stage == Game.VICTORY:
            self.display_message(self.window, "You Win", "Press 'R' to restart")
        elif self.stage == Game.GAME_OVER:
            self.display_message(self.window, "Game Over", "Press 'R' to restart")

        pygame.display.flip()

    def loop(self):
        while not self.done:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.start()
    game.loop()
    pygame.quit()
    sys.exit()
