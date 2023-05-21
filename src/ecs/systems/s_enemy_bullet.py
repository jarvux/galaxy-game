import pygame

import esper
from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet


def system_enemy_bullet(world: esper.World):
    bullet_enemy_components = world.get_components(CTransform, CBulletState, CVelocity, CTagEnemyBullet)
    for _, (c_t, c_bt, c_v, c_te) in bullet_enemy_components:
        c_t.pos.y += 1
