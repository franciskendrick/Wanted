from Scripts.Functions import *
from Scripts.Windows import window
from Scripts.Cursor import crosshair 
from Scripts.Crosshair import crosshair_title
from Scripts.DefaultCrosshair import default_crosshair
from Scripts.Music import sound
from PIL import Image
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


def separate_from_redseparator(spriteset, order):
    redsets = {}
    current_ht = 0
    idx = 0

    # Loop Over Y Pixels in Tileset
    for y in range(spriteset.get_height()):
        pixel = spriteset.get_at((0, y))

        # A Separator is Found
        if pixel == (255, 0, 0, 255):  # red
            # Clip Image
            set = clip(
                spriteset,
                (0, y - current_ht),
                (spriteset.get_width(), current_ht))
            
            # Append
            redsets[order[idx]] = set
            current_ht = 0
            idx += 1
        else:
            current_ht += 1

    return redsets


def separate_from_greenseparator(redset, order):
    greensets = {}
    current_ht = 0
    idx = 0

    # Loop Over Y Pixels in Tileset
    for y in range(redset.get_height()):
        pixel = redset.get_at((0, y))

        # A Separator is Found
        if pixel == (0, 255, 0, 255):  # green
            # Clip Image
            set = clip(
                redset,
                (0, y - current_ht),
                (redset.get_width(), current_ht))
            
            # Append
            greensets[order[idx]] = set
            current_ht = 0
            idx += 1
        else:
            current_ht += 1

    return greensets


class Buttons:
    # Initialize
    def __init__(self):
        self.buttons = {}
        self.palettes = {
            "red_button": {
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
            },
            "green_button": {
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
            },
            "save": {
                "hover": {
                    (117, 167, 67): (168, 202, 88),
                    (70, 130, 50): (117, 167, 67), 
                    (37, 86, 46): (70, 130, 50),   
                    (9, 10, 20): (16, 20, 31)}
            }
        }
        self.enlarge = crosshair_enlarge * window.enlarge

        spriteset = pygame.image.load(
            path + "/Images/Crosshair/Custom" + "/buttons.png")
        
        redset_order = [
            "color", "outer_circle", "inner_circles", 
            "center_type", "overall_size", "graticule", 
            "redirect"]
        self.redsets = separate_from_redseparator(spriteset, redset_order)
        self.greensets = {
            "graticule": separate_from_greenseparator(
                self.redsets["graticule"], ["length", "width", "visible"])
        }
        for name in self.greensets:
            self.redsets.pop(name)

        self.init_color()
        self.init_outercircle()
        self.init_innercircle()
        self.init_centertype()
        self.init_overallsize()
        self.init_graticule()
        self.init_redirect()

    def init_color(self):
        buttons = {}
        imgs = clip_set_to_list(self.redsets["color"])
        hover_palette = {
            "blue": {
                (60, 94, 139): (79, 143, 186),
                (37, 58, 94): (60, 94, 139),
                (9, 10, 20): (16, 20, 31)},
            "green": {
                (37, 86, 46): (70, 130, 50),
                (25, 51, 45): (37, 86, 46),
                (9, 10, 20): (16, 20, 31)},
            "yellow": {
                (222, 158, 65): (232, 193, 112),
                (190, 119, 43): (222, 158, 65),
                (9, 10, 20): (16, 20, 31)},
            "red": {
                (165, 48, 48): (207, 87, 60),
                (117, 36, 56): (165, 48, 48),
                (9, 10, 20): (16, 20, 31)},
            "purple": {
                (122, 54, 123): (162, 62, 140),
                (64, 39, 81): (122, 54, 123),
                (9, 10, 20): (16, 20, 31)},
            "black": {
                (32, 46, 55): (57, 74, 80),
                (16, 20, 31): (21, 29, 40),
                (9, 10, 20): (16, 20, 31)}}
        for name, img in zip(hover_palette, imgs):
            # Initialize
            toggle_stat = window.game_data["custom_crosshair"]["color"][name]
            hover_img = palette_swap(img.convert(), hover_palette[name])
            img_rect = pygame.Rect(
                data["Crosshair"]["Custom"]["Buttons_position"]["color"][name],
                img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Crosshair"]["Shadow_offset"], (168, 181, 178))
            hitbox = pygame.Rect(
                img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                img_rect.width * self.enlarge, img_rect.height * self.enlarge)

            # Append
            button = [
                False,  # is_hovered
                toggle_stat,  # toggle status 
                img,  # image
                hover_img,  # hover image
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox  # hitbox
            ]
            buttons[name] = button
        self.buttons["color"] = buttons

    def init_outercircle(self):
        # Initialize
        img = clip_set_to_list(self.redsets["outer_circle"])

        toggle_stat = window.game_data["custom_crosshair"]["outer_circle"]
        palette_swapped_imgs = {}
        for toggle in self.palettes["red_button"]:
            swapped_imgs = {}
            for type in self.palettes["red_button"][toggle]:
                palette = self.palettes["red_button"][toggle][type]
                swapped_imgs[type] = palette_swap(img.convert(), palette)
            palette_swapped_imgs[toggle] = swapped_imgs
        else:
            palette_swapped_imgs["on"]["orig"] = img
        img_rect = pygame.Rect(
            data["Crosshair"]["Custom"]["Buttons_position"]["outer_circle"],
            img.get_size())
        shadow_img, shadow_rect = get_shadow(
            img, img_rect, data["Crosshair"]["Shadow_offset"])
        hitbox = pygame.Rect(
            img_rect.x * self.enlarge, img_rect.y * self.enlarge,
            img_rect.width * self.enlarge, img_rect.height * self.enlarge)

        # Append
        button = [
            False,  # is_hovered
            toggle_stat,  # toggle status
            palette_swapped_imgs,  # palette swapped images
            img_rect,  # image rect
            shadow_img,  # shadow image
            shadow_rect,  # shadow rect
            hitbox
        ]
        self.buttons["outer_circle"] = button

    def init_innercircle(self):
        buttons = {}
        imgs = clip_set_to_list(self.redsets["inner_circles"])
        order = ["1st", "2nd", "3rd"]
        for name, img in zip(order, imgs):
            # Initialize
            toggle_stat = window.game_data["custom_crosshair"]["inner_circles"][name]
            palette_swapped_imgs = {}
            for toggle in self.palettes["green_button"]:
                swapped_imgs = {}
                for type in self.palettes["green_button"][toggle]:
                    palette = self.palettes["green_button"][toggle][type]
                    swapped_imgs[type] = palette_swap(img.convert(), palette)
                palette_swapped_imgs[toggle] = swapped_imgs
            else:
                palette_swapped_imgs["on"]["orig"] = img
            img_rect = pygame.Rect(
                data["Crosshair"]["Custom"]["Buttons_position"]["inner_circles"][name],
                img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Crosshair"]["Shadow_offset"])
            hitbox = pygame.Rect(
                img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                img_rect.width * self.enlarge, img_rect.height * self.enlarge)

            # Append
            button = [
                False,  # is_hovered
                toggle_stat,  # toggle status
                palette_swapped_imgs,  # palette swapped images
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox  # hitbox
            ]
            buttons[name] = button
        self.buttons["inner_circles"] = buttons

    def init_centertype(self):
        buttons = {}
        imgs = clip_set_to_list(self.redsets["center_type"])
        order = ["dot", "cross", "none"]
        for name, img in zip(order, imgs):
            # Initialize
            toggle_stat = window.game_data["custom_crosshair"]["center_type"][name]
            palette_swapped_imgs = {}
            for toggle in self.palettes["green_button"]:
                swapped_imgs = {}
                for type in self.palettes["green_button"][toggle]:
                    palette = self.palettes["green_button"][toggle][type]
                    swapped_imgs[type] = palette_swap(img.convert(), palette)
                palette_swapped_imgs[toggle] = swapped_imgs
            else:
                palette_swapped_imgs["on"]["orig"] = img
            img_rect = pygame.Rect(
                data["Crosshair"]["Custom"]["Buttons_position"]["center_type"][name],
                img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Crosshair"]["Shadow_offset"])
            hitbox = pygame.Rect(
                img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                img_rect.width * self.enlarge, img_rect.height * self.enlarge)

            # Append
            button = [
                False,  # is_hovered
                toggle_stat,  # toggle status
                palette_swapped_imgs,  # palette swapped images
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox  # hitbox
            ]
            buttons[name] = button
        self.buttons["center_type"] = buttons

    def init_overallsize(self):
        buttons = {}
        imgs = clip_set_to_list(self.redsets["overall_size"])
        order = ["1x", "2x", "3x"]
        for name, img in zip(order, imgs):
            # Initialize
            toggle_stat = window.game_data["custom_crosshair"]["overall_size"][name]
            palette_swapped_imgs = {}
            for toggle in self.palettes["green_button"]:
                swapped_imgs = {}
                for type in self.palettes["green_button"][toggle]:
                    palette = self.palettes["green_button"][toggle][type]
                    swapped_imgs[type] = palette_swap(img.convert(), palette)
                palette_swapped_imgs[toggle] = swapped_imgs
            else:
                palette_swapped_imgs["on"]["orig"] = img
            img_rect = pygame.Rect(
                data["Crosshair"]["Custom"]["Buttons_position"]["overall_size"][name],
                img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Crosshair"]["Shadow_offset"])
            hitbox = pygame.Rect(
                img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                img_rect.width * self.enlarge, img_rect.height * self.enlarge)

            # Append
            button = [
                False,  # is_hovered
                toggle_stat,  # toggle status
                palette_swapped_imgs,  # palette swapped images
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox  # hitbox
            ]
            buttons[name] = button
        self.buttons["overall_size"] = buttons

    def init_graticule(self):
        buttons = {}

        images = {}
        greensets = self.greensets["graticule"]
        for name in greensets:
            images[name] = clip_set_to_list(greensets[name])
        order = {
            "length": ["2", "3", "4", "5", "6"],
            "width": ["1", "2", "3", "4"],
            "visible": ["N", "E", "S", "W"]
        }

        for label in order:
            buttons[label] = {}
            for name, img, in zip(order[label], images[label]):
                # Initialize
                toggle_stat = window.game_data["custom_crosshair"]["graticule"][label][name]
                palette_swapped_imgs = {}
                for toggle in self.palettes["green_button"]:
                    swapped_imgs = {}
                    for type in self.palettes["green_button"][toggle]:
                        palette = self.palettes["green_button"][toggle][type]
                        swapped_imgs[type] = palette_swap(img.convert(), palette)
                    palette_swapped_imgs[toggle] = swapped_imgs
                else:
                    palette_swapped_imgs["on"]["orig"] = img
                img_rect = pygame.Rect(
                    data["Crosshair"]["Custom"]["Buttons_position"]["graticule"][label][name],
                    img.get_size())
                shadow_img, shadow_rect = get_shadow(
                    img, img_rect, data["Crosshair"]["Shadow_offset"])
                hitbox = pygame.Rect(
                    img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                    img_rect.width * self.enlarge, img_rect.height * self.enlarge)

                # Append
                button = [
                    False,  # is_hovered
                    toggle_stat,  # toggle status
                    palette_swapped_imgs,  # palette swapped images
                    img_rect,  # image rect
                    shadow_img,  # shadow image
                    shadow_rect,  # shadow rect
                    hitbox  # hitbox
                ]
                buttons[label][name] = button
        self.buttons["graticule"] = buttons
        
    def init_redirect(self):
        imgs = clip_set_to_list(self.redsets["redirect"])
        self.redirect_order = ["back", "save"]
        for name, img in zip(self.redirect_order, imgs):
            # Initialize
            if name == "back":
                palette = self.palettes["red_button"]["on"]["hover"]
            else:
                palette = self.palettes["save"]["hover"]
            hover_img = palette_swap(img.convert(), palette)
            img_rect = pygame.Rect(
                data["Crosshair"]["Custom"]["Buttons_position"][name],
                img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Crosshair"]["Shadow_offset"])
            hitbox = pygame.Rect(
                img_rect.x * self.enlarge, img_rect.y * self.enlarge,
                img_rect.width * self.enlarge, img_rect.height * self.enlarge)

            # Append
            button = [
                False,  # is_hovered
                img,  # image
                hover_img,  # hover image
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect,  # shadow rect
                hitbox  # hitbox
            ]
            self.buttons[name] = button
        
    # Draw
    def draw(self, display):
        self.draw_color(display)
        self.draw_outercircle(display)
        self.draw_innercircle(display)
        self.draw_centertype(display)
        self.draw_overallsize(display)
        self.draw_graticule(display)
        self.draw_redirect(display)

    def draw_color(self, display):
        buttons = self.buttons["color"]
        for name in buttons:
            is_hovered, toggle_stat, orig_img, hover_img, img_rect, shadow_img, shadow_rect, hitbox = buttons[name]
            img = hover_img if is_hovered else orig_img

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image
            if toggle_stat:
                mark = pygame.Rect(
                    img_rect.x + data["Crosshair"]["Custom"]["ColorToMarkedColor_offset"][0],
                    img_rect.y + data["Crosshair"]["Custom"]["ColorToMarkedColor_offset"][1],
                    2, 2)
                pygame.draw.rect(display, (9, 10, 20), mark)
            elif is_hovered:
                mark = pygame.Rect(
                    img_rect.x + data["Crosshair"]["Custom"]["ColorToMarkedColor_offset"][0],
                    img_rect.y + data["Crosshair"]["Custom"]["ColorToMarkedColor_offset"][1],
                    2, 2)
                pygame.draw.rect(display, (199, 207, 204), mark)

    def draw_outercircle(self, display):
        is_hovered, toggle_stat, palette_swapped_imgs, img_rect, shadow_img, shadow_rect, hitbox = self.buttons["outer_circle"]
        toggle_palette_img = palette_swapped_imgs["on"] if toggle_stat else palette_swapped_imgs["off"]
        img = toggle_palette_img["hover"] if is_hovered else toggle_palette_img["orig"]

        display.blit(shadow_img, shadow_rect)  # shadow
        display.blit(img, img_rect)  # image

    def draw_innercircle(self, display):
        buttons = self.buttons["inner_circles"]
        for name in buttons:
            is_hovered, toggle_stat, palette_swapped_imgs, img_rect, shadow_img, shadow_rect, hitbox = buttons[name]
            toggle_palette_img = palette_swapped_imgs["on"] if toggle_stat else palette_swapped_imgs["off"]
            img = toggle_palette_img["hover"] if is_hovered else toggle_palette_img["orig"]

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image

    def draw_centertype(self, display):
        buttons = self.buttons["center_type"]
        for name in buttons:
            is_hovered, toggle_stat, palette_swapped_imgs, img_rect, shadow_img, shadow_rect, hitbox = buttons[name]
            toggle_palette_img = palette_swapped_imgs["on"] if toggle_stat else palette_swapped_imgs["off"]
            img = toggle_palette_img["hover"] if is_hovered else toggle_palette_img["orig"]

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image

    def draw_overallsize(self, display):
        buttons = self.buttons["overall_size"]
        for name in buttons:
            is_hovered, toggle_stat, palette_swapped_imgs, img_rect, shadow_img, shadow_rect, hitbox = buttons[name]
            toggle_palette_img = palette_swapped_imgs["on"] if toggle_stat else palette_swapped_imgs["off"]
            img = toggle_palette_img["hover"] if is_hovered else toggle_palette_img["orig"]

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image

    def draw_graticule(self, display):
        buttons = self.buttons["graticule"]
        for label in buttons:
            for name in buttons[label]:
                is_hovered, toggle_stat, palette_swapped_imgs, img_rect, shadow_img, shadow_rect, hitbox = buttons[label][name]
                toggle_palette_img = palette_swapped_imgs["on"] if toggle_stat else palette_swapped_imgs["off"]
                img = toggle_palette_img["hover"] if is_hovered else toggle_palette_img["orig"]

                display.blit(shadow_img, shadow_rect)  # shadow
                display.blit(img, img_rect)  # image

    def draw_redirect(self, display):
        for name in self.redirect_order:
            is_hovered, orig_img, hover_img, img_rect, shadow_img, shadow_rect, hitbox = self.buttons[name]
            img = hover_img if is_hovered else orig_img

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image


class Labels:
    # Initialize
    def __init__(self):
        self.labels = {}
        spriteset = pygame.image.load(
            path + "/Images/Crosshair/Custom" + "/labels.png")

        order = ["color", "inner_circles", "center_type", "overall_size", "graticule"]
        self.redsets = separate_from_redseparator(spriteset, order)
        self.greensets = {
            "color": separate_from_greenseparator(
                self.redsets["color"], ["position", "background"]), 
            "graticule": separate_from_greenseparator(
                self.redsets["graticule"], ["position", "sublabels", "arrows"])
        }
        for name in self.greensets:
            self.redsets.pop(name)

        self.init_redsets()
        self.init_greensets()

    def init_redsets(self):
        labels = {}
        for name in self.redsets:
            # Initialize
            img = clip_set_to_list(self.redsets[name])
            img_rect = pygame.Rect(
                data["Crosshair"]["Custom"]["Labels_position"][name], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Crosshair"]["Shadow_offset"])

            # Append
            label = [
                img,  # image
                img_rect,  # image rect
                shadow_img,  # shadow image
                shadow_rect  # shadow rect
            ]
            labels[name] = label
        self.labels["redlabel"] = labels

    def init_greensets(self):
        labels = {}
        sublabels_order = ["length", "width", "visible"]
        for name in self.greensets:
            green_labels = {}
            for green_name in self.greensets[name]:
                # Initialize
                if green_name != "sublabels":
                    img = clip_set_to_list(self.greensets[name][green_name])
                    img_rect = pygame.Rect(
                        data["Crosshair"]["Custom"]["Labels_position"][name][green_name],
                        img.get_size())
                    shadow_img, shadow_rect = get_shadow(
                        img, img_rect, data["Crosshair"]["Shadow_offset"])

                    # Append
                    label = [
                        img,  # image
                        img_rect,  # image rect
                        shadow_img,  # shadow image
                        shadow_rect  # shadow rect
                    ]
                    green_labels[green_name] = label
                else:
                    sublabels = {}
                    imgs = clip_set_to_list(self.greensets[name][green_name])
                    for sublabel_name, img in zip(sublabels_order, imgs):
                        img_rect = pygame.Rect(
                            data["Crosshair"]["Custom"]["Labels_position"][name][green_name][sublabel_name],
                            img.get_size())
                        shadow_img, shadow_rect = get_shadow(
                            img, img_rect, data["Crosshair"]["Shadow_offset"])

                        # Append
                        label = [
                            img,  # image
                            img_rect,  # image rect
                            shadow_img,  # shadow image
                            shadow_rect  # shadow rect
                        ]
                        sublabels[sublabel_name] = label
                    green_labels[green_name] = sublabels
                
                labels[name] = green_labels
        self.labels["greenlabel"] = labels

    # Draw
    def draw(self, display):
        # Red Labels
        redlabels = self.labels["redlabel"]
        for name in redlabels:
            img, img_rect, shadow_img, shadow_rect = redlabels[name]

            display.blit(shadow_img, shadow_rect)  # shadow
            display.blit(img, img_rect)  # image

        # Green Labels
        greenlabels = self.labels["greenlabel"]
        for name in greenlabels:
            for green_name in greenlabels[name]:
                green_label = greenlabels[name][green_name]
                if green_name != "sublabels":
                    img, img_rect, shadow_img, shadow_rect = green_label

                    display.blit(shadow_img, shadow_rect)  # shadow
                    display.blit(img, img_rect)  # image
                else:
                    for sublabel_name in green_label:
                        img, img_rect, shadow_img, shadow_rect = green_label[sublabel_name]

                        display.blit(shadow_img, shadow_rect)  # shadow
                        display.blit(img, img_rect)  # image


class Preview:
    # Initialize
    def __init__(self):
        self.init_surface()
        self.init_parts()

    def init_surface(self):
        self.preview = pygame.Surface((17, 17), pygame.SRCALPHA)
        self.preview.fill((0, 0, 0, 0))
        self.rect = pygame.Rect(
            data["Crosshair"]["Custom"]["CrosshairPreview_position"],
            self.preview.get_size())

    def init_parts(self):
        self.parts = {}
        spriteset = pygame.image.load(
            path + "/Images/Crosshair/Custom" + "/customization_parts.png")
        order = {
            "outer_circle": None, 
            "inner_circles": ["1st", "2nd", "3rd"], 
            "graticules": {
                "length": ["2", "3", "4", "5", "6"],
                "width": ["1", "2", "3", "4"],
                "direction": ["N", "E", "S", "W"]
            }, 
            "centers": ["dot", "cross"]}
        sets = separate_from_redseparator(spriteset, list(order))

        # Outer Circle
        img = clip_set_to_list(sets["outer_circle"])
        rect = pygame.Rect(
            data["Crosshair"]["Custom"]["PreviewParts_position"]["outer_circle"],
            img.get_rect().size)
        self.parts["outer_circle"] = [img, rect]

        # Inner Circles, Centers
        for label in ["inner_circles", "centers"]:
            self.parts[label] = {}
            imgs = clip_set_to_dict(sets[label], order[label])
            for name in order[label]:
                # Initialize
                img = imgs[name]
                rect = pygame.Rect(
                    data["Crosshair"]["Custom"]["PreviewParts_position"][label],
                    img.get_rect().size)

                # Append
                self.parts[label][name] = [img, rect]
        
        # Graticules
        self.parts["graticules"] = {}
        imgs = clip_set_to_dict(sets["graticules"], order["graticules"]["width"])
        degree = 0
        for direction in order["graticules"]["direction"]:
            default_position = data["Crosshair"]["Custom"]["PreviewParts_position"]["graticules_direction"][direction]
            graticules_direction = {}
            for width in order["graticules"]["width"]:
                graticules_width = {}
                for length in order["graticules"]["length"]:
                    img = imgs[width]

                    wd, ht = img.get_rect().size
                    cropped_region = pygame.Rect(0, 0, wd, ht - (6 - int(length)))
                    cropped_img = img.subsurface(cropped_region)
                    rotated_img = pygame.transform.rotate(cropped_img, degree)

                    position = {
                        "N": default_position,
                        "E": (default_position[0] + (6 - int(length)), default_position[1]),
                        "S": (default_position[0], default_position[1] + (6 - int(length))),
                        "W": default_position
                    }
                    rect = pygame.Rect(
                        position[direction],
                        rotated_img.get_rect().size)

                    graticules_width[length] = [rotated_img, rect]
                graticules_direction[width] = graticules_width
            self.parts["graticules"][direction] = graticules_direction
            degree -= 90

        # Color
        self.color_palette = {
            "blue": {
                (117, 36, 56): (37, 58, 94), 
                (165, 48, 48): (60, 94, 139)},
            "green": {
                (117, 36, 56): (25, 51, 45),
                (165, 48, 48): (37, 86, 46)},
            "yellow": {
                (117, 36, 56): (190, 119, 43),
                (165, 48, 48): (222, 158, 65)},
            "red": {
                (117, 36, 56): (117, 36, 56),
                (165, 48, 48): (165, 48, 48)},
            "purple": {
                (117, 36, 56): (64, 39, 81),
                (165, 48, 48): (122, 54, 123)},
            "black": {
                (117, 36, 56): (16, 20, 31),
                (165, 48, 48): (32, 46, 55)}
        }

    # Draw
    def draw(self, display, buttons):
        self.preview = self.blit_crosshair(self.preview, buttons)

        # Blit Preview to Display
        wd, ht = self.rect.size
        resized_preview = pygame.transform.scale(
            self.preview, (wd * 3, ht * 3))

        display.blit(resized_preview, self.rect)

    def blit_crosshair(self, surface, buttons):
        # Center
        btns = buttons["center_type"]
        [center] = [name for name in btns if btns[name][1]]
        if center != "none":
            surface.blit(*self.parts["centers"][center])

        # Graticule
        btns = buttons["graticule"]
        visible_graticules = [name for name in btns["visible"] if btns["visible"][name][1]]
        [width] = [name for name in btns["width"] if btns["width"][name][1]]
        [length] = [name for name in btns["length"] if btns["length"][name][1]]
        for direction in visible_graticules:
            img, rect = self.parts["graticules"][direction][width][length]
            surface.blit(img, rect)

        # Outer Circle
        if buttons["outer_circle"][1]:
            surface.blit(*self.parts["outer_circle"])

        # Inner Circles
        btns = buttons["inner_circles"]
        inner_circles = [name for name in btns if btns[name][1]]
        for inner_circle in inner_circles:
            surface.blit(*self.parts["inner_circles"][inner_circle])

        # Color
        btns = buttons["color"]
        [color] = [name for name in btns if btns[name][1]]
        surface = palette_swap(
            surface, self.color_palette[color])

        return surface

    # Update
    def update(self):
        self.preview.fill((0, 0, 0, 0))

    # Functions
    def save_crosshair(self, buttons):
        # Get Crosshair
        crosshair = pygame.Surface(self.preview.get_size())
        crosshair = self.blit_crosshair(crosshair, buttons)

        # Save Pygame Surface
        crosshair_path = path + "/Images/Cursors/Crosshairs" + "/custom.png"
        pygame.image.save(crosshair, crosshair_path)

        # Remove Black Color
        img = Image.open(crosshair_path)
        rgba = img.convert("RGBA")
        pixels = rgba.getdata()

        new_pixels = []
        for pixel in pixels:
            if pixel == (0, 0, 0, 255):  # black
                new_pixels.append((0, 0, 0, 0))
            else:
                new_pixels.append(pixel)

        # Save Pillow Image
        rgba.putdata(new_pixels)
        rgba.save(crosshair_path)
            

class CustomCrosshair:
    # Initialize
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface((wd / crosshair_enlarge, ht / crosshair_enlarge))
        self.rect = pygame.Rect((0, 0), self.display.get_size())

        self.title = crosshair_title
        self.buttons = Buttons()
        self.labels = Labels()
        self.preview = Preview()

    # Draw
    def draw(self, display):
        self.display.fill(window.color)

        self.title.draw(self.display)
        self.labels.draw(self.display)
        self.buttons.draw(self.display)
        self.preview.draw(self.display, self.buttons.buttons)

        # Blit to Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)

    # Handles
    def get_button_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            # Color, Inner Circles, Center Type, Overall Size
            buttons = {
                "color": self.buttons.buttons["color"],
                "center_type": self.buttons.buttons["center_type"],
                "overall_size": self.buttons.buttons["overall_size"]}
            for label in buttons:
                for name in buttons[label]:
                    *_, hitbox = buttons[label][name]

                    mouse_pos = pygame.mouse.get_pos()
                    if hitbox.collidepoint(mouse_pos):
                        sound.play_button_click()
                        for new_name in buttons[label]:
                            buttons[label][new_name][1] = False
                        buttons[label][name][1] = True

                        for new_name in window.game_data["custom_crosshair"][label]:
                            window.game_data["custom_crosshair"][label][new_name] = False
                        window.game_data["custom_crosshair"][label][name] = True

            # Outer Circle
            buttons = self.buttons.buttons["outer_circle"]
            *_, hitbox = buttons
            mouse_pos = pygame.mouse.get_pos()
            if hitbox.collidepoint(mouse_pos):
                sound.play_button_click()
                buttons[1] = not buttons[1]
                window.game_data["custom_crosshair"]["outer_circle"] = buttons[1]

            # Inner Circles
            buttons = self.buttons.buttons["inner_circles"]
            for name in buttons:
                *_, hitbox = buttons[name]

                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    sound.play_button_click()
                    buttons[name][1] = not buttons[name][1]
                    window.game_data["custom_crosshair"]["inner_circles"][name] = buttons[name][1]

            # Graticule
            for set_name in ["width", "length"]:
                buttons = self.buttons.buttons["graticule"][set_name]
                for name in buttons:
                    *_, hitbox = buttons[name]

                    mouse_pos = pygame.mouse.get_pos()
                    if hitbox.collidepoint(mouse_pos):
                        sound.play_button_click()
                        for new_name in buttons:
                            buttons[new_name][1] = False
                        buttons[name][1] = True

                        for new_name in window.game_data["custom_crosshair"]["graticule"][set_name]:
                            window.game_data["custom_crosshair"]["graticule"][set_name][new_name] = False
                        window.game_data["custom_crosshair"]["graticule"][set_name][name] = True

            buttons = self.buttons.buttons["graticule"]["visible"]
            for name in buttons:
                *_, hitbox = buttons[name]

                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    sound.play_button_click()
                    buttons[name][1] = not buttons[name][1]
                    window.game_data["custom_crosshair"]["graticule"]["visible"][name] = buttons[name][1]

            # Back, Save
            buttons = {
                "back": self.buttons.buttons["back"],
                "save": self.buttons.buttons["save"]}
            for name in buttons:
                *_, hitbox = buttons[name]

                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    return name

    def handle_mousemotion(self, event):
        # Find if Button is Hovered
        if event.type == pygame.MOUSEMOTION:
            # Color, Inner Circles, Center Type, Overall Size
            buttons = {
                "color": self.buttons.buttons["color"],
                "inner_circles": self.buttons.buttons["inner_circles"],
                "center_type": self.buttons.buttons["center_type"],
                "overall_size": self.buttons.buttons["overall_size"]}
            for label in buttons:
                for name in buttons[label]:
                    *_, hitbox = buttons[label][name]

                    mouse_pos = pygame.mouse.get_pos()
                    if hitbox.collidepoint(mouse_pos):
                        buttons[label][name][0] = True  # is_hovered
                    else:
                        buttons[label][name][0] = False  # is_hovered

            # Outer Circle, Back, Save
            buttons = {
                "outer_circle": self.buttons.buttons["outer_circle"],
                "back": self.buttons.buttons["back"],
                "save": self.buttons.buttons["save"]}
            for name in buttons:
                *_, hitbox = buttons[name]

                mouse_pos = pygame.mouse.get_pos()
                if hitbox.collidepoint(mouse_pos):
                    buttons[name][0] = True  # is_hovered
                else:
                    buttons[name][0] = False  # is_hovered

            # Graticule
            for set_name in self.buttons.buttons["graticule"]:
                for name in self.buttons.buttons["graticule"][set_name]:
                    *_, hitbox = self.buttons.buttons["graticule"][set_name][name]

                    mouse_pos = pygame.mouse.get_pos()
                    if hitbox.collidepoint(mouse_pos):
                        self.buttons.buttons["graticule"][set_name][name][0] = True  # is_hovered
                    else:
                        self.buttons.buttons["graticule"][set_name][name][0] = False  # is_hovered

    # Functions
    def save_crosshair(self):
        # Save
        self.preview.save_crosshair(self.buttons.buttons)
        window.game_data["crosshair"] = "custom"

        # Update Cursor
        crosshair.init()

        # Update DefaultCrosshair
        for name in default_crosshair.buttons.buttons["toggleable"]:
            default_crosshair.buttons.buttons["toggleable"][name][1] = False


custom_crosshair = CustomCrosshair()
