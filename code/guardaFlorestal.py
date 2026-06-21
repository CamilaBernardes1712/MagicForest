#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame

from code.config import PLAYER_HP, PLAYER_SPEED, WINDOW_HEIGHT, WINDOW_WIDTH
from code.entity import Entity

class GuardaFlorestal(Entity):
    def __init__(self, pos_x: float, pos_y: float):
        super().__init__("GuardaFlorestal", pos_x, pos_y, folder_name="player")
        self.hp = PLAYER_HP
        self.speed = PLAYER_SPEED
        self.shot_cooldown = 0.0
        self.arrow_requested = False

        base_path = os.getcwd()
        audio_path = os.path.join(base_path, "asset", "audio", "Lança flecha.mp3")
        self.sound_arrow = pygame.mixer.Sound(audio_path)

    def move(self, dt: float):
        if self.current_action == "Dying":
            self.update_animation(dt)
            return

        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt

        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_SPACE] and self.current_action != "Shooting" and self.shot_cooldown <= 0:
            self.change_action("Shooting")
            self.shoot()
            self.arrow_requested = True
            self.shot_cooldown = 0.5

        if self.current_action == "Shooting":
            if self.current_frame == len(self.animations["Shooting"]) - 1:
                self.change_action("Walking")
            else:
                self.update_animation(dt)
            return

        if keys[pygame.K_LEFT]:
            self.pos_x -= self.speed * dt
            moving = True
        if keys[pygame.K_RIGHT]:
            self.pos_x += self.speed * dt
            moving = True
        if keys[pygame.K_UP]:
            self.pos_y -= self.speed * dt
            moving = True
        if keys[pygame.K_DOWN]:
            self.pos_y += self.speed * dt
            moving = True

        self.pos_x = max(0, min(self.pos_x, WINDOW_WIDTH - self.rect.width))
        self.pos_y = max(0, min(self.pos_y, WINDOW_HEIGHT - self.rect.height))

        if moving:
            self.change_action("Walking")
        elif self.current_action == "Walking":
            self.current_frame = 0
            if self.animations["Walking"]:
                self.surf = self.animations["Walking"][0]

        self.update_animation(dt)

    def shoot(self):
        self.sound_arrow.play()

