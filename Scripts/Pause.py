from Scripts.Functions import *
from Scripts.Windows import window
from Scripts.Game import game
import pygame
import os
import json

pygame.init()
path = os.path.dirname(os.path.realpath("Main.py"))

# Json
json_file = open(path + "/Json" + "/Data.json")
data = json.load(json_file)
json_file.close()

pause_enlarge = data["Pause"]["enlarge"]


class Window:
    def __init__(self):
        img = pygame.image.load(
            path + "/Images/Pause" + "/window.png")
        img_rect = pygame.Rect(
            data["Pause"]["Window_position"],
            img.get_rect().size)
        shadow_img, shadow_rect = get_shadow(
            img, img_rect, data["Pause"]["OutsideShadow_offset"])

        self.window = [
            img,  # orig image
            img_rect,  # image rect
            shadow_img,  # shadow
            shadow_rect  # shadow rect
        ]

    def draw(self, display):
        img, img_rect, shadow_img, shadow_rect = self.window
        display.blit(shadow_img, shadow_rect)  # shadow
        display.blit(img, img_rect)  # image


class Title:
    def __init__(self):
        animation_set = pygame.image.load(
            path + "/Images/Pause" + "/paused_animation.png")
        self.idx = 0

        self.frames = []
        for img in clip_set_to_list(animation_set):
            # Initialize
            img_rect = pygame.Rect(
                data["Pause"]["PausedTitle_position"], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Pause"]["InsideShadow_offset"])

            # Resize
            wd, ht = img.get_size()
            size = (wd * 2, ht * 2)
            img = pygame.transform.scale(img, size)
            shadow_img = pygame.transform.scale(shadow_img, size)

            # Append
            slide = [
                img,  # orig image
                img_rect,  # image rect
                shadow_img,  # shadow
                shadow_rect  # shadow rect
            ]
            self.frames.append(slide)

    def draw_animation(self, display):
        # Reset
        if self.idx >= len(self.frames) * 5:
            self.idx = 0

        # Draw
        img, img_rect, shadow_img, shadow_rect = self.frames[self.idx // 5]
        display.blit(shadow_img, shadow_rect)  # shadow
        display.blit(img, img_rect)  # image

        # Update
        self.idx += 1

    def draw_stopped(self, display):
        # Reset
        self.idx = 0
        
        # Draw
        img, img_rect, shadow_img, shadow_rect = self.frames[self.idx // 5]
        display.blit(shadow_img, shadow_rect)  # shadow
        display.blit(img, img_rect)  # image

    def draw(self, display):
        if window.options_toggle["animation"]:
            self.draw_animation(display)
        else:
            self.draw_stopped(display)



class Stats(Font):
    def __init__(self):
        super().__init__()

        # Status Box
        img = pygame.image.load(
            path + "/Images/Pause" + "/status_box.png")
        rect = pygame.Rect(
            data["Pause"]["StatBox_position"], img.get_rect().size)
        shadow_img, shadow_rect = get_shadow(
            img, rect, data["Pause"]["InsideShadow_offset"])
        self.statbox = [
            img,  # orig image
            rect,  # rect
            shadow_img,  # shadow image
            shadow_rect,  # shadow rect
        ]

    def draw(self, display):
        # Box
        img, rect, shadow_img, shadow_rect = self.statbox
        display.blit(shadow_img, shadow_rect)  # shadow
        display.blit(img, rect)  # image

        # Score
        self.render_font(display, self.score["text"], self.score["pos"], color="dark_green", enlarge=1)

        # Time
        for i, time in enumerate(zip(self.time["texts"], self.time["rects"])):
            text, rect = time
            color = "dark_green" if i % 2 == 0 else "black"
            self.render_font(display, text, (rect.x, rect.y), color=color, enlarge=1)

    def update(self):
        # Score
        self.score = {
            "text": f"{game.status.level:,}",
            "pos": data["Pause"]["StatsFont_position"]["score"]
        }

        # Time
        min, sec = divmod(game.status.time, 60)
        hour, min = divmod(min, 60)
        list_texts = [[str(hour), "H,"], [str(min), "M,"], [str(sec), "S"]]

        new_texts = []
        rects = []
        for texts in list_texts:
            if texts[0] != "0":
                for text in texts:
                    if len(rects) == 0:
                        pos = data["Pause"]["StatsFont_position"]["time"]
                    else:
                        pos = [rects[-1].right, rects[-1].y]

                    rect = self.get_font_rect(text, pos, enlarge=1)
                    new_texts.append(text)
                    rects.append(rect)

        self.time = {
            "texts": new_texts,
            "rects": rects
        }


class Buttons:
    def __init__(self):
        spriteset = pygame.image.load(
            path + "/Images/Pause" + "/buttons.png")
        order = ["play", "restart", "options", "menu"]
        images = clip_set_to_list(spriteset)

        hover_palette = {
            (232, 193, 112): (231, 213, 179),
            (222, 158, 65): (232, 193, 112),
            (190, 119, 43): (222, 158, 65),
            (32, 46, 55): (57, 74, 80),
            (21, 29, 40): (32, 46, 55),
            (16, 20, 31): (21, 29, 40),
            (9, 10, 20): (16, 20, 31)}
        enlarge = pause_enlarge * window.enlarge

        self.buttons = {}
        for name, img in zip(order, images):
            hover_img = palette_swap(img.convert(), hover_palette)
            img_rect = pygame.Rect(
                data["Pause"]["Buttons_position"][name], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Pause"]["InsideShadow_offset"])
            hitbox = pygame.Rect(
                img_rect.x * enlarge, img_rect.y * enlarge,
                img_rect.width * enlarge, img_rect.height * enlarge)

            button = [
                False,  # is_hovered
                img,  # orig image
                hover_img,  # hover image
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox  # hitbox
            ]
            self.buttons[name] = button

    def draw(self, display):
        for name in self.buttons:
            is_hovered, orig_img, hover_img, img_rect, shadow_img, shadow_rect, hitbox = self.buttons[
                name]
            img = hover_img if is_hovered else orig_img

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image


class Pause:
    def __init__(self):
        self.init()

    def init(self):
        wd, ht = window.rect.size

        self.display = pygame.Surface(
            (wd / pause_enlarge, ht / pause_enlarge)).convert_alpha()
        self.rect = pygame.Rect((0, 0), self.display.get_size())

        self.window = Window()
        self.title = Title()
        self.stats = Stats()
        self.buttons = Buttons()

    def draw(self, display):
        self.display.fill((0, 0, 0, 100))

        self.window.draw(self.display)
        self.title.draw(self.display)
        self.stats.draw(self.display)
        self.buttons.draw(self.display)

        # Blit to Display
        display.blit(game.display, window.game_rect)

        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)

    def get_button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for name in self.buttons.buttons:
                *_, hitbox = self.buttons.buttons[name]

                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    return name

    def handle_mousemotion(self, event):
        if event.type == pygame.MOUSEMOTION:
            for name in self.buttons.buttons:
                *_, hitbox = self.buttons.buttons[name]

                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    self.buttons.buttons[name][0] = True  # is_hovered
                else:
                    self.buttons.buttons[name][0] = False  # is_hovered


pause = Pause()
