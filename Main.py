from Scripts.Windows import window
from Scripts.Cursor import cursor, crosshair
from Scripts.CustomCrosshair import custom_crosshair
from Scripts.DefaultCrosshair import default_crosshair
from Scripts.Game import game, sidebar
from Scripts.Menu import menu
from Scripts.Music import music, sound
from Scripts.Options import options
from Scripts.GameOver import gameover
from Scripts.Pause import pause
import pygame
import time
import sys

pygame.init()


# Functions ------------------------------------------------------- #
def init_windows():
    global win_size, win, display
    win_size, win, display = window.init_window()


def game_reset():
    game.init()
    sidebar.init()
    gameover.init()


def spawn_entities():
    global civilians, target
    civilians, target = game.spawn_entities()
    sidebar.posters.target_update(target)


def none():
    pass


# Windows --------------------------------------------------------- #
init_windows()
window.set_icon()
pygame.display.set_caption("Wanted")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


# Redraws --------------------------------------------------------- #
def redraw_game():
    game.display.fill(window.color)
    sidebar.display.fill(window.color)

    # Civilians & Target
    for civilian in civilians:
        civilian.draw(game.display)
    target.draw(game.display)

    # Game & Sidebar
    game.draw(display)
    sidebar.draw(display)

    # Windows
    window.draw_game(display)

    # Cursor & Crosshair
    crosshair.draw("game", display)
    cursor.draw("game", display)

    # Blit to Screen ---------------------------------------------- #
    win.blit(pygame.transform.scale(display, win_size), (0, 0))

    pygame.display.update()


def redraw_menu():
    # Menu
    menu.draw(display)

    # Cursor
    cursor.draw("not_game", display)

    # Blit to Screen ---------------------------------------------- #
    win.blit(pygame.transform.scale(display, win_size), (0, 0))

    pygame.display.update()


def redraw_options():
    display.fill(window.color)

    # Options
    options.draw(display)

    # Cursor
    cursor.draw("not_game", display)

    # Blit to Screen ---------------------------------------------- #
    win.blit(pygame.transform.scale(display, win_size), (0, 0))

    pygame.display.update()


def redraw_defaultcrosshair():
    display.fill(window.color)

    # Default Crosshair
    default_crosshair.draw(display)

    # Cursor
    cursor.draw("not_game", display)

    # Blit to Screen ---------------------------------------------- #
    win.blit(pygame.transform.scale(display, win_size), (0, 0))

    pygame.display.update()    


def redraw_customcrosshair():
    display.fill(window.color)

    # Custom Crosshair
    custom_crosshair.draw(display)

    # Cursor
    cursor.draw("not_game", display)

    # Blit to Screen ---------------------------------------------- #
    win.blit(pygame.transform.scale(display, win_size), (0, 0))

    pygame.display.update()


def redraw_lost():
    game.display.fill(window.color)
    sidebar.display.fill(window.color)

    # Civilians & Target
    for civilian in civilians:
        civilian.draw(game.display)
    target.draw(game.display)

    # Game & Sidebar
    game.draw(display)
    sidebar.draw(display)

    # Windows
    window.draw_game(display)

    # Game Over
    gameover.draw(display)

    # Cursor
    cursor.draw("not_game", display)

    # Blit to Screen ---------------------------------------------- #
    win.blit(pygame.transform.scale(display, win_size), (0, 0))

    pygame.display.update()


def redraw_pause():
    game.display.fill(window.color)
    sidebar.display.fill(window.color)

    # Game & Sidebar
    game.draw(display)
    sidebar.draw(display)

    # Pause
    pause.draw(display)

    # Windows
    window.draw_game(display)

    # Cursor
    cursor.draw("not_game", display)

    # Blit to Screen ---------------------------------------------- #
    win.blit(pygame.transform.scale(display, win_size), (0, 0))

    pygame.display.update()


# Loops ----------------------------------------------------------- #
def game_loop():
    game.status.time_of_start = time.time()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(options.buttons.buttons["windowsize"])
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # pause
                    sound.play_pause()
                    pause_loop()

            # Game
            game.handle_mousedown(event, civilians, target, spawn_entities)

            # Sidebar
            btn_pressed = sidebar.get_button_pressed(event)
            if btn_pressed:
                sound.play_pause()
                sidebar.button.button[0] = False  # is_hovered
                pause_loop()
            sidebar.handle_mousemotion(event)

        # Update
        window.update_deltatime()
        for civilian in civilians:
            civilian.update()
        target.update()
        cursor.update()
        crosshair.update()
        game.update()

        redraw_game()
        clock.tick(window.framerate)
        game.reset_rect()

        # Check if Lost
        if game.status.lost:
            gameover.init()
            gameover.update_entities(civilians + [target])
            sound.play_gameover()
            lost_loop()

    pygame.quit()
    sys.exit()


def menu_loop():
    btn_switchcase = {
        "play": [spawn_entities, game_loop],
        "options": [options_loop]
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(options.buttons.buttons["windowsize"])
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # play
                    functions = btn_switchcase["play"]
                    for function in functions:
                        function()

            # Menu
            btn_pressed = menu.get_button_pressed(event)
            if btn_pressed != None:
                sound.play_button_click()
                functions = btn_switchcase[btn_pressed]
                for function in functions:
                    function(menu_loop) if function == options_loop else function()
            menu.handle_mousemotion(event)

        # Update
        cursor.update()

        redraw_menu()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def options_loop(from_loop):
    btn_switchcase = {
        "back": [from_loop],
        "crosshair": [defaultcrosshair_loop],
        "animation": [none],
        "music": [music.update],
        "sound": [none],
        "dark_mode": [window.update_color],
        "640x360": [pygame.quit, sys.exit],
        "1280x720": [pygame.quit, sys.exit],
        "1920x1080": [pygame.quit, sys.exit]
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(options.buttons.buttons["windowsize"])
                run = False

            # Options
            btn_pressed = options.get_button_pressed(event)
            if btn_pressed != None:
                sound.play_button_click()
                functions = btn_switchcase[btn_pressed]
                for function in functions:
                    function(from_loop) if function == defaultcrosshair_loop else function()
            options.handle_mousemotion(event)

        # Update
        cursor.update()

        redraw_options()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def defaultcrosshair_loop(options_from_loop):
    btn_switchcase = {
        "back": [options_loop],
        "customize": [customcrosshair_loop]
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(options.buttons.buttons["windowsize"])
                run = False

            # Default Crosshair
            btn_pressed = default_crosshair.get_button_pressed(event)
            if btn_pressed != None:
                sound.play_button_click()
                functions = btn_switchcase[btn_pressed]
                for function in functions:
                    function(options_from_loop)
            default_crosshair.handle_mousemotion(event)

        # Update
        cursor.update()

        redraw_defaultcrosshair()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def customcrosshair_loop(options_from_loop):
    btn_switchcase = {
        "back": [defaultcrosshair_loop],
        "save": [custom_crosshair.save_crosshair]
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(options.buttons.buttons["windowsize"])
                run = False
            
            # Custom Crosshair
            btn_pressed = custom_crosshair.get_button_pressed(event)
            if btn_pressed != None:
                sound.play_button_click()
                functions = btn_switchcase[btn_pressed]
                for function in functions:
                    function(options_from_loop) if function == defaultcrosshair_loop else function()
            custom_crosshair.handle_mousemotion(event)

        # Update
        cursor.update()
        custom_crosshair.preview.update()

        redraw_customcrosshair()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def lost_loop():
    btn_switchcase = {
        "play": [game_reset, spawn_entities, game_loop],
        "options": [options_loop],
        "menu": [game_reset, menu_loop]
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(options.buttons.buttons["windowsize"])
                run = False

            # GameOver
            if not gameover.animation.update:
                btn_pressed = gameover.get_button_pressed(event)
                if btn_pressed != None:
                    sound.play_button_click()
                    functions = btn_switchcase[btn_pressed]
                    for function in functions:
                        function(lost_loop) if function == options_loop else function()
            gameover.handle_mousemotion(event)

        # Update
        game.update()
        cursor.update()

        redraw_lost()
        clock.tick(window.framerate)
        game.reset_rect()

    pygame.quit()
    sys.exit()


def pause_loop():
    pause.stats.update()
    btn_switchcase = {
        "play": [game_loop],
        "restart": [game_reset, spawn_entities, game_loop],
        "options": [options_loop],
        "menu": [game_reset, menu_loop]
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.update_gameinfo(options.buttons.buttons["windowsize"])
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # play
                    functions = btn_switchcase["play"]
                    for function in functions:
                        function()

            # Pause
            btn_pressed = pause.get_button_pressed(event)
            if btn_pressed != None:
                sound.play_button_click()
                functions = btn_switchcase[btn_pressed]
                for function in functions:
                    function(pause_loop) if function == options_loop else function()
            pause.handle_mousemotion(event)

        # Update
        cursor.update()

        redraw_pause()
        clock.tick(window.framerate)
        game.reset_rect()

    pygame.quit()
    sys.exit()


# Execute --------------------------------------------------------- #
menu_loop()
