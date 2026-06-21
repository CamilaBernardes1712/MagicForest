#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame

class ParallaxBackground:
    def __init__(self, window_width=1280, window_height=720):
        display = pygame.display.get_surface()
        if display:
            self.window_width, self.window_height = display.get_size()
        else:
            self.window_width = window_width
            self.window_height = window_height

        base_path = os.getcwd()
        bg_dir = os.path.join(base_path, "asset", "images", "background")
        self.layers_config = [
            ("game_background_1.png", 0.1),
            ("back_land.png", 0.3),
            ("back_decor.png", 0.5),
            ("battleground.png", 0.7),
            ("ground_decor.png", 0.9),
            ("front_decor.png", 1.2),
        ]
        self.layers = []

        for file_name, speed_factor in self.layers_config:
            path = os.path.join(bg_dir, file_name)
            if os.path.exists(path):
                raw_img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(raw_img, (self.window_width, self.window_height))
                self.layers.append({"surf": img, "x": 0.0, "speed_factor": speed_factor})

    def update(self, player_speed, dt):
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            for layer in self.layers:
                layer["x"] -= player_speed * layer["speed_factor"] * dt
                image_width = layer["surf"].get_width()
                if layer["x"] <= -image_width:
                    layer["x"] += image_width

    def draw(self, window):
        window_width, window_height = window.get_size()
        for layer in self.layers:
            image_width = layer["surf"].get_width()
            x = int(layer["x"])
            window.blit(layer["surf"], (x, 0), area=pygame.Rect(0, 0, window_width, window_height))
            window.blit(layer["surf"], (x + image_width, 0), area=pygame.Rect(0, 0, window_width, window_height))


