import json
import time
import pygame
from src.create.prefab_creator import create_enemy_spawner, create_input_player, create_key_text, create_player_square
from src.create.prefab_creator_interface import create_menu
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_hunter_random import system_enemy_hunter_random
from src.ecs.systems.s_enemies_count import system_enemies_count
from src.ecs.systems.s_enemy_hunter_state import system_enemy_hunter_state
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_movement_background import system_movement_background
from src.ecs.systems.s_player_bullet import system_player_bullet
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_screen_background import system_screen_background
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_screen_return import system_screen_return_home
from src.ecs.systems.s_surface_blink import system_surface_blink
from src.ecs.systems.s_surface_blink_background import system_surface_blink_background

from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform 
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
import src.engine.game_engine
from src.engine.service_locator import ServiceLocator

class PlayScene(Scene):
    def __init__(self, level_path:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self.level_path = level_path
        self._load_config_files()
        self._paddle_ent = -1
        self._num_lives = self.player_cfg["num_lives"]

    def _load_config_files(self):
        self.window_cfg = ServiceLocator.configs_service.get("assets/cfg/window.json")
        self.enemies_cfg = ServiceLocator.configs_service.get("assets/cfg/enemies_2.json")
        self.level_01_cfg = ServiceLocator.configs_service.get(self.level_path)
        self.player_cfg = ServiceLocator.configs_service.get("assets/cfg/player.json")
        self.bullet_cfg = ServiceLocator.configs_service.get("assets/cfg/bullet.json")
        self.explosion_cfg = ServiceLocator.configs_service.get("assets/cfg/enemy_explosion.json")
        self.interface_cfg = ServiceLocator.configs_service.get("assets/cfg/interface.json")
        self.player_explosion_cfg = ServiceLocator.configs_service.get("assets/cfg/player_explosion.json")

    def do_create(self):
        self.wait = False
        self.start = True
        self._paused = False
        self._player_entity = create_player_square(self.ecs_world, self.player_cfg,self.screen)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)

        create_input_player(self.ecs_world)
        
        # Texts + images
        self.conttrol_items = create_menu(self.ecs_world, self.interface_cfg, self.screen)
        paused_text_ent = self.conttrol_items["pause"]
        self.p_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.p_txt_s.visible = self._paused
        
        # This is for start
        ServiceLocator.sounds_service.play(self.window_cfg["start"]["sound"])
        self.timestamp = time.time()

    
    def do_update(self, delta_time: float):
        
        system_screen_background(self.ecs_world, self.screen)
        system_surface_blink_background(self.ecs_world)

        if self.start or self.wait:
            diff = time.time() - self.timestamp

        if self.start and diff >= self.window_cfg["start"]["waiting_time"]:
            create_enemy_spawner(self.ecs_world, self.level_01_cfg, self.enemies_cfg, self.screen)
            self.start = False
            game_start = self.ecs_world.component_for_entity(self.conttrol_items["game_start"], CSurface)
            game_start.visible = False
        elif self.wait and diff >= 5:
            self.wait = False
        elif not self.start:
            if not self._paused:
                
                system_enemy_spawner(self.ecs_world, self.enemies_cfg,delta_time)
                system_movement(self.ecs_world, delta_time)
                system_player_bullet(self.ecs_world, self._player_c_t.pos, self._player_c_s.area.size, self.bullet_cfg)

                system_screen_bounce(self.ecs_world, self.screen)
                system_screen_player(self.ecs_world, self.screen)
                system_screen_bullet(self.ecs_world, self.screen)
            

                system_collision_enemy_bullet(self.ecs_world, self.explosion_cfg, self.conttrol_items["score"], self.conttrol_items["hi-score"])
                system_collision_player_enemy(self.ecs_world, self._player_entity, self.level_01_cfg, self.player_explosion_cfg,
                                            self.screen, self._num_lives, self)
                
                system_explosion_kill(self.ecs_world)
                system_player_state(self.ecs_world)
                #TODO: PILAS CREAR DIFERENTES ENEMIGOS
                system_enemy_hunter_random(self.ecs_world, self._player_entity, self.enemies_cfg)
                system_screen_return_home(self.ecs_world, self.screen)
                system_enemy_hunter_state(self.ecs_world, self._player_entity, self.enemies_cfg)

                system_animation(self.ecs_world, delta_time) 
            else:
                system_surface_blink(self.ecs_world)
                system_movement_background(self.ecs_world, delta_time)
            
            system_enemies_count(self.ecs_world,  self.level_01_cfg, self.enemies_cfg, self.screen, self.conttrol_items["level"])
        else:
            
            system_screen_player(self.ecs_world, self.screen)
            system_player_bullet(self.ecs_world, self._player_c_t.pos, self._player_c_s.area.size, self.bullet_cfg)
            system_movement(self.ecs_world, delta_time)

        self.ecs_world._clear_dead_entities()
        self.num_bullets = len(self.ecs_world.get_component(CTagBullet))

    def do_clean(self):
        self._paused = False

    def do_action(self, action: CInputCommand):
        if not self._paused:
            if action.name == "PLAYER_LEFT":
                if action.phase == CommandPhase.START:
                    self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
                elif action.phase == CommandPhase.END:
                    self._player_c_v.vel.x += self.player_cfg["input_velocity"]
            if action.name == "PLAYER_RIGHT":
                if action.phase == CommandPhase.START:
                    self._player_c_v.vel.x += self.player_cfg["input_velocity"]
                elif action.phase == CommandPhase.END:
                    self._player_c_v.vel.x -= self.player_cfg["input_velocity"]

        if action.name == "PLAYER_FIRE" and self.num_bullets <= self.level_01_cfg["player_spawn"]["max_bullets"] and action.phase == CommandPhase.START:
            components = self.ecs_world.get_components(CVelocity, CTagBullet)
            for bullet_entity, (c_v, _) in components:
                if c_v.vel.magnitude() == 0 :
                    c_v.vel = pygame.Vector2(0,-self.bullet_cfg["velocity"])
                    ServiceLocator.sounds_service.play(self.bullet_cfg["sound"])


        if action.name == "P_DOWN":
            if action.phase == CommandPhase.START:
                self._paused = not self._paused
                self.p_txt_s.visible = self._paused
                if self._paused:
                    ServiceLocator.sounds_service.play(self.window_cfg["pause"]["sound"])
                    
                    
