from Scripts.Functions import *
from Scripts.Windows import window
from Scripts.Cursor import crosshair
from Scripts.Music import sound
import pygame
import os
import json
import time
import random

pygame.init()
path = os.path.dirname(os.path.realpath("Main.py"))

# Windows
win_size = (
    window.rect.width * window.enlarge,
    window.rect.height * window.enlarge)
win = pygame.display.set_mode(win_size)

# Json
json_file = open(path + "/Json" + "/Data.json")
data = json.load(json_file)
json_file.close()

json_file = open(path + "/Json" + "/Game.json")
game_info = json.load(json_file)
json_file.close()

sidebar_enlarge = data["Sidebar"]["enlarge"]


# Game ------------------------------------------------------------ #
class Suspects:
    def __init__(self):
        self.types = [*range(8)]
        self.civilian_population = 1


class Status(Font):
    def __init__(self):
        super().__init__()

        self.level = 0

        self.end_time = 0  # seconds
        self.time = 10  # seconds
        self.time_of_start = None
        self.time_modification = []

        self.lost = False

    def draw(self, display):
        for i, time_mod in enumerate(self.time_modification):
            text, pos, color, alpha, loop_count = time_mod
            self.render_font(display, text, pos, color, alpha)
            if loop_count >= 15:
                self.time_modification[i][3] -= 13  # alpha
            else:
                self.time_modification[i][4] += 1  # loop_count

    def timer(self):
        if self.time > 0:  # alive
            dt = time.time() - self.time_of_start
            if dt * 1000 > 1000:
                self.time -= 1
                self.end_time += 1
                self.time_of_start = time.time()
        else:  # dead
            self.lost = True

    def remove_unused_timemod(self):
        removing_timemod = []
        for time_mod in self.time_modification:
            if time_mod[3] <= 0:  # alpha
                removing_timemod.append(time_mod)

        for time_mod in removing_timemod:
            self.time_modification.remove(time_mod)


class Surface:
    def __init__(self, rect):
        # Screen Shake
        self.shake_loop = 0
        self.shaking = False

        # Mask & Sniper Radius
        self.alpha = 0
        self.sniper_light_radius = 75
        self.mask = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.mask.fill((0, 0, 0, self.alpha))
        self.mixed = pygame.Surface(rect.size, pygame.SRCALPHA)

    def draw_shake(self, rect):
        if self.shaking:
            rect.y += -2

    def draw_mask(self, rect, display):
        center = (crosshair.rect.centerx - rect.x, crosshair.rect.centery)
        pygame.draw.circle(
            self.mask, (9, 10, 20, 0), center, self.sniper_light_radius)

        self.mixed.blit(self.mask, rect, special_flags=pygame.BLEND_RGBA_MULT)
        display.blit(self.mask, (0, 0))

    def screen_shake(self):
        if self.shaking:
            if self.shake_loop > 0 and self.shake_loop < 2:
                self.shake_loop += 1
            else:
                self.shaking = False
                self.shake_loop = 0


class Game:
    # Initialize 
    def __init__(self):
        self.init()

    def init(self):
        self.rect_resized = pygame.Rect(
            window.game_rect.x * window.enlarge, window.game_rect.y * window.enlarge,
            window.game_rect.width * window.enlarge, window.game_rect.height * window.enlarge)
        self.display = pygame.Surface(window.game_rect.size)

        self.suspects = Suspects()
        self.status = Status()
        self.surface = Surface(window.game_rect)

    # Draw 
    def draw(self, display):
        self.surface.draw_shake(window.game_rect)
        self.surface.draw_mask(window.game_rect, self.display)
        self.status.draw(self.display)

        # Blit to Screen
        display.blit(self.display, window.game_rect)

    # Update 
    def update(self):
        self.surface.mask.fill((0, 0, 0, self.surface.alpha))
        self.surface.screen_shake()
        self.status.timer()
        self.status.remove_unused_timemod()

    # Functions 
    def shot(self, civilians, target):
        sound.play_gunshot()
        self.surface.shaking = True
        self.surface.shake_loop += 1
        mouse_center = (
            (crosshair.rect.centerx - window.game_rect.x) * window.enlarge,
            crosshair.rect.centery * window.enlarge)

        # Identify the Score by Finding the Location of Hit
        if target.head_hitbox.collidepoint(mouse_center):  # head-shot
            time_mod = "+5"
            is_shot = True
        elif target.body_hitbox.collidepoint(mouse_center):  # body-shot
            time_mod = "+3"
            is_shot = True
        else:
            done = False
            for civilian in civilians:  # civilian is shot
                if civilian.head_hitbox.collidepoint(mouse_center) or civilian.body_hitbox.collidepoint(mouse_center):
                    time_mod = "-5"
                    done = True

            if not done:  # no one was shot
                time_mod = "-3"

            is_shot = False

        # Update Level
        if is_shot:
            self.status.level += 1

        # Update Highscore
        if self.status.level > window.game_data["high_score"]:
            window.game_data["high_score"] = self.status.level

        # Modify Time Modification
        x_offset, y_offset = (9, 6)
        time_pos = [
            mouse_center[0] / window.enlarge - x_offset,
            mouse_center[1] / window.enlarge - y_offset]
        color = "light_green" if int(time_mod) > 0 else "red"
        self.status.time_modification.append(
            [time_mod, time_pos, color, 255, 0])

        # Modify Time
        self.status.time += int(time_mod)
        if self.status.time < 0:
            self.status.time = 0
        self.status.time_of_start = time.time()

        return is_shot

    def spawn_entities(self):
        from Scripts.Entities import Civilian, Target

        # Types
        target_type = random.choice(self.suspects.types)
        civilian_types = self.suspects.types.copy()
        civilian_types.remove(target_type)

        # Update Game
        if self.status.level > 0 and self.status.level < 10:  # civilian population
            self.suspects.civilian_population += 20
        elif self.status.level > 15 and self.status.level <= 25:  # screen alpha
            self.surface.alpha += 25
        elif self.status.level > 25 and self.status.level <= 33:  # sniper radius
            self.surface.sniper_light_radius -= 2.5

        # Update Entity Position
        civilians = []
        for _ in range(self.suspects.civilian_population):
            civilians.append(Civilian(civilians, civilian_types))
        target = Target(civilians, target_type)

        # Return
        return civilians, target

    def reset_rect(self):
        window.game_rect.x, window.game_rect.y = (window.sidebar_wd, 0)

    # Handles 
    def handle_mousedown(self, event, civilians, target, spawn_entities):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                mouse_pos = pygame.mouse.get_pos()
                if game.rect_resized.collidepoint(mouse_pos):  # in game window
                    is_shot = game.shot(civilians, target)
                    if is_shot:
                        spawn_entities()


# Sidebar --------------------------------------------------------- #
class Posters(Font):
    def __init__(self):
        super().__init__()

        self.posters = []
        spriteset = pygame.image.load(
            path + "/Images/Sidebar" + "/posters.png")
        for i, poster in enumerate(clip_set_to_list(spriteset)):
            rect = pygame.Rect(
                data["Sidebar"]["Posters_position"][i], poster.get_size())
            self.posters.append([poster, rect])

    def draw(self, display):
        self.draw_wanted(display)
        self.draw_stats(display)

    def draw_wanted(self, display):
        # Poster
        for poster in self.posters:
            display.blit(*poster)

        # Target
        display.blit(self.target_img, self.target_rect)

    def draw_stats(self, display):
        # Kills
        text = f"{game.status.level:,}"
        pos = data["Sidebar"]["StatPosterFont_position"]["kills"]
        self.render_font(display, text, pos, enlarge=1)

        # Time
        min, sec = divmod(game.status.time, 60)
        text = f"{str(min).zfill(2)}:{str(sec).zfill(2)}"
        pos = data["Sidebar"]["StatPosterFont_position"]["time"]
        self.render_font(display, text, pos, enlarge=1)

        # High Score
        text = f"{window.game_data['high_score']}"
        pos = data["Sidebar"]["StatPosterFont_position"]["high_score"]
        self.render_font(display, text, pos, enlarge=1)

    def target_update(self, target):
        self.target = target
        pos = data["Sidebar"]["WantedPosterToSprite_position"][self.target.type]
        self.target_img = self.target.images["idle"][0]
        self.target_rect = pygame.Rect(pos, self.target_img.get_rect().size)


class Button:
    def __init__(self):
        hover_palette = {
            (232, 193, 112): (231, 213, 179),
            (222, 158, 65): (232, 193, 112),
            (190, 119, 43): (222, 158, 65),
            (32, 46, 55): (57, 74, 80),
            (21, 29, 40): (32, 46, 55),
            (16, 20, 31): (21, 29, 40),
            (9, 10, 20): (16, 20, 31)}
        enlarge = sidebar_enlarge * window.enlarge
        
        img = pygame.image.load(
            path + "/Images/Sidebar" + "/button.png")
        wd, ht = img.get_rect().size
        size = (wd * 2, ht * 2)

        resized_img = pygame.transform.scale(img, size)
        hover_img = palette_swap(resized_img.convert(), hover_palette)
        img_rect = pygame.Rect(
            data["Sidebar"]["PauseButton_position"], resized_img.get_rect().size)
        shadow_img, shadow_rect = get_shadow(
            resized_img, img_rect, data["Sidebar"]["Shadow_offset"])
        hitbox = pygame.Rect(
            img_rect.x * enlarge, img_rect.y * enlarge,
            img_rect.width * enlarge, img_rect.height * enlarge)

        self.button = [
            False,  # is_hovered
            resized_img,  # orig image
            hover_img,  # hover image
            img_rect,  # image rect
            shadow_img,  # shadow image
            shadow_rect,  # shadow rect
            hitbox,  # hitbox
        ]

    def draw(self, display):
        is_hovered, orig_img, hover_img, img_rect, shadow_img, shadow_rect, hitbox = self.button
        img = hover_img if is_hovered else orig_img

        display.blit(shadow_img, shadow_rect)  # shadow
        display.blit(img, img_rect)  # image


class Sidebar:
    # Initialize 
    def __init__(self):
        self.init()

    def init(self):
        self.display = pygame.Surface(
            (window.sidebar_rect.width // sidebar_enlarge,
            window.sidebar_rect.height // sidebar_enlarge)
        )

        self.posters = Posters()
        self.button = Button()

    # Draw 
    def draw(self, display):
        self.posters.draw(self.display)
        self.button.draw(self.display)

        # Blit to Display
        wd, ht = self.display.get_size()
        size = (wd * sidebar_enlarge, ht * sidebar_enlarge)
        resized_display = pygame.transform.scale(self.display, size)

        display.blit(resized_display, window.sidebar_rect)

    # Handles 
    def get_button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            *_, hitbox = self.button.button

            mouse_pos = pygame.mouse.get_pos()
            if hitbox.collidepoint(mouse_pos):
                return True

    def handle_mousemotion(self, event):
        if event.type == pygame.MOUSEMOTION:
            *_, hitbox = self.button.button

            mouse_pos = pygame.mouse.get_pos()
            if hitbox.collidepoint(mouse_pos):
                self.button.button[0] = True  # is_hovered
            else:
                self.button.button[0] = False  # is_hovered


game = Game()
sidebar = Sidebar()
