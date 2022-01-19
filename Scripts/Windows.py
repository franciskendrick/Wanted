import pygame
import os
import json
import time

pygame.init()
path = os.path.dirname(os.path.realpath("Main.py"))

json_file = open(path + "/Json" + "/Game.json")
game_info = json.load(json_file)
json_file.close()


class Window:
    # Initialize
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 640, 360)
        self.enlarge_windowsize = {
            "640x360": 1,
            "1280x720": 2,
            "1920x1080": 3
        }

        # Game
        self.game_data = {
            "high_score": game_info["Game"]["high_score"],
            "crosshair": game_info["Game"]["crosshair"],
            "custom_crosshair": game_info["Game"]["CustomCrosshair"]
        }

        # Options
        self.options_toggle = {
            "animation": game_info["Options"]["ToggleStatus_toggleable"]["animation"],
            "music": game_info["Options"]["ToggleStatus_toggleable"]["music"],
            "sound": game_info["Options"]["ToggleStatus_toggleable"]["sound"],
            "dark_mode": game_info["Options"]["ToggleStatus_toggleable"]["dark_mode"]
        }
        self.enlarge = game_info["Options"]["Window_enlarge"]

        # Game & Sidebar
        self.sidebar_wd = 100
        self.game_rect = pygame.Rect(
            self.sidebar_wd, 0,
            self.rect.width - self.sidebar_wd, self.rect.height)
        self.sidebar_rect = pygame.Rect(
            0, 0, self.sidebar_wd, self.rect.height)
        
        # Windows
        self.colors = {
            "light": (235, 237, 233),
            "dark": (32, 46, 55)
        }
        self.update_color()

        # Framerate 
        self.last_time = time.time()
        self.framerate = 30
        self.update_deltatime()

    def init_window(self):
        win_size = (
            window.rect.width * window.enlarge,
            window.rect.height * window.enlarge)
        win = pygame.display.set_mode(win_size)
        display = pygame.Surface(window.rect.size)

        return win_size, win, display

    def set_icon(self):
        icon = pygame.image.load(path + "/Images/Icon" + "/icon.png")
        pygame.display.set_icon(icon)

    # Draw
    def draw_game(self, display):
        pygame.draw.line(
            display, (9, 10, 20),
            (self.game_rect.x, 0), (self.game_rect.x, self.rect.height))

    # Update
    def update_gameinfo(self, options_windowsize_buttons):
        handle_gameinfo = game_info.copy()

        # Edit Game
        handle_gameinfo["Game"]["high_score"] = self.game_data["high_score"]
        handle_gameinfo["Game"]["crosshair"] = self.game_data["crosshair"]
        handle_gameinfo["Game"]["CustomCrosshair"] = self.game_data["custom_crosshair"]

        # Edit Options
        handle_gameinfo["Options"]["Window_enlarge"] = window.enlarge
        handle_gameinfo["Options"]["ToggleStatus_toggleable"] = {
            "animation": self.options_toggle["animation"],
            "music": self.options_toggle["music"],
            "sound": self.options_toggle["sound"],
            "dark_mode": self.options_toggle["dark_mode"]
        }
        for name in options_windowsize_buttons:
            if options_windowsize_buttons[name][1]:
                handle_gameinfo["Options"]["windowsize"] = name

        # Append
        with open(path + "/Json" + "/Game.json", "w") as json_file:
            json.dump(game_info, json_file)

    def update_color(self):
        color = "dark" if self.options_toggle["dark_mode"] else "light"
        self.color = self.colors[color]

    def update_deltatime(self):
        self.dt = time.time() - self.last_time
        self.dt *= self.framerate
        self.last_time = time.time()


window = Window()
