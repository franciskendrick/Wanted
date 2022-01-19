from Scripts.Functions import *
from Scripts.Windows import window
from Scripts.Music import sound
from tkinter import messagebox
import tkinter as tk
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

json_file = open(path + "/Json" + "/Game.json")
game_info = json.load(json_file)
json_file.close()

options_enlarge = data["Options"]["enlarge"]


class Title:
    def __init__(self):
        animation_set = pygame.image.load(
            path + "/Images/Options" + "/options_animation.png")
        self.idx = 0

        self.frames = []
        for img in clip_set_to_list(animation_set):
            # Initialize
            img_rect = pygame.Rect(
                data["Options"]["OptionsTitle_position"], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Options"]["Shadow_offset"])
            
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


def get_sets_from_spriteset(spriteset, order):
    sets = {}
    idx = 0
    cur_ht = 0
    for y in range(spriteset.get_height()):
        pixel = spriteset.get_at((0, y))
        if pixel == (255, 0, 0, 255):  # red
            set = clip(
                spriteset, 
                (0, y - cur_ht),
                (spriteset.get_width(), cur_ht))

            sets[order[idx]] = set
            cur_ht = 0
            idx += 1
        else:
            cur_ht += 1

    return sets 


def get_images_from_sets(sets, button_order):
    images = {}
    for name in sets:
        set = sets[name]
        imgs = clip_set_to_list(set)
        images[name] = imgs

    buttons = {}
    for name, button in zip(button_order, images["buttons"]):
        buttons[name] = button
    images["buttons"] = buttons

    return images, buttons


class Buttons:
    # Initialize
    def __init__(self):
        self.labels = {}
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
        self.enlarge = options_enlarge * window.enlarge

        self.init_redirect()
        self.init_toggleable()
        self.init_windowsize()

    def init_redirect(self):
        spriteset = pygame.image.load(
            path + "/Images/Options" + "/redirect_buttons.png")
        order = ["back", "crosshair"]
        images = clip_set_to_list(spriteset)

        buttons = {}
        for name, img in zip(order, images):
            # Initialize
            hover_img = palette_swap(img.convert(), self.palettes["on"]["hover"])
            img_rect = pygame.Rect(
                data["Options"]["Buttons_position"][name], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Options"]["Shadow_offset"])
            hitbox = pygame.Rect(
                img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                img_rect.width * self.enlarge, img_rect.height * self.enlarge)

            # Append
            button = [
                False,  # is_hovered
                img,  # orig image
                hover_img,  # hover image
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox,  # hitbox
            ]
            buttons[name] = button
        self.buttons["redirect"] = buttons

    def init_toggleable(self):
        spriteset = pygame.image.load(
            path + "/Images/Options" + "/toggleable_buttons.png")
        order = ["animation", "music", "sound", "dark_mode"]
        toggle_status = game_info["Options"]["ToggleStatus_toggleable"]
        images = clip_set_to_list(spriteset)

        buttons = {}
        for name, img in zip(order, images):
            # Initialize
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
                data["Options"]["Buttons_position"][name], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Options"]["Shadow_offset"])
            hitbox = pygame.Rect(
                img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                img_rect.width * self.enlarge, img_rect.height * self.enlarge)

            # Append
            button = [
                False,  # is_hovered
                toggle_status[name],  # toggle status
                palette_swapped_imgs,  # palette swapped images
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox  # hitbox
            ]
            buttons[name] = button
        self.buttons["toggleable"] = buttons

    def init_windowsize(self):
        spriteset = pygame.image.load(
            path + "/Images/Options" + "/windowsize_buttons.png")
        button_palettes = {
            "on": {
                "hover": {
                    (222, 158, 65): (232, 193, 112),
                    (190, 119, 43): (222, 158, 65), 
                    (136, 75, 43): (190, 119, 43),  
                    (9, 10, 20): (16, 20, 31)}
            },
            "off": {
                "orig": {
                    (222, 158, 65): (32, 46, 55),
                    (190, 119, 43): (21, 29, 40),
                    (136, 75, 43): (16, 20, 31),
                    (9, 10, 20): (9, 10, 20)},
                "hover": {
                    (222, 158, 65): (57, 74, 80),
                    (190, 119, 43): (32, 46, 55),
                    (136, 75, 43): (21, 29, 40),
                    (9, 10, 20): (16, 20, 31)}
            }
        }
        sets = get_sets_from_spriteset(spriteset, ["labels", "buttons"])
        images, buttons = get_images_from_sets(sets, ["640x360", "1280x720", "1920x1080"])

        # Append Labels
        img = images["labels"]
        img_rect = pygame.Rect(
            data["Options"]["Labels_position"]["window_size"], 
            img.get_rect().size)
        shadow_img, shadow_rect = get_shadow(
            img, img_rect, data["Options"]["Shadow_offset"])

        label = [
            img,  # image
            img_rect,  # image rect
            shadow_img,  # shadow image
            shadow_rect  # shadow rect
        ]
        self.labels["windowsize"] = label

        # Append Buttons
        windowsize = game_info["Options"]["windowsize"]
        for name in images["buttons"]:
            img = images["buttons"][name]
            palette_swapped_imgs = {}
            for toggle in button_palettes:
                swapped_imgs = {}
                for type in button_palettes[toggle]:
                    palette = button_palettes[toggle][type]
                    swapped_imgs[type] = palette_swap(img.convert(), palette)
                palette_swapped_imgs[toggle] = swapped_imgs
            else:
                palette_swapped_imgs["on"]["orig"] = img
            img_rect = pygame.Rect(
                data["Options"]["Buttons_position"][name], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Options"]["Shadow_offset"])
            hitbox = pygame.Rect(
                img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                img_rect.width * self.enlarge, img_rect.height * self.enlarge)

            # Append
            button = [
                False,  # is_hovered
                # toggle_status[name],  # toggle status
                True if windowsize == name else False,  # toggle status
                palette_swapped_imgs,  # palette swapped images
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox  # hitbox
            ]
            buttons[name] = button
        self.buttons["windowsize"] = buttons

    # Draw
    def draw(self, display):
        self.draw_redirect(display)
        self.draw_toggleable(display)
        self.draw_windowsize(display)

    def draw_redirect(self, display):
        buttons = self.buttons["redirect"]
        for name in buttons:
            is_hovered, orig_img, hover_img, img_rect, shadow_img, shadow_rect, hitbox = buttons[name]
            img = hover_img if is_hovered else orig_img
            
            display.blit(shadow_img, shadow_rect)  # rect
            display.blit(img, img_rect)  # image

    def draw_toggleable(self, display):
        buttons = self.buttons["toggleable"]
        for name in buttons:
            is_hovered, toggle_stat, palette_swapped_imgs, img_rect, shadow_img, shadow_rect, hitbox = buttons[name]
            toggle_palette_img = palette_swapped_imgs["on"] if toggle_stat else palette_swapped_imgs["off"]
            img = toggle_palette_img["hover"] if is_hovered else toggle_palette_img["orig"]

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image

    def draw_windowsize(self, display):
        label = self.labels["windowsize"]

        img, img_rect, shadow_img, shadow_rect = label
        display.blit(shadow_img, shadow_rect)  # shadow
        display.blit(img, img_rect)  # image

        buttons = self.buttons["windowsize"]
        for name in buttons:
            is_hovered, toggle_stat, palette_swapped_imgs, img_rect, shadow_img, shadow_rect, hitbox = buttons[name]
            toggle_palette_img = palette_swapped_imgs["on"] if toggle_stat else palette_swapped_imgs["off"]
            img = toggle_palette_img["hover"] if is_hovered else toggle_palette_img["orig"]

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image


class Options:
    # Initialize
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface((wd / options_enlarge, ht / options_enlarge))
        self.rect = pygame.Rect((0, 0), self.display.get_size())

        self.title = Title()
        self.buttons = Buttons()

    # Draw
    def draw(self, display):
        self.display.fill(window.color)

        self.title.draw(self.display)
        self.buttons.draw(self.display)

        # Blit to Screen
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
                    self.buttons.buttons["toggleable"][name][1] = not self.buttons.buttons["toggleable"][name][1]
                    self.update_options_toggle()
                    return name
                    
            # Window Size Buttons
            for name in self.buttons.buttons["windowsize"]:
                *_, hitbox = self.buttons.buttons["windowsize"][name]

                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    sound.play_button_click()

                    if self.ask_windowsize_confirmation():
                        for new_name in self.buttons.buttons["windowsize"]:
                            self.buttons.buttons["windowsize"][new_name][1] = False
                        self.buttons.buttons["windowsize"][name][1] = True 
                        self.update_options_toggle()
                        window.enlarge = window.enlarge_windowsize[name]
                        window.update_gameinfo(options.buttons.buttons["windowsize"])
                        return name

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
    def update_options_toggle(self):
        options_toggle = {}
        for name in window.options_toggle:
            options_toggle[name] = self.buttons.buttons["toggleable"][name][1]
        window.options_toggle = options_toggle

    def ask_windowsize_confirmation(self):
        root = tk.Tk()
        root.withdraw()
        answer = messagebox.askyesno("Confirmation", "The game will end after executing the command. Your progress will not be saved. Do you still wish to proceed?")
        root.destroy()

        return answer


options = Options()
