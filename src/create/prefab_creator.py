from enum import Enum
import json
import random
import pygame
import esper
from src.ecs.components.c_bullet_state import CBulletState

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text import CText
from src.ecs.components.c_text_key import CTextText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_background import CTagBackground
from src.ecs.components.tags.c_tag_blink import CTagBlink
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_header import CTagHeader
from src.ecs.components.tags.c_tag_key import CTagKey
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_text import CTagText
from src.engine.service_locator import ServiceLocator


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    return sprite_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CTagEnemy("Bouncer"))
    ServiceLocator.sounds_service.play(enemy_info["sound"])

def create_background(world: esper.World, screen:pygame.Surface, fromAxisX =  False):
    surface = screen.get_rect()
    start = pygame.Surface((1, 1))
    if fromAxisX :
        y=0
    else:
        y=random.randrange(0,surface.width)
    x=random.randrange(0,surface.width)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    start.fill((r,g,b))
    pos = pygame.Vector2(x,y)
    vel_range = random.randrange(int(surface.height/8), int(surface.height/4))
    velocity = pygame.Vector2(0, vel_range)
    background_entity = create_sprite(world, pos, velocity, start)
    world.add_component(background_entity, CTagBackground())
    blink = random.uniform(0.3, 0.5)
    world.add_component(background_entity, CTagBlink(blink))
    
    
def create_enemy_hunter(world: esper.World, pos: pygame.Vector2, enemy_info: dict, enemy_type: str):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    velocity = pygame.Vector2(enemy_info["velocity_waiting"]["x"], enemy_info["velocity_waiting"]["y"])
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CEnemyHunterState(pos, enemy_info["score"]))
    world.add_component(enemy_entity,
                        CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CTagEnemy(enemy_type))


def create_player_square(world: esper.World, player_info: dict, screen: pygame.Surface) -> int:
    player_sprite = ServiceLocator.images_service.get(player_info["image"])
    #player_sprite = pygame.transform.scale_by(player_sprite, player_info["scale"])
    surface = screen.get_rect()
    size = player_sprite.get_size()
    size = (size[0] / player_info["animations"]["number_frames"], size[1])

    pos = pygame.Vector2(surface.centerx,
                         surface.bottom)
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player_sprite)
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity,
                        CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState(player_info["num_lives"]))
    return player_entity


def create_enemy_spawner(world: esper.World, level_data: dict, enemies_data: dict, screen: pygame.Surface):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(level_data,enemies_data, screen))


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_p = world.create_entity()
    input_z = world.create_entity()
    world.add_component(input_left,
                        CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right,
                        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))

    world.add_component(input_p,
                        CInputCommand("P_DOWN", pygame.K_p))
    world.add_component(input_z,
                        CInputCommand("PLAYER_FIRE", pygame.K_z))


def create_player_bullet(world: esper.World,
                  player_pos: pygame.Vector2,
                  player_size: pygame.Vector2,
                  bullet_info: dict):
    bullet_size = pygame.Vector2(bullet_info["width"], bullet_info["height"])
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_info["width"] / 2),
                         player_pos.y - bullet_info["height"])
    vel = pygame.Vector2(0,0)
    col = pygame.Color(bullet_info["color"]["r"],bullet_info["color"]["g"],bullet_info["color"]["b"])
    bullet_entity = create_square(world,bullet_size, pos, vel, col)
    world.add_component(bullet_entity, CTagBullet())
    world.add_component(bullet_entity, CBulletState())


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):

    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    scale = 1 if explosion_info.get("scale") is None else explosion_info["scale"]
    explosion_surface = pygame.transform.scale_by(explosion_surface, scale)
    vel = pygame.Vector2(0, 0)
    pos = pygame.Vector2(pos[0], pos[1] )
    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity,
                        CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(explosion_info["sound"])
    return explosion_entity


def create_interface(world: esper.World, interfaceinfo: dict, pos: dict):
    source = pygame.font.Font(interfaceinfo["source"], interfaceinfo["size"])
    text = source.render(interfaceinfo["text"], 0,
                         (interfaceinfo["color"]["r"], interfaceinfo["color"]["g"], interfaceinfo["color"]["b"]))
    sprite_entity = world.create_entity()
    pos = pygame.Vector2(pos[0] - text.get_width() // 2, pos[1] - text.get_height() // 2)
    world.add_component(sprite_entity,
                        CText(pos, text))
    return sprite_entity


def create_key_text(world: esper.World, interface_config_info: dict, key: str):
    interface_info = interface_config_info[key]
    sz: int = interface_info["size"]
    path = interface_info["font"]
    font = ServiceLocator.fonts_service.get(path, sz)
    color = (interface_info["color"]["r"],
             interface_info["color"]["g"],
             interface_info["color"]["b"])
    interface_surface = font.render(interface_info["text"], False, color)
    pos = interface_info["position"]
    p = pygame.Vector2(pos["x"], pos["y"])
    velocity = interface_info.get("velocity")
    vel = pygame.Vector2(0, 0) if velocity is None else pygame.Vector2(velocity["x"], velocity["y"])

    entity = create_sprite(world, p, vel, interface_surface)
    world.add_component(entity, CTagText())
    return entity


def update_score(world: esper.World, score: int, score_entity:int):
    txt_s = world.component_for_entity(score_entity, CSurface)
    txt_t = world.component_for_entity(score_entity, CText)
    new_score = int(txt_t.text) + score
    txt_t.text = str(new_score)
    txt_s.update_text(str(new_score))
    return new_score

def update_hi_score(world: esper.World, new_score: int, hi_score_entity:int):
    txt_t = world.component_for_entity(hi_score_entity, CText)
    if new_score > int(txt_t.text):
        txt_s = world.component_for_entity(hi_score_entity, CSurface)
        txt_t.text = str(new_score)
        txt_s.update_text(str(new_score))
        
        # Writing new scores in the files
        interface_info = ServiceLocator.configs_service.get("assets/cfg/interface.json")
        menu_info = ServiceLocator.configs_service.get("assets/cfg/menu.json")
        interface_info["hi-score"]["text"]=str(new_score)
        menu_info["line2center"]["text"]=str(new_score)

        with open("assets/cfg/interface.json", "w") as write_file:
            json.dump(interface_info, write_file)
        with open("assets/cfg/menu.json", "w") as write_file:
            json.dump(menu_info, write_file)

        ServiceLocator.configs_service.update("assets/cfg/interface.json", interface_info)
        ServiceLocator.configs_service.update("assets/cfg/menu.json", menu_info)
        
        return new_score
    
def update_level(world: esper.World, level_entity: int):
    txt_s = world.component_for_entity(level_entity, CSurface)
    txt_t = world.component_for_entity(level_entity, CText)
    new_level = int(txt_t.text) + 1
    txt_t.text = str(new_level)
    txt_s.update_text(str(new_level).zfill(2))

def update_lives(world: esper.World, num_life: int):
        components = world.get_components(CTagKey, CTagHeader)
        for entity, (c_k, _) in components:
            if c_k.key == ('live-0' + (str(num_life))):
                world.delete_entity(entity)
            
