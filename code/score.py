#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from code.DBProxy import DBProxy

class Score:
    def __init__(self, db_name: str = "magicforest.db"):
        self.db = DBProxy(db_name)

    def calculate(self, crystals: int, defeated_golems: int, player_hp: int, victory: bool) -> int:
        score = 0
        score += crystals * 100
        score += defeated_golems * 50
        score += max(0, player_hp) * 2

        if victory:
            score += 1000

        return score

    def save(self, player_name: str, crystals: int, defeated_golems: int, player_hp: int, victory: bool):
        score_value = self.calculate(crystals, defeated_golems, player_hp, victory)
        self.db.save(
            {
                "name": player_name,
                "score": score_value,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
        )
        return score_value

    def top10(self):
        return self.db.retrieve_top10()

    def close(self):
        self.db.close()
