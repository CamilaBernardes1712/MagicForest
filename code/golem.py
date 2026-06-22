#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame

from code.config import GOLEM_HP, GOLEM_SPEED, GOLEM_DAMAGE
from code.enemy import Enemy
from code.paths import resource_path


class Golem(Enemy):
    def __init__(self, pos_x: float, pos_y: float):
        super().__init__("Golem", pos_x, pos_y, hp=GOLEM_HP, speed=GOLEM_SPEED, damage=GOLEM_DAMAGE, folder_name="enemy/Golem comum")
        self.weapon = "Machado"

        audio_path = resource_path(os.path.join("asset", "audio", "Ataque inimigo.mp3"))
        self.sound_attack = pygame.mixer.Sound(audio_path)

    def move(self, dt: float):
        if self.current_action == "Slashing" and self.current_frame == 0 and self.frame_timer == 0.0:
            self.sound_attack.play()
        super().move(dt)

