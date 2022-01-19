from Scripts.Functions import *
from Scripts.Windows import window
from Scripts.Game import game
import pygame
import random
import os
import json

pygame.init()
path = os.path.dirname(os.path.realpath("Main.py"))

# Json
json_file = open(path + "/Json" + "/Data.json")
data = json.load(json_file)
json_file.close()


def get_character_spriteset(full_spriteset, type):
    y, ht = data["Entities"]["Spriteset_redSeparator"][type]
    spriteset = clip(
        full_spriteset,
        (0, y),
        (full_spriteset.get_width(), ht)
    )

    return spriteset


def get_images(spriteset, actions, type):
    images = {}
    separators = data["Entities"]["Spriteset_greenSeparator"][type]
    for idx, separator in enumerate(separators):
        left_separator, right_separator = separator
        action_set = clip(
            spriteset,
            (left_separator, 0),
            (right_separator, spriteset.get_height())
        )

        images[actions[idx]] = clip_set_to_list(action_set)

    return images


class Entity:
    # Initialize -------------------------------------------------- #
    def init_images(self):
        full_spriteset = pygame.image.load(
            path + "/Images/Sprites" + "/sprites.png")
        self.idx = 0
        self.status = "idle" if game.status.level >= 0 and game.status.level < 10 else "walk"
        actions = ["idle", "walk"]

        spriteset = get_character_spriteset(full_spriteset, self.type)
        self.images = get_images(spriteset, actions, self.type)

    def init_rect(self, entities):
        # Position
        wd, ht = self.images[self.status][self.idx].get_rect().size
        x = random.randint(1, window.game_rect.width - wd)
        y = random.randint(0, window.game_rect.height - ht)

        # Make Sure that No Entity is Colliding with Each Other
        handle_rect = pygame.Rect(x, y, wd, ht)
        for entity in entities:
            if handle_rect.colliderect(entity.rect):
                self.init_rect(entities)
                return

        # Initialize Rectangle
        self.rect = pygame.Rect(x, y, wd, ht)

    def init_offset(self):
        self.offsets = {
            "hitbox": data["Entities"]["RectToHitbox_offset"][self.type],
            "left_turn": data["Entities"]["LeftTurn_offset"][self.type],
        }

    def init_directionvelocity(self):
        if self.status == "idle":
            self.idle_facing()
            self.animation_speed = 5
        else:
            level = game.status.level-10
            vel_idx = level if level <= 4 else 4

            self.walk_velocities(vel_idx)
            self.walk_facing()
            self.animation_speed = data["Entities"]["Animation_speed"][str(vel_idx)]

    def init_hitbox(self):
        x_offset, y_offset = self.offsets["hitbox"]
        self.headbox_data = {
            "x": self.rect.x + x_offset,
            "y": self.rect.y + y_offset,
            "size": [11, 9]
        }
        self.bodybox_data = {
            "x": self.headbox_data["x"] + 1,
            "y": self.headbox_data["y"] + self.headbox_data["size"][1],
            "size": [8, 7]
        }

        self.update_hitbox()

    # Draw -------------------------------------------------------- #
    def draw_animation(self, display):
        # Reset
        imgs = self.images[self.status]
        if self.idx >= len(imgs) * self.animation_speed:
            self.idx = 0

        # Direction
        img = imgs[self.idx // self.animation_speed]
        if self.direction == "left":
            img = pygame.transform.flip(img, True, False)

        # Draw
        display.blit(img, self.rect)

        # Update
        self.idx += 1

    def draw_stopped(self, display):
        # Reset
        self.idx = 0
        
        # Direction
        imgs = self.images[self.status]
        img = imgs[self.idx // self.animation_speed]
        if self.direction == "left":
            img = pygame.transform.flip(img, True, False)

        # Draw
        display.blit(img, self.rect)

    def draw(self, display):
        if window.options_toggle["animation"]:
            self.draw_animation(display)
        else:
            self.draw_stopped(display)

    # Update ------------------------------------------------------ #
    def update(self):
        if self.status == "walk":
            self.movement()
            self.walk_facing()
        self.init_hitbox()

    def movement(self):
        x_vel, y_vel = self.vels
        self.rect.x += x_vel * window.dt
        self.rect.y += y_vel * window.dt

        # X Coordinate
        if self.rect.left <= window.game_rect.left - window.game_rect.x:
            self.rect.left = window.game_rect.left - window.game_rect.x
            x_vel = x_vel * -1
        elif self.rect.right >= window.game_rect.right - window.game_rect.x:
            self.rect.right = window.game_rect.right - window.game_rect.x
            x_vel = x_vel * -1

        # Y Coordinate
        if self.rect.top <= window.game_rect.top:
            self.rect.top = window.game_rect.top
            y_vel = y_vel * -1
        elif self.rect.bottom >= window.game_rect.bottom:
            self.rect.bottom = window.game_rect.bottom
            y_vel = y_vel * -1

        # Update
        self.vels = (x_vel, y_vel)

    # Functions --------------------------------------------------- #
    # Velocities
    def walk_velocities(self, vel_idx):
        choices = data["Entities"]["Movement_velocities"][vel_idx]
        self.vels = random.choice(choices)

    # Facing
    def idle_facing(self):
        self.direction = random.choice(["left", "right"])
        if self.direction == "right":  # right
            self.head_offset = 0
            self.body_offset = 0
        else:  # left
            self.head_offset = self.offsets["left_turn"][0] * window.enlarge
            self.body_offset = self.offsets["left_turn"][1] * window.enlarge

    def walk_facing(self):
        if self.vels[0] > 0:  # positive
            self.direction = "right"
            self.head_offset = 0
            self.body_offset = 0
        else:  # negative
            self.direction = "left"
            self.head_offset = self.offsets["left_turn"][0] * window.enlarge
            self.body_offset = self.offsets["left_turn"][1] * window.enlarge

    # Hitbox
    def update_hitbox(self):
        self.head_hitbox = pygame.Rect(
            self.headbox_data["x"] * window.enlarge + self.head_offset,
            self.headbox_data["y"] * window.enlarge,
            self.headbox_data["size"][0] * window.enlarge,
            self.headbox_data["size"][0] * window.enlarge
        )
        self.body_hitbox = pygame.Rect(
            self.bodybox_data["x"] * window.enlarge + self.body_offset,
            self.bodybox_data["y"] * window.enlarge,
            self.bodybox_data["size"][0] * window.enlarge,
            self.bodybox_data["size"][0] * window.enlarge
        )


class Civilian(Entity):
    def __init__(self, entities, types):
        super().__init__()

        self.type = random.choice(types)
        self.init_images()
        self.init_rect(entities)
        self.init_offset()
        self.init_directionvelocity()
        self.init_hitbox()


class Target(Entity):
    def __init__(self, entities, type):
        super().__init__()

        self.type = type
        self.init_images()
        self.init_rect(entities)
        self.init_offset()
        self.init_directionvelocity()
        self.init_hitbox()
