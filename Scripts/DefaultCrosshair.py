from Scripts.Functions import *
from Scripts.Windows import window
from Scripts.Cursor import crosshair 
from Scripts.Crosshair import crosshair_title
from Scripts.Music import sound
import pygame
import os
import json

pygame.init()
path = os.path.dirname(os.path.realpath("Main.py"))

# Window
win_size = (
    window.rect.width * window.enlarge,
    window.rect.height * window.enlarge)
win = pygame.display.set_mode(win_size)

# Json
json_file = open(path + "/Json" + "/Data.json")
data = json.load(json_file)
json_file.close()

crosshair_enlarge = data["Crosshair"]["enlarge"]


class Buttons:
    # Initialize
    def __init__(self):
        self.buttons = {}
        self.palettes = {
            "on": {
                "hover": {
                    (232, 193, 112): (231, 213, 179),
                    (222, 158, 65): (232, 193, 112),
                    (190, 119, 43): (222, 158, 65),
                    (9, 10, 20): (16, 20, 31)}
            },
            "off": {
                "orig": {
                    (232, 193, 112): (57, 74, 80),
                    (222, 158, 65): (32, 46, 55), 
                    (190, 119, 43): (21, 29, 40), 
                    (9, 10, 20): (9, 10, 20)},
                "hover": {
                    (232, 193, 112): (87, 114, 119),
                    (222, 158, 65): (57, 74, 80),
                    (190, 119, 43): (32, 46, 55),
                    (9, 10, 20): (16, 20, 31)}
            }
        }
        self.enlarge = crosshair_enlarge * window.enlarge

        self.init_redirect()
        self.init_toggleable()

    def init_redirect(self):
        spriteset = pygame.image.load(
            path + "/Images/Crosshair/Default" + "/redirect_buttons.png")
        order = ["back", "customize"]
        images = clip_set_to_list(spriteset)

        buttons = {}
        for name, img in zip(order, images):
            hover_img = palette_swap(img.convert(), self.palettes["on"]["hover"])
            img_rect = pygame.Rect(
                data["Crosshair"]["Default"]["Buttons_position"][name], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Crosshair"]["Shadow_offset"])
            hitbox = pygame.Rect(
                img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                img_rect.width * self.enlarge, img_rect.height * self.enlarge)

            button = [
                False,  # is_hovered
                img,  # orig image
                hover_img,  # hover image
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox  # hitbox
            ]
            buttons[name] = button
        self.buttons["redirect"] = buttons

    def init_toggleable(self):
        spriteset = pygame.image.load(
            path + "/Images/Crosshair/Default" + "/toggleable_buttons.png")
        order = [
            "fine", "german", "star", "dot", 
            "target_dot", "circle", "bullseye", "cross"]
        images = clip_set_to_list(spriteset)

        buttons = {}
        for name, img in zip(order, images):
            # Initialize
            toggle_status = True if window.game_data["crosshair"] == name else False
            palette_swapped_imgs = {}
            for toggle in self.palettes:
                swapped_imgs = {}
                for type in self.palettes[toggle]:
                    palette = self.palettes[toggle][type]
                    swapped_imgs[type] = palette_swap(img.convert(), palette)
                palette_swapped_imgs[toggle] = swapped_imgs
            else:
                palette_swapped_imgs["on"]["orig"] = img
            img_rect = pygame.Rect(
                data["Crosshair"]["Default"]["Buttons_position"][name], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Crosshair"]["Shadow_offset"])
            hitbox = pygame.Rect(
                img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                img_rect.width * self.enlarge, img_rect.height * self.enlarge)

            # Append
            button = [
                False,  # is_hovered
                toggle_status,  # toggle status
                palette_swapped_imgs,  # palette swapped images
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox  # hitbox
            ]
            buttons[name] = button
        self.buttons["toggleable"] = buttons

    # Draw
    def draw(self, display):
        self.draw_redirect(display)
        self.draw_toggleable(display)

    def draw_redirect(self, display):
        buttons = self.buttons["redirect"]
        for name in self.buttons["redirect"]:
            is_hovered, orig_img, hover_img, img_rect, shadow_img, shadow_rect, hitbox = buttons[name]
            img = hover_img if is_hovered else orig_img

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image

    def draw_toggleable(self, display):
        buttons = self.buttons["toggleable"]
        for name in self.buttons["toggleable"]:
            is_hovered, toggle_stat, palette_swapped_imgs, img_rect, shadow_img, shadow_rect, hitbox = buttons[name]
            toggle_palette_img = palette_swapped_imgs["on"] if toggle_stat else palette_swapped_imgs["off"]
            img = toggle_palette_img["hover"] if is_hovered else toggle_palette_img["orig"]

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image


class Previews:
    def __init__(self):
        self.previews = {}
        order = [
            "fine", "german", "star", "dot",
            "target_dot", "circle", "bullseye", "cross"]

        # Background
        background_img = pygame.image.load(
            path + "/Images/Crosshair/Default" + "/preview_background.png")
        background_size = background_img.get_size()
        offset = data["Crosshair"]["Default"]["PreviewToCrosshair_offset"]

        # Crosshair
        for name in order:
            background_rect = pygame.Rect(
                data["Crosshair"]["Default"]["Previews_position"][name], background_size)
            crosshair_img = pygame.image.load(
                path + "/Images/Cursors/Crosshairs" + f"/{name}.png")
            crosshair_rect = pygame.Rect(
                background_rect.x + offset[0], background_rect.y + offset[1],
                *crosshair_img.get_size())
            shadow_img, shadow_rect = get_shadow(
                background_img, background_rect, data["Crosshair"]["Shadow_offset"])

            # Append
            preview = [
                background_img,
                background_rect,
                crosshair_img,
                crosshair_rect,
                shadow_img,
                shadow_rect
            ]
            self.previews[name] = preview

    def draw(self, display):
        for name in self.previews:
            background_img, background_rect, crosshair_img, crosshair_rect, shadow_img, shadow_rect = self.previews[name]

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(background_img, background_rect)  # background
            display.blit(crosshair_img, crosshair_rect)  # crosshair


class DefaultCrosshair:
    # Initialize
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface((wd / crosshair_enlarge, ht / crosshair_enlarge))
        self.rect = pygame.Rect((0, 0), self.display.get_size())

        self.title = crosshair_title
        self.buttons = Buttons()
        self.previews = Previews()

    # Draw
    def draw(self, display):
        self.display.fill(window.color)

        self.title.draw(self.display)
        self.buttons.draw(self.display)
        self.previews.draw(self.display)

        # Blit to Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)

    # Handles
    def get_button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            # Redirect Buttons
            for name in self.buttons.buttons["redirect"]:
                *_, hitbox = self.buttons.buttons["redirect"][name]
                
                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    return name

            # Toggle Buttons
            for name in self.buttons.buttons["toggleable"]:
                *_, hitbox = self.buttons.buttons["toggleable"][name]
                
                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    sound.play_button_click()
                    for new_name in self.buttons.buttons["toggleable"]:
                        self.buttons.buttons["toggleable"][new_name][1] = False
                    self.buttons.buttons["toggleable"][name][1] = True
                    self.update_crosshair()

    def handle_mousemotion(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Find if Button is Hovered
            for set_name in self.buttons.buttons:
                for name in self.buttons.buttons[set_name]:
                    *_, hitbox = self.buttons.buttons[set_name][name]

                    mouse_pos = pygame.mouse.get_pos()
                    if hitbox.collidepoint(mouse_pos):
                        self.buttons.buttons[set_name][name][0] = True  # is_hovered
                    else:
                        self.buttons.buttons[set_name][name][0] = False  # is_hovered

    # Functions
    def update_crosshair(self):
        # Edit
        for crosshair_name in self.buttons.buttons["toggleable"]:
            if self.buttons.buttons["toggleable"][crosshair_name][1]:
                break
        window.game_data["crosshair"] = crosshair_name

        # Update
        crosshair.init()


default_crosshair = DefaultCrosshair()
