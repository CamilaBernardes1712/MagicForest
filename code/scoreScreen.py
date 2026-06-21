#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.score import Score

class ScoreScreen:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont("Verdana", 26)
        self.title_font = pygame.font.SysFont("Verdana", 60, bold=True)

    def run(self):
        score = Score()
        top_scores = score.top10()
        score.close()

        while True:
            self.window.fill((20, 45, 30))
            title = self.title_font.render("Score", True, (255, 230, 120))
            self.window.blit(title, ((1280 - title.get_width()) // 2, 70))

            if not top_scores:
                text = self.font.render("Nenhuma pontuacao salva ainda.", True, (255, 255, 255))
                self.window.blit(text, ((1280 - text.get_width()) // 2, 230))
            else:
                for index, row in enumerate(top_scores, start=1):
                    name, score_value, date = row
                    line = f"{index}. {name} - {score_value} pontos - {date}"
                    text = self.font.render(line, True, (255, 255, 255))
                    self.window.blit(text, (300, 170 + index * 42))

            instruction = self.font.render("Pressione Esc para voltar", True, (220, 220, 220))
            self.window.blit(instruction, ((1280 - instruction.get_width()) // 2, 650))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            pygame.display.flip()
