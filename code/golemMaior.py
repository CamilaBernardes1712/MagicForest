#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame

from code.config import GOLEM_KING_HP, GOLEM_KING_SPEED
from code.enemy import Enemy

class GolemMaior(Enemy):
    def __init__(self, pos_x: float, pos_y: float):
        super().__init__("GolemMaior", pos_x, pos_y, hp=GOLEM_KING_HP, speed=GOLEM_KING_SPEED, damage=5, folder_name="enemy/Golem maior")
        self.weapon = "Mini-espada"

        base_path = os.getcwd()
        audio_path = os.path.join(base_path, "asset", "audio", "Ataque inimigo master.mp3")
        self.sound_attack = pygame.mixer.Sound(audio_path)

    def move(self, dt: float):
        if self.current_action == "Slashing" and self.current_frame == 0 and self.frame_timer == 0.0:
            self.sound_attack.play()
        super().move(dt)
