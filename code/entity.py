#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import pygame
import os

class Entity(ABC):
    def __init__(self, name: str, pos_x: float, pos_y: float, folder_name: str):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = 0
        self.animations = {"Walking": [], "Dying": [], "Slashing": [], "Shooting": []}
        self.current_action = "Walking"
        self.current_frame = 0
        self.animation_speed = 12.0
        self.frame_timer = 0.0

        # Carrega todas as animações
        self.load_all_animations(folder_name)

        if self.animations[self.current_action]:
            self.surf = self.animations[self.current_action][self.current_frame]
            self.rect = self.surf.get_rect(left=int(pos_x), top=int(pos_y))
        else:
            self.surf = pygame.Surface((60, 60))
            self.surf.fill((255, 0, 0))
            self.rect = self.surf.get_rect(left=int(pos_x), top=int(pos_y))

    def load_all_animations(self, folder_name: str):
        base_path = os.getcwd()
        for action in self.animations.keys():
            dir_path = os.path.join(base_path, 'asset', 'images', folder_name, action)
            if os.path.exists(dir_path):
                for i in range(1, 31):
                    file_name = f"{i}.png"
                    full_path = os.path.join(dir_path, file_name)
                    if os.path.exists(full_path):
                        img = pygame.image.load(full_path).convert_alpha()
                        if self.name == "GolemMaior":
                            img = pygame.transform.scale(img, (160, 160))
                        else:
                            img = pygame.transform.scale(img, (120, 120))

                        if self.name == "Golem" or self.name == "GolemMaior":
                            img = pygame.transform.flip(img, True, False)

                        self.animations[action].append(img)

    def update_animation(self, dt: float):
        frames = self.animations[self.current_action]
        if len(frames) > 1:
            self.frame_timer += dt
            if self.frame_timer >= (1.0 / self.animation_speed):
                self.frame_timer = 0.0

                if self.current_action == "Dying" and self.current_frame == len(frames) - 1:
                    return

                self.current_frame = (self.current_frame + 1) % len(frames)
                self.surf = frames[self.current_frame]

    def change_action(self, new_action: str):
        if self.current_action != new_action:
            self.current_action = new_action
            self.current_frame = 0
            self.frame_timer = 0.0

            if new_action == "Dying":
                audio_path = os.path.join(os.getcwd(), 'asset', 'audio', 'Grito de dor.mp3')
                if os.path.exists(audio_path):
                    pygame.mixer.Sound(audio_path).play()

    @abstractmethod
    def move(self, dt: float):
        pass

    def draw(self, window: pygame.Surface):
        if self.surf and self.rect:
            # Sincroniza o tamanho do rect com o tamanho do sprite atual antes de desenhar
            self.rect.size = self.surf.get_size()
            self.rect.topleft = (int(self.pos_x), int(self.pos_y))
            window.blit(self.surf, self.rect)