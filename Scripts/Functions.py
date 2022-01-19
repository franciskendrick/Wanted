import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath("Main.py"))


# Pythonic
def merge_dictionaries(*args):  # !!!
    main_dict = args[0]
    for dict in args[1:]:
        main_dict.update(dict)
    return main_dict


# Display
class Font:
    def __init__(self):
        self.order = [
            'A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'Y', 'Z',
            '0', '1', '2', '3',  '4',
            '5', '6', '7', '8', '9', ':', ",", "-", "+"
        ]
        self.characters = {}

        colors = {
            "red": (165, 48, 48),
            "light_green": (70, 130, 50),
            "dark_green": (37, 86, 46),
            "black": (9, 10, 20)}
        font_set = pygame.image.load(
            path + "/Images/Sprites" + "/font.png").convert()
        for name in colors:
            colorswaped_fontset = color_swap(
                font_set, (9, 10, 20), colors[name])
            colorswaped_fontset.set_colorkey((0, 0, 0))
            self.characters[name] = clip_font_to_dict(
                colorswaped_fontset, self.order)

        self.character_spacing = 1
        self.space = 3

    def render_font(self, display, text, pos, color="black", alpha=255, enlarge=2):
        x, y = pos
        x_off = 0

        characters = self.characters[color]
        for char in text:
            if char != " ":  # characters
                character = characters[char]
                wd, ht = character.get_size()

                character = pygame.transform.scale(
                    character, (wd * enlarge, ht * enlarge))
                character.set_alpha(alpha)

                display.blit(character, (x + x_off, y))

                x_off += character.get_width() + self.character_spacing
            else:  # space
                x_off += self.space + self.character_spacing

    def get_font_rect(self, text, pos, enlarge=2):
        wd = 0
        heights = []

        characters = self.characters["black"]
        for char in text:
            if char != " ":  # characters
                character = characters[char]
                wd += character.get_width() + self.character_spacing
                heights.append(character.get_height())
            else:  # space
                wd += self.space + self.character_spacing

        return pygame.Rect(*pos, wd * enlarge, max(heights) * enlarge)
    

# Clip Image
def clip(set, pos, size):
    clip_rect = pygame.Rect(pos, size)
    set.set_clip(clip_rect)
    img = set.subsurface(set.get_clip())

    return img


def clip_set_to_list(set):
    images = []

    # Loop Over every Pixel in Tileset
    for y in range(set.get_height()):
        for x in range(set.get_width()):
            pixel = set.get_at((x, y))

            # A Sprite/Tile is Found
            if pixel == (255, 0, 255, 255):  # magenta
                wd = 0
                ht = 0

                # Find the End of Sprites/Tiles in the X Coordinate
                while True:
                    wd += 1
                    pixel = set.get_at((x + wd, y))
                    if pixel == (0, 255, 255, 255):  # cyan
                        break

                # Find the End of Sprites/Tiles in the Y Coordinate
                while True:
                    ht += 1
                    pixel = set.get_at((x, y + ht))
                    if pixel == (0, 255, 255, 255):  # cyan
                        break

                # Clip Image
                img = clip(
                    set,
                    (x + 1, y + 1),
                    (wd - 1, ht - 1))

                # Append
                images.append(img)
    
    # Unpack Images if Less Than One
    [images] = [images] if len(images) > 1 else images

    return images


def clip_set_to_dict(set, order):
    dict_images = {}

    images = clip_set_to_list(set)
    for name, image in zip(order, images):
        dict_images[name] = image
    
    return dict_images


def clip_font_to_dict(font_set, order):
    characters = {}
    char_wd = 0
    count = 0

    # Loop Over Every Top Pixel in Fontset
    for x in range(font_set.get_width()):
        pixel = font_set.get_at((x, 0))

        # Found a Separator
        if pixel == (255, 0, 0, 255):  # red
            img = clip(
                font_set,
                (x - char_wd, 0),
                (char_wd, font_set.get_height()))

            characters[order[count]] = img

            char_wd = 0
            count += 1
        else:
            char_wd += 1

    return characters


# Palette Swap
def color_swap(img, old_color, new_color):
    # handle_img = img.copy()
    handle_img = pygame.Surface(img.get_size())
    handle_img.fill(new_color)
    img.set_colorkey(old_color)
    handle_img.blit(img, (0, 0))

    return handle_img


def palette_swap(img, palette):
    for old_color in palette:
        new_color = palette[old_color]

        img = color_swap(img, old_color, new_color)
    img.set_colorkey((0, 0, 0))

    return img


# Shadow
def get_shadow(img, rect, shadow_offset, shadow_color=(21, 29, 40)):
    # Get Palette
    handle_img = img.copy()
    palette = {}
    for x in range(handle_img.get_width()):
        for y in range(handle_img.get_height()):
            color = handle_img.get_at((x, y))

            # if solid, and not in palette
            if color[3] != 0 and tuple(color) not in palette:
                palette[tuple(color)] = shadow_color

    # Palette Swap & Rectangle
    x_offset, y_offset = shadow_offset
    shadow_rect = pygame.Rect(rect.x + x_offset, rect.y + y_offset, *rect.size)
    shadow = palette_swap(handle_img.convert(), palette)

    # Return
    return shadow, shadow_rect
