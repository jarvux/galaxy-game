import pygame

import esper
import random

from src.create.prefab_creator import create_enemy_bullet
from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState, HunterState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator


def system_enemy_hunter_random(world: esper.World, player_entity: int, hunter_info: dict, bullet_info: dict):
    components = world.get_components(CEnemyHunterState, CAnimation, CTransform, CVelocity, CTagEnemy)
    rand_value = random.randint(-6, 2)
    if (get_enemy_running(components) < rand_value) and len(components) > 0:
        random_index = random.randint(0, len(components) - 1)
        _, (c_st, c_a, c_t, c_v, c_e) = components[random_index]
        c_st.state = HunterState.PREPARE_CHASE
        c_st.start_rot_pos = c_t.pos
        ServiceLocator.sounds_service.play(hunter_info[str(c_e.enemy_type)]["sound_chanse"])
        set_animation(c_a, "MOVE")
        t = pygame.Vector2(20,20)
        create_enemy_bullet(world, c_t.pos, t, bullet_info)


def get_enemy_running(components: list):
    cant = 0
    for _, (c_st, c_a, c_t, c_v, c_e) in components:
        if c_st.state == HunterState.CHASE or c_st.state == HunterState.RETURN or c_st.state == HunterState.PREPARE_CHASE:
            cant += 1

    return cant
