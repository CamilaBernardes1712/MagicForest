#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import random
import pygame

from code.background import ParallaxBackground
from code.config import (
    ARROW_SPEED,
    CRYSTAL_MAX_TIME,
    CRYSTAL_MIN_TIME,
    GOLEM_ATTACK_COOLDOWN,
    GOLEM_ATTACK_RANGE,
    FPS,
    GOLEM_KING_HP,
    GOLEM_MAX_TIME,
    GOLEM_MIN_TIME,
    MAX_CRYSTALS,
    SCROLL_SPEED,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from code.entityFactory import EntityFactory

class Level:
    def __init__(self, window, name="Magic Forest", menu_option=None):
        self.window = window
        self.name = name
        self.menu_option = menu_option
        self.background = ParallaxBackground(window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT)
        self.entity_list = []
        self.arrows_list = []
        self.crystal_count = 0

        pygame.font.init()
        self.font = pygame.font.SysFont("Verdana", 24)
        self.victory_font = pygame.font.SysFont("Verdana", 60, bold=True)

        self.golem_king_spawned = False
        self.boss_warning_text = ""
        self.boss_warning_timer = 0.0
        self.game_over_victory = False
        self.victory_timer = 0.0
        self.enemy_spawn_timer = GOLEM_MIN_TIME
        self.golem_rei_instancia = None

        pygame.mixer.init()
        base_path = os.getcwd()
        audio_dir = os.path.join(base_path, "asset", "audio")
        pygame.mixer.music.load(os.path.join(audio_dir, "Som de fundo.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.sound_crystal = pygame.mixer.Sound(os.path.join(audio_dir, "Pegando Cristal.mp3"))

        self.crystal_spawn_timer = CRYSTAL_MIN_TIME
        self.current_crystal_rect = None
        self.current_crystal_surf = None
        self.crystal_images = []

        items_dir = os.path.join(base_path, "asset", "images", "items")
        for i in range(1, 6):
            path_crystal = os.path.join(items_dir, f"{i}.png")
            try:
                img = pygame.image.load(path_crystal).convert_alpha()
                img = pygame.transform.scale(img, (60, 75))
                self.crystal_images.append(img)
            except pygame.error:
                pass

        if len(self.crystal_images) == 0:
            fallback = pygame.Surface((40, 50))
            fallback.fill((0, 255, 255))
            self.crystal_images.append(fallback)

        self.spawn_initial_entities()

    def spawn_initial_entities(self):
        player = EntityFactory.create_entity("guarda_florestal", pos_x=100.0, pos_y=430.0)
        self.entity_list.append(player)

        golem_positions = [1300.0, 1450.0, 1600.0, 1750.0]
        for pos_x in golem_positions:
            golem = EntityFactory.create_entity("golem", pos_x=pos_x, pos_y=460.0)
            self.entity_list.append(golem)

    def spawn_new_crystal(self):
        random_x = random.randint(300, 1100)
        random_y = random.randint(530, 580)
        self.current_crystal_surf = random.choice(self.crystal_images)
        self.current_crystal_rect = self.current_crystal_surf.get_rect(topleft=(random_x, random_y))

    def create_player_arrow(self, player):
        arrow_rect = pygame.Rect(player.pos_x + 90, player.pos_y + 55, 30, 6)
        self.arrows_list.append(arrow_rect)

    def draw_boss_life_bar(self):
        if not (self.golem_king_spawned and self.golem_rei_instancia in self.entity_list):
            return

        bar_width = 320
        bar_height = 18
        bar_x = 285
        bar_y = 22
        vida_proporcao = max(0, self.golem_rei_instancia.hp) / GOLEM_KING_HP
        largura_atual = int(bar_width * vida_proporcao)

        txt_boss = self.font.render("Rei Golem", True, (255, 230, 120))
        self.window.blit(txt_boss, (bar_x, 48))
        pygame.draw.rect(self.window, (75, 20, 20), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.window, (210, 40, 40), (bar_x, bar_y, largura_atual, bar_height))
        pygame.draw.rect(self.window, (255, 230, 120), (bar_x, bar_y, bar_width, bar_height), 2)

    def update_enemy_attack(self, enemy, player, dt):
        if enemy.current_action == "Dying" or not player:
            return False

        enemy_rect = enemy.rect
        player_rect = player.rect
        perto_do_guarda = (
            enemy_rect
            and player_rect
            and abs(enemy_rect.centerx - player_rect.centerx) <= GOLEM_ATTACK_RANGE
            and abs(enemy_rect.centery - player_rect.centery) <= 90
        )

        if not perto_do_guarda:
            if enemy.current_action == "Slashing":
                enemy.change_action("Walking")
            return False

        enemy.change_action("Slashing")
        enemy.update_animation(dt)

        if not hasattr(enemy, "attack_cooldown"):
            enemy.attack_cooldown = 0.0

        enemy.attack_cooldown -= dt
        if enemy.attack_cooldown <= 0:
            player.hp = max(0, player.hp - enemy.damage)
            enemy.attack_cooldown = GOLEM_ATTACK_COOLDOWN

        return True

    def run(self):
        clock = pygame.time.Clock()
        playing = True

        while playing:
            dt = clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    playing = False

            player = self.entity_list[0] if self.entity_list else None

            if self.game_over_victory:
                self.victory_timer -= dt
                if self.victory_timer <= 0:
                    pygame.mixer.music.stop()
                    playing = False

                self.window.fill((0, 0, 0))
                self.background.draw(self.window)
                for entity in self.entity_list:
                    entity.draw(self.window)
                txt_vitoria = self.victory_font.render("Parabéns! Você venceu!", True, (0, 255, 0))
                pos_x = (WINDOW_WIDTH - txt_vitoria.get_width()) // 2
                pos_y = (WINDOW_HEIGHT - txt_vitoria.get_height()) // 2
                self.window.blit(txt_vitoria, (pos_x, pos_y))
                pygame.display.flip()
                continue

            golems_vivos = len(self.entity_list) - 1 if not self.golem_king_spawned else 0
            if not self.golem_king_spawned:
                self.enemy_spawn_timer -= dt
                if self.enemy_spawn_timer <= 0 or golems_vivos < 3:
                    novo_golem = EntityFactory.create_entity("golem", pos_x=1350.0, pos_y=460.0)
                    self.entity_list.append(novo_golem)
                    self.enemy_spawn_timer = random.uniform(GOLEM_MIN_TIME, GOLEM_MAX_TIME)

            if self.crystal_count >= MAX_CRYSTALS and not self.golem_king_spawned:
                golem_rei = EntityFactory.create_entity("golem_maior", pos_x=1400.0, pos_y=420.0)
                self.entity_list.append(golem_rei)
                self.golem_rei_instancia = golem_rei
                self.golem_king_spawned = True
                self.boss_warning_text = "Cuidado! O Rei Golem está vindo!"
                self.boss_warning_timer = 4.0

            if self.boss_warning_timer > 0:
                self.boss_warning_timer -= dt
                if self.boss_warning_timer <= 0:
                    self.boss_warning_text = ""

            if self.current_crystal_rect is None and self.crystal_count < MAX_CRYSTALS:
                self.crystal_spawn_timer -= dt
                if self.crystal_spawn_timer <= 0:
                    self.spawn_new_crystal()
                    self.crystal_spawn_timer = random.uniform(CRYSTAL_MIN_TIME, CRYSTAL_MAX_TIME)

            self.background.update(player_speed=SCROLL_SPEED, dt=dt)

            if self.current_crystal_rect and player and player.current_action == "Walking" and pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.current_crystal_rect.x -= int(SCROLL_SPEED * dt)

            if player and getattr(player, "arrow_requested", False):
                self.create_player_arrow(player)
                player.arrow_requested = False

            for arrow in self.arrows_list[:]:
                arrow.x += int(ARROW_SPEED * dt)
                if arrow.x > WINDOW_WIDTH:
                    self.arrows_list.remove(arrow)

            for entity in self.entity_list:
                if entity is not player and entity.name == "Golem" and self.update_enemy_attack(entity, player, dt):
                    pass
                else:
                    entity.move(dt)
                entity.pos_x = max(0, min(entity.pos_x, WINDOW_WIDTH - entity.rect.width))
                entity.pos_y = max(0, min(entity.pos_y, WINDOW_HEIGHT - entity.rect.height))
                entity.rect.topleft = (int(entity.pos_x), int(entity.pos_y))

            for arrow in self.arrows_list[:]:
                for enemy in self.entity_list[1:]:
                    if enemy.current_action != "Dying" and enemy.rect and enemy.rect.colliderect(arrow):
                        if arrow in self.arrows_list:
                            self.arrows_list.remove(arrow)
                        enemy.hp -= 5
                        if enemy.hp <= 0:
                            enemy.change_action("Dying")
                        break

            for enemy in self.entity_list[1:]:
                if enemy.current_action == "Dying" and enemy.current_frame == len(enemy.animations["Dying"]) - 1:
                    if enemy.name == "GolemMaior":
                        self.game_over_victory = True
                        self.victory_timer = 5.0
                    self.entity_list.remove(enemy)

            if player and self.current_crystal_rect and player.rect and player.rect.colliderect(self.current_crystal_rect):
                self.sound_crystal.play()
                self.crystal_count += 1
                self.current_crystal_rect = None
                self.current_crystal_surf = None

            self.window.fill((0, 0, 0))
            self.background.draw(self.window)

            if self.current_crystal_rect and self.current_crystal_surf:
                self.window.blit(self.current_crystal_surf, self.current_crystal_rect)

            for arrow in self.arrows_list:
                pygame.draw.rect(self.window, (255, 215, 0), arrow)

            for entity in self.entity_list:
                entity.draw(self.window)

            if self.crystal_images:
                hud_icon = pygame.transform.scale(self.crystal_images[0], (25, 32))
                self.window.blit(hud_icon, (20, 15))

            txt_cristais = self.font.render(f"Cristais: {self.crystal_count}/{MAX_CRYSTALS}", True, (255, 255, 0))
            self.window.blit(txt_cristais, (55, 18))
            self.draw_boss_life_bar()

            fps = int(clock.get_fps())
            texto_fps = self.font.render(f"FPS: {fps}", True, (255, 255, 255))
            self.window.blit(texto_fps, (10, 680))

            if self.boss_warning_text != "":
                txt_aviso = self.font.render(self.boss_warning_text, True, (255, 0, 0))
                pos_x_centro = (WINDOW_WIDTH - txt_aviso.get_width()) // 2
                self.window.blit(txt_aviso, (pos_x_centro, 640))

            pygame.display.flip()

