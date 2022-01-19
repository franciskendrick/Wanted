from Scripts.Windows import window
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath("Main.py"))


class Cursor:
    def __init__(self):
        # Image
        img = pygame.image.load(path + "/Images/Cursors/Cursor" + "/cursor.png")
        wd, ht = img.get_rect().size
        self.img = pygame.transform.scale(img, (wd * 2, ht * 2))

        # Rectangle
        self.rect = pygame.Rect(
            pygame.mouse.get_pos(),
            self.img.get_rect().size)

        # Mask
        self.mask = pygame.Surface(window.sidebar_rect.size, pygame.SRCALPHA)
        self.mixed = pygame.Surface(window.rect.size, pygame.SRCALPHA)

    def draw(self, loop, display):
        if pygame.mouse.get_focused():
            if loop == "game":
                x, y = (self.rect.x - window.sidebar_rect.x, self.rect.y)
                self.mask.blit(self.img, (x, y))
                self.mixed.blit(self.mask, window.sidebar_rect, special_flags=pygame.BLEND_RGBA_MULT)

                display.blit(self.mask, window.sidebar_rect)
            else:
                display.blit(self.img, self.rect)

    def update(self):
        self.mask.fill((0, 0, 0, 0))

        x, y = pygame.mouse.get_pos()
        self.rect.x, self.rect.y = (x / window.enlarge, y / window.enlarge)


class Crosshair:
    # Initialize
    def __init__(self):
        self.init()

    def init(self):
        # Images
        if window.game_data["crosshair"] != "custom":
            self.init_defaultcrosshair()
        else:
            self.init_customcrosshair()

        # Rectangle
        x, y = pygame.mouse.get_pos()
        wd, ht = self.img.get_rect().size
        self.rect = pygame.Rect(
            x - (wd / 2), y - (ht / 2),
            wd, ht)

        # Mask
        self.mask = pygame.Surface(window.game_rect.size, pygame.SRCALPHA)
        self.mixed = pygame.Surface(window.rect.size, pygame.SRCALPHA)

    def init_defaultcrosshair(self):
        enlarge = 1
        img = pygame.image.load(
            path + "/Images/Cursors/Crosshairs" + f"/{window.game_data['crosshair']}.png")
        wd, ht = img.get_rect().size
        self.img = pygame.transform.scale(
            img, (wd * enlarge, ht * enlarge))

    def init_customcrosshair(self):
        enlarge_switchcase = {
            "1x": 1,
            "2x": 2,
            "3x": 3
        }
        sizes = window.game_data["custom_crosshair"]["overall_size"]
        [size] = [name for name in sizes if sizes[name]]
        enlarge = enlarge_switchcase[size]

        img = pygame.image.load(
            path + "/Images/Cursors/Crosshairs" + f"/{window.game_data['crosshair']}.png")
        wd, ht = img.get_rect().size
        self.img = pygame.transform.scale(
            img, (wd * enlarge, ht * enlarge))

    # Draw
    def draw(self, loop, display):
        if pygame.mouse.get_focused():
            if loop == "game":
                x, y = (self.rect.x - window.game_rect.x, self.rect.y)
                self.mask.blit(self.img, (x, y))
                self.mixed.blit(
                    self.mask, window.game_rect,
                    special_flags=pygame.BLEND_RGBA_MULT)

                display.blit(self.mask, window.game_rect)

    # Update
    def update(self):
        self.mask.fill((0, 0, 0, 0))

        x, y = pygame.mouse.get_pos()
        center = (x / window.enlarge, y / window.enlarge)
        self.rect.center = center


cursor = Cursor()
crosshair = Crosshair()
