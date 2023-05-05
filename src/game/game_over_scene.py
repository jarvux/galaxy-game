import pygame

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand

class GameOverScene(Scene):
    
    def do_create(self):
        create_text(self.ecs_world, "GAME OVER", 16, 
                    pygame.Color(255, 0, 0), pygame.Vector2(320, 150), TextAlignment.CENTER)
        create_text(self.ecs_world, "PRESS Z TO TRY AGAIN", 11, 
                    pygame.Color(255, 255, 0), pygame.Vector2(320, 210), TextAlignment.CENTER)        
        create_text(self.ecs_world, "PRESS ESC TO GO TO THE MAIN MENU", 11, 
                    pygame.Color(255, 255, 0), pygame.Vector2(320, 240), TextAlignment.CENTER)        
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("RETRY_GAME", pygame.K_z))
        quit_to_menu_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(quit_to_menu_action,
                                     CInputCommand("QUIT_TO_MENU", pygame.K_ESCAPE))
        
    def do_action(self, action: CInputCommand):
        if action.name == "RETRY_GAME":
            self.switch_scene("LEVEL_01")
        if action.name == "QUIT_TO_MENU":
            self.switch_scene("MENU_SCENE")
        
