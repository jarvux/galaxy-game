import pygame
import esper
from src.create.prefab_creator import create_enemy_spawner, update_level

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_enemies_count(world: esper.World, level_data: dict, enemies_data: dict, screen: pygame.Surface, level_entity: int):
    components = world.get_components(CTagEnemy)
    if len(components) == 0:
        update_level(world, level_entity)
        create_enemy_spawner(world, level_data, enemies_data, screen)

