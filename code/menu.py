#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame
from pygame import image


class Menu:

    def __init__(self, window):
        self.window = window
        base_path = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(base_path, 'asset', 'images', 'backgroundmenu', 'game_background_4.png')
        imagem_original = pygame.image.load(image_path)
        self.surf = pygame.transform.scale(imagem_original, (1280, 720))
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self, ):

        pygame.mixer_music.load('./asset/audio/Som de fundo.mp3')
        pygame.mixer_music.play(-1)
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(text_size=100, text="Magic Forest", text_color=(28, 27, 8), text_center_pos=(640, 320))
            self.menu_text(text_size=50, text="Start Game", text_color=(255, 255, 255), text_center_pos=(640, 450))
            self.menu_text(text_size=50, text="Exit", text_color=(255, 255, 255), text_center_pos=(640, 550))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()  # End pygame

    def menu_text(self, text_size:int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font = pygame.font.SysFont(name="Caladea", size=text_size)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)




