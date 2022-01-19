from Scripts.Windows import window
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath("Main.py"))


class Music:
    def __init__(self):
        pygame.mixer.music.load(
            path + "/Music" + "/ES_Pixel Ghost - HiP CoLouR.mp3")
        pygame.mixer.music.set_volume(0.75)

        if window.options_toggle["music"]:
            pygame.mixer.music.play(-1)
            self.played = True  
        else:
            self.played = False

    def update(self):
        if window.options_toggle["music"]:
            if self.played:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play(-1)
                self.played = True
        else:
            pygame.mixer.music.pause() 


class Sound:
    def __init__(self):
        self.button_click_sound = pygame.mixer.Sound(
            path + "/Sound" + "/ES_Switch Click 5 - SFX Producer.mp3")
        self.gunshot_sound = pygame.mixer.Sound(
            path + "/Sound" + "/ES_Gunshot Sniper Rifle - SFX Producer.mp3")
        self.gameover_sound = pygame.mixer.Sound(
            path + "/Sound" + "/envatoelements_Game Over.mp3")
        self.pause_sound = pygame.mixer.Sound(
            path + "/Sound" + "/envatoelements_Pause.mp3")

    def play_button_click(self):
        if window.options_toggle["sound"]:
            self.button_click_sound.play()

    def play_gunshot(self):
        if window.options_toggle["sound"]:
            self.gunshot_sound.play()

    def play_gameover(self):
        if window.options_toggle["sound"]:
            self.gameover_sound.play()
    
    def play_pause(self):
        if window.options_toggle["sound"]:
            self.pause_sound.play()


music = Music()
sound = Sound()
