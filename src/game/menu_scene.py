import pygame
from src.create.prefab_creator import create_background
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_screen_background import system_screen_background

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text, create_text_dinamic
from src.ecs.components.c_input_command import CInputCommand 

class MenuScene(Scene):
    def __init__(self,engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)

    def do_create(self):
         
        create_text(self.ecs_world, "PRESS Z TO START GAME", 11, 
                    pygame.Color(255, 255, 0), pygame.Vector2(320, 210), TextAlignment.CENTER)
        create_text(self.ecs_world, "Arrows to MOVE - P to PAUSE", 8, 
                    pygame.Color(150, 150, 255), pygame.Vector2(320, 250), TextAlignment.CENTER)
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
    def do_update(self, delta_time: float):
        system_movement(self.ecs_world, delta_time)
        system_animation(self.ecs_world, delta_time)
        create_text_dinamic(self.ecs_world, "MAIN MENU", 16, 
                    pygame.Color(50, 255, 50), TextAlignment.CENTER,self.screen)
        system_screen_background(self.ecs_world, self.screen)
        self.ecs_world._clear_dead_entities()
        create_background(self.ecs_world,self.screen)

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")
   

        
