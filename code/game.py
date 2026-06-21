#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.config import WINDOW_HEIGHT, WINDOW_WIDTH
from code.level import Level
from code.menu import Menu
from code.scoreScreen import ScoreScreen

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("O Guarda Florestal")
        self.menu = Menu(self.window)

    def run(self):
        playing = True

        while playing:
            menu_option = self.menu.run()
            if menu_option is None:
                continue

            option_upper = str(menu_option).upper()
            if "START" in option_upper or "GAME" in option_upper or "NEW" in option_upper or "JOGAR" in option_upper:
                level = Level(self.window, name="Magic Forest")
                level.run()
            elif "SCORE" in option_upper or "PONTUACAO" in option_upper:
                score_screen = ScoreScreen(self.window)
                score_screen.run()
            elif "QUIT" in option_upper or "EXIT" in option_upper or "SAIR" in option_upper:
                playing = False

        pygame.quit()



