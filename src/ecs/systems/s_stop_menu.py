
import pygame
import esper
import time
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_menu import CTagMenu

def system_stop_menu(world:esper.World):
    components = world.get_components(CTransform, CTagMenu, CVelocity)
    for _, (c_t, c_m, c_v) in components:
        if (c_t.pos - c_m.final_pos).magnitude() < 3 and c_v.vel.magnitude != 0:
            c_v.vel = pygame.Vector2(0,0)
