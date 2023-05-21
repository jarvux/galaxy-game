import pygame

import esper
from src.create.prefab_creator import create_player_bullet
from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_player_bullet(world: esper.World, player_pos: pygame.Vector2, player_area: pygame.Vector2,
                         bullet_info: dict):
    components = world.get_components(CTransform, CBulletState, CVelocity, CTagBullet)
    if len(components) == 0:
        create_player_bullet(world, player_pos, player_area, bullet_info)
    else:
        for bullet_entity, (c_t, c_s, c_v, _) in components:
            if c_v.vel.magnitude() == 0:
                c_t.pos = pygame.Vector2(player_pos.x + (player_area[0] / 2) - (bullet_info["width"] / 2),
                                         player_pos.y - bullet_info["height"])
