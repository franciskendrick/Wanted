from Scripts.Functions import *
from Scripts.Windows import window
import pygame
import os
import json

pygame.init()
path = os.path.dirname(os.path.realpath("Main.py"))

# Json
json_file = open(path + "/Json" + "/Data.json")
data = json.load(json_file)
json_file.close()

menu_enlarge = data["Menu"]["enlarge"]


class Title:
    def __init__(self):
        animation_set = pygame.image.load(
            path + "/Images/Menu" + "/wanted_animation.png")
        self.idx = 0

        self.frames = []
        for img in clip_set_to_list(animation_set):
            # Initialize
            img_rect = pygame.Rect(
                data["Menu"]["WantedTitle_position"], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Menu"]["Shadow_offset"])

            # Resize
            wd, ht = img.get_size()
            size = (wd * 3, ht * 3)
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


class Buttons:
    def __init__(self):
        spriteset = pygame.image.load(
            path + "/Images/Menu" + "/buttons.png")
        order = ["play", "options", "tutorial"]
        images = clip_set_to_list(spriteset)

        hover_palette = {
            (232, 193, 112): (231, 213, 179),
            (222, 158, 65): (232, 193, 112),
            (190, 119, 43): (222, 158, 65),
            (9, 10, 20): (16, 20, 31)}
        enlarge = menu_enlarge * window.enlarge
        
        self.buttons = {}
        for name, img in zip(order, images):
            hover_img = palette_swap(img.convert(), hover_palette)
            img_rect = pygame.Rect(
                data["Menu"]["Buttons_position"][name], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Menu"]["Shadow_offset"])
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
            is_hovered, orig_img, hover_img, img_rect, shadow_img, shadow_rect, hitbox = self.buttons[name]
            img = hover_img if is_hovered else orig_img

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image


def get_sets_from_spriteset(spriteset):
    sets = []
    separator_count = 0
    last_separator = 0
    for y in range(spriteset.get_height()):
        pixel = spriteset.get_at((0, y))

        # Found a Separator
        if pixel == (255, 0, 0, 255):  # red
            # Clip Image
            set = clip(
                spriteset,
                (0, last_separator),
                (spriteset.get_width(), y - last_separator)
            )

            sets.append(set)
            separator_count += 1
            last_separator = y + 1

    return sets


def get_images_from_sets(sets):
    images = []
    current_wd = 0
    for set in sets:
        for x in range(set.get_width()):
            pixel = set.get_at((x, 0))

            # Found a Separator
            if pixel == (0, 255, 0, 255):  # green
                # Clip Image
                action_set = clip(
                    set,
                    (x - current_wd, 0),
                    (current_wd, set.get_height())
                )

                # Append
                images.append(clip_set_to_list(action_set))
                current_wd = 0
                break
            else:
                current_wd += 1
    
    return images


class Suspects:
    def __init__(self):
        spriteset = pygame.image.load(
            path + "/Images/Sprites" + "/sprites.png")
        self.idx = 0

        sets = get_sets_from_spriteset(spriteset)
        self.suspects = []
        for idx, imgs in enumerate(get_images_from_sets(sets)):
            suspect = []
            for img in imgs:
                img_rect = pygame.Rect(
                    data["Menu"]["Suspects_position"][idx], img.get_size())
                shadow_img, shadow_rect = get_shadow(
                    img, img_rect, data["Menu"]["Shadow_offset"])

                shadow_rect.height -= 1
                shadow_img = shadow_img.subsurface(
                    pygame.Rect(0, 0, shadow_rect.width, shadow_rect.height)
                )

                sprite = [
                    img,  # orig image
                    img_rect,  # image rect
                    shadow_img,  # shadow image
                    shadow_rect  # shadow rect
                ]
                suspect.append(sprite)
            self.suspects.append(suspect)

    def draw_animation(self, display):
        # Reset
        if self.idx >= len(self.suspects[0]) * 5:
            self.idx = 0

        # Draw
        for suspect in self.suspects:
            img, img_rect, shadow_img, shadow_rect = suspect[self.idx // 5]

            display.blit(shadow_img, shadow_rect)  # shadow 
            display.blit(img, img_rect)  # image

        # Update
        self.idx += 1

    def draw_stopped(self, display):
        # Reset
        self.idx = 0
        
        # Draw
        for suspect in self.suspects:
            img, img_rect, shadow_img, shadow_rect = suspect[self.idx // 5]

            display.blit(shadow_img, shadow_rect)  # shadow 
            display.blit(img, img_rect)  # image

    def draw(self, display):
        if window.options_toggle["animation"]:
            self.draw_animation(display)
        else:
            self.draw_stopped(display)


class Menu:
    def __init__(self):
        self.init()

    def init(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface((wd / menu_enlarge, ht / menu_enlarge))
        self.rect = pygame.Rect((0, 0), self.display.get_size())

        self.title = Title()
        self.buttons = Buttons()
        self.suspects = Suspects()

    def draw(self, display):
        self.display.fill(window.color)

        self.title.draw(self.display)
        self.buttons.draw(self.display)
        self.suspects.draw(self.display)

        # Blit to Display
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


menu = Menu()
