#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame

class Menu:
    def __init__(self, window):
        self.window = window
        base_path = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(base_path, "asset", "images", "backgroundmenu", "game_background_4.png")

        try:
            imagem_original = pygame.image.load(image_path)
            self.surf = pygame.transform.scale(imagem_original, (1280, 720))
        except pygame.error:
            self.surf = pygame.Surface((1280, 720))
            self.surf.fill((30, 50, 30))

        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        try:
            pygame.mixer_music.load("./asset/audio/Som de fundo.mp3")
            pygame.mixer_music.play(-1)
        except pygame.error:
            print("Aviso: Audio de fundo nao encontrado.")

        menu_option = 0
        menu_options = ["Start Game", "Score", "Exit"]

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(100, "Magic Forest", (28, 27, 8), (640, 300))

            mouse_pos = pygame.mouse.get_pos()
            for i, option in enumerate(menu_options):
                pos_y = 400 + (i * 70)
                if 500 < mouse_pos[0] < 780 and (pos_y - 25) < mouse_pos[1] < (pos_y + 25):
                    menu_option = i

                color = (28, 27, 8) if i == menu_option else (255, 255, 255)
                self.menu_text(50, option, color, (640, pos_y))

            self.menu_text(20, "Movimentação: use as setas do teclado", (220, 220, 220), (640, 635))
            self.menu_text(20, "Atirar: pressione a barra de espaço", (220, 220, 220), (640, 665))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return menu_options[menu_option]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(menu_options)
                    elif event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        return menu_options[menu_option]

            pygame.display.flip()

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        try:
            text_font = pygame.font.SysFont(name="Verdana", size=text_size)
        except Exception:
            text_font = pygame.font.SysFont(name="Arial", size=text_size)

        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

