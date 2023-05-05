import esper
import pygame
import random
from src.create.prefab_creator import create_background
from src.ecs.components.c_enemy_spawner import CEnemySpawner, SpawnEventData
from src.ecs.components.tags.c_tag_background import CTagBackground

def system_background_spawner(world: esper.World, background_info: dict, screen:pygame.Surface):
    components = world.get_component(CTagBackground)
    scr_rect = screen.get_rect()
    while len(components) < 100:
        components = world.get_component(CTagBackground)
        create_background(world,pygame.Vector2(
            random.choice([-screen.get_width(), scr_rect.width]),
            random.choice([-screen.get_height(), scr_rect.height])),background_info,screen)
        

  