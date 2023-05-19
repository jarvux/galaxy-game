import pygame
import esper
from src.create.prefab_creator import create_background
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState, HunterState

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_background import CTagBackground
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
def system_screen_return_home(world: esper.World, screen: pygame.Surface):
    scr_rect = screen.get_rect()
    components = world.get_components(CTransform,CSurface,CEnemyHunterState,CTagEnemy)
    for enemy_entity, (c_t, c_s, c_st, c_e) in components:
        enemy_rect = CSurface.get_area_relative(c_s.area,c_t.pos)
        if not scr_rect.contains(enemy_rect):
           c_st.state = HunterState.RETURN_HOME
           c_t.pos.y = 0
        

