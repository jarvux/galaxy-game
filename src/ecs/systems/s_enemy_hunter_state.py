import math
import pygame
import esper	
from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_enemy_spawner import CEnemySpawner	
from src.ecs.components.c_velocity import CVelocity	
from src.ecs.components.c_transform import CTransform	
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState, HunterState	
from src.engine.service_locator import ServiceLocator	
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_hunter_state(world: esper.World, player_entity: int, hunter_info: dict):	
    pl_t = world.component_for_entity(player_entity, CTransform)	
    components = world.get_components(CEnemyHunterState, CAnimation, CTransform, CVelocity, CTagEnemy)
    spawer = world.get_component(CEnemySpawner)
    for _, (c_st, c_a, c_t, c_v,c_te) in components:	
        for _, (c_e_s) in spawer:	
            if c_st.state == HunterState.IDLE:	
                _do_enemy_hunter_idle(c_st, c_a, c_t, c_v, pl_t, hunter_info[str(c_te.enemy_type)], c_e_s)	
            elif c_st.state == HunterState.PREPARE_CHASE:	
                _do_enemy_hunter_prepare_chase(c_st, c_a, c_t, c_v, hunter_info[str(c_te.enemy_type)])	
            elif c_st.state == HunterState.CHASE:	
                _do_enemy_hunter_chase(c_st, c_a, c_t, c_v, pl_t, hunter_info[str(c_te.enemy_type)])	
            elif c_st.state == HunterState.RETURN:	
                _do_enemy_hunter_return(c_st, c_a, c_t, c_v, hunter_info[str(c_te.enemy_type)])	
            elif c_st.state == HunterState.RETURN_HOME:	
                _do_enemy_hunter_return_home(c_st, c_a, c_t, c_v, hunter_info[str(c_te.enemy_type)],c_e_s)	


def _do_enemy_hunter_idle(c_st: CEnemyHunterState, c_a: CAnimation, c_t: CTransform,	
                          c_v: CVelocity, pl_t: CTransform, hunter_info: dict, c_e_s: CEnemySpawner):	
    set_animation(c_a, "IDLE")	
    dist_to_player = c_t.pos.distance_to(pl_t.pos)	
    c_v.vel = pygame.Vector2(c_e_s.ref_velocity,0)

def _do_enemy_hunter_prepare_chase(c_st: CEnemyHunterState, c_a: CAnimation, c_t: CTransform,	
                          c_v: CVelocity, pl_t: CTransform):	
    set_animation(c_a, "IDLE")	
    c_st.angle -= math.pi / 60
    c_t.pos.x = math.sin(c_st.angle) + c_st.start_rot_pos.x
    c_t.pos.y = math.cos(c_st.angle) + c_st.start_rot_pos.y
    if c_st.angle  < math.pi / 60:	
        c_st.state = HunterState.CHASE	

def _do_enemy_hunter_chase(c_st: CEnemyHunterState, c_a: CAnimation, c_t: CTransform,	
                           c_v: CVelocity, pl_t: CTransform, hunter_info: dict):	
    set_animation(c_a, "MOVE")	
    c_v.vel = (pl_t.pos - c_t.pos).normalize() * hunter_info["velocity_chase"]	
    dist_to_origin = c_st.start_pos.distance_to(c_t.pos)	
    if dist_to_origin >= hunter_info["distance_start_return"]:	
        c_v.vel = pygame.Vector2(0,hunter_info["velocity_chase"])
        c_st.state = HunterState.RETURN	

def _do_enemy_hunter_return(c_st: CEnemyHunterState, c_a: CAnimation,	
                            c_t: CTransform, c_v: CVelocity, hunter_info: dict):	
    set_animation(c_a, "MOVE")	
    dist_to_origin = c_st.start_pos.distance_to(c_t.pos)	
    if dist_to_origin <= 2:
        c_t.pos.xy += c_st.start_pos.xy	
        c_st.angle = math.pi 
        c_st.state = HunterState.RETURN_HOME	


def _do_enemy_hunter_return_home(c_st: CEnemyHunterState, c_a: CAnimation,	
                            c_t: CTransform, c_v: CVelocity, hunter_info: dict, c_e_s: CEnemySpawner):	
    set_animation(c_a, "MOVE")	
    diff = (c_st.start_pos+pygame.Vector2(c_e_s.ref_distance,0)-c_t.pos)
    c_v.vel = (diff).normalize() * hunter_info["velocity_return"]
    dist_to_origin = c_t.pos.distance_to(c_st.start_pos+pygame.Vector2(c_e_s.ref_distance,0))	
    if dist_to_origin <= 2:	
        c_t.pos = c_st.start_pos+pygame.Vector2(c_e_s.ref_distance,0)
        c_v.vel = pygame.Vector2(c_e_s.ref_velocity, 0)
        c_st.state = HunterState.IDLE	
    