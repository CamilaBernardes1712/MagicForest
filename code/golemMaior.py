#!/usr/bin/python
# -*- coding: utf-8 -*-

from Golem import Golem
from Enemy import Enemy


class GolemMaior(Golem, Enemy):
    def __init__(self):
        self.weapon = "Mini-espada"
        self.hp = 5
