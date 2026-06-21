#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.golem import Golem
from code.golemMaior import GolemMaior
from code.guardaFlorestal import GuardaFlorestal

class EntityFactory:
    @staticmethod
    def create_entity(entity_type: str, pos_x: float, pos_y: float):
        type_lower = entity_type.lower()

        if type_lower == "golem":
            return Golem(pos_x, pos_y)

        elif type_lower == "golem_maior":
            return GolemMaior(pos_x, pos_y)

        elif type_lower == "guarda_florestal":
            return GuardaFlorestal(pos_x, pos_y)

        raise ValueError(f"A Fábrica não sabe como criar a entidade do tipo: '{entity_type}'")
