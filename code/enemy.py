#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.entity import Entity

class Enemy(Entity):
    def __init__(self, name: str, pos_x: float, pos_y: float, hp: int, speed: float, damage: int, folder_name: str):
        super().__init__(name, pos_x, pos_y, folder_name)
        self.hp = hp
        self.speed = speed
        self.damage = damage

    def move(self, dt: float):
        if self.current_action == "Dying":
            self.update_animation(dt)
            return

        self.pos_x -= self.speed * dt
        self.update_animation(dt)


