#!/usr/bin/python
# -*- coding: utf-8 -*-

from Entity import Entity


class Enemy(Entity):
    def __init__(self):
        self.hp = None
        self.speed = None
        self.damage = None

    def move(self, ):
        pass
