import pygame
pygame.mixer.init()
pygame.mixer.music.load("song.mp3")

import os

os.system('mpg321 song.mp3 &')