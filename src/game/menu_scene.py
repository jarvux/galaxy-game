import json
import pygame

from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_screen_background import system_screen_background
from src.ecs.systems.s_stop_menu import system_stop_menu
from src.ecs.systems.s_surface_blink import system_surface_blink

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import  create_menu
from src.ecs.components.c_input_command import CInputCommand
from src.engine.service_locator import ServiceLocator 

class MenuScene(Scene):
    def __init__(self,engine:'src.engine.game_engine.GameEngine') -> None:
        self._load_config_files()
        super().__init__(engine)

    def _load_config_files(self):
        self.menu_cfg = ServiceLocator.configs_service.get("assets/cfg/menu.json")

    def do_create(self):
        create_menu(self.ecs_world, self.menu_cfg, self.screen)
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
    def do_update(self, delta_time: float):
        system_movement(self.ecs_world, delta_time)
        system_animation(self.ecs_world, delta_time)

        system_screen_background(self.ecs_world, self.screen)
        system_surface_blink(self.ecs_world)

        system_stop_menu(self.ecs_world)
        self.ecs_world._clear_dead_entities()

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")
   