#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.entity import Entity

class Arrow(Entity):
    def __init__(self, pos_x: float, pos_y: float):
        super().__init__("Arrow", pos_x, pos_y)
        self.speed = 300.0
        self.direction = 1

    def move(self, dt: float):
        # Movimentação para frente
        self.pos_x += self.speed * self.direction * dt
