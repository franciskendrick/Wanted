from Scripts.Functions import *
from Scripts.Windows import window
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


class Title:
    def __init__(self):
        animation_set = pygame.image.load(
            path + "/Images/Crosshair" + "/crosshair_animation.png")
        self.idx = 0

        self.frames = []
        for img in clip_set_to_list(animation_set):
            # Initialize
            img_rect = pygame.Rect(
                data["Crosshair"]["CrosshairTitle_position"], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, data["Crosshair"]["Shadow_offset"])

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


crosshair_title = Title()
