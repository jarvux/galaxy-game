import math
import random
import pygame
import esper

from src.create.prefab_creator import create_sprite
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.tags.c_tag_ball import CTagBall
from src.ecs.components.tags.c_tag_block import CTagBlock
from src.ecs.components.tags.c_tag_paddle import CTagPaddle
from src.engine.service_locator import ServiceLocator

def create_paddle(world:esper.World, paddle_cfg:dict, player_start_cfg:dict):
    surf = ServiceLocator.images_service.get(paddle_cfg["image"])
    pos = pygame.Vector2(player_start_cfg["pos"]["x"], player_start_cfg["pos"]["y"])
    vel = pygame.Vector2(0,0)
    paddle_ent = create_sprite(world, pos, vel, surf)
    world.add_component(paddle_ent, CTagPaddle())    
    return paddle_ent

def create_ball(world:esper.World, ball_cfg:dict, ball_start_cfg:pygame.Vector2) -> int:
    surf = ServiceLocator.images_service.get(ball_cfg["image"])
    pos = pygame.Vector2(ball_start_cfg["pos"]["x"], ball_start_cfg["pos"]["y"])
    vel = pygame.Vector2(0,0)
    start_speed = ball_cfg["velocity"]
    random_angle = (math.pi + (math.pi * 0.25)) + (random.random() * math.pi / 2)
    random_angle = math.pi/2
    vel.x = start_speed*math.cos(random_angle)
    vel.y = start_speed*math.sin(random_angle)

    ball_ent = create_sprite(world, pos, vel, surf)
    world.add_component(ball_ent, CTagBall())    
    return ball_ent

def create_play_field(world:esper.World, blocks_field:dict, block_types:dict):
    for element in blocks_field:
        b_type = element["type"]
        pos = pygame.Vector2(element["pos"]["x"], 
                             element["pos"]["y"])
        create_block(world, b_type, block_types[b_type], pos)

def create_block(world:esper.World, type:str, block_info:dict, pos:pygame.Vector2):
    surf = ServiceLocator.images_service.get(block_info["image"])
    block_ent = create_sprite(world, pos, None, surf)
    world.add_component(block_ent, CTagBlock(type))

def create_game_input(world:esper.World):
    quit_to_menu_action = world.create_entity()
    world.add_component(quit_to_menu_action,
                        CInputCommand("QUIT_TO_MENU", 
                                      pygame.K_ESCAPE))
    left_action = world.create_entity()
    world.add_component(left_action,
                        CInputCommand("LEFT", 
                                      pygame.K_LEFT))
    right_action = world.create_entity()
    world.add_component(right_action,
                        CInputCommand("RIGHT", 
                                      pygame.K_RIGHT))
    
    pause_action = world.create_entity()
    world.add_component(pause_action,
                        CInputCommand("PAUSE", 
                                      pygame.K_p))
    