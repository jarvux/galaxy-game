import pygame
from src.ecs.systems.s_movement_background import system_movement_background
from src.ecs.systems.s_screen_background import system_screen_background
from src.ecs.systems.s_surface_blink import system_surface_blink

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand
from src.engine.service_locator import ServiceLocator

class GameOverScene(Scene):
    
    def do_create(self):
        create_text(self.ecs_world, "game_over" ,self.screen, "GAME OVER", 10, "assets/fnt/PressStart2P.ttf",
                    pygame.Color(255, 0, 0), pygame.Vector2(0, 0), pygame.Vector2(0, 0), 0.5, 0.5)
        create_text(self.ecs_world, "game_over_instructions1", self.screen,"PRESS Z TO TRY AGAIN", 5, "assets/fnt/PressStart2P.ttf",
                    pygame.Color(255, 255, 0), pygame.Vector2(0, 0),pygame.Vector2(0, 0),0.5, 0.6)        
        create_text(self.ecs_world, "game_over_instructions1",self.screen, "PRESS ESC TO GO TO THE MAIN MENU", 5, "assets/fnt/PressStart2P.ttf",
                    pygame.Color(255, 255, 0), pygame.Vector2(0, 0),pygame.Vector2(0, 0) ,0.5, 0.7)        
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("RETRY_GAME", pygame.K_z))
        quit_to_menu_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(quit_to_menu_action,
                                     CInputCommand("QUIT_TO_MENU", pygame.K_ESCAPE))
        ServiceLocator.sounds_service.play('assets/snd/game_over.ogg')
        
    def do_action(self, action: CInputCommand):
        if action.name == "RETRY_GAME":
            self.switch_scene("MENU_SCENE")
        if action.name == "QUIT_TO_MENU":
            self.switch_scene("MENU_SCENE")
        
    def do_update(self, delta_time: float):
            
        system_screen_background(self.ecs_world, self.screen)
        system_movement_background(self.ecs_world, delta_time)

