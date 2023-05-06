import random
import pygame
import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text import CText
from src.ecs.components.c_text_key import CTextText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_background import CTagBackground
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
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
    #Random color
    start.fill((255,255,255))
    if fromAxisX :
        y=0
    else:
        y=random.randrange(0,surface.width)
    x=random.randrange(0,surface.height)
    pos = pygame.Vector2(x,y)
    vel_range = random.randrange(0, surface.height)
    velocity = pygame.Vector2(0, vel_range)
    background_entity = create_sprite(world, pos, velocity, start)
    world.add_component(background_entity, CTagBackground())
    

    
def create_enemy_hunter(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    velocity = pygame.Vector2(0, 0)
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CEnemyHunterState(pos))
    world.add_component(enemy_entity,
                        CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CTagEnemy("Hunter"))


def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict, screen: pygame.Surface) -> int:
    player_sprite = ServiceLocator.images_service.get(player_info["image"])
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
    world.add_component(player_entity, CPlayerState())
    return player_entity


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))


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


def create_bullet(world: esper.World,
                  player_pos: pygame.Vector2,
                  player_size: pygame.Vector2,
                  bullet_info: dict):
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2),
                         player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    vel = ((player_pos.x, 0) - player_pos)
    vel = vel.normalize() * bullet_info["velocity"]
    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_info["sound"])


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    vel = pygame.Vector2(0, 0)

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


def create_text_sebas(world: esper.World, text: str, pos: dict):
    green = (0, 255, 0)
    font = pygame.font.SysFont("Arial", 36)
    txtsurf = font.render(text, True, green)
    sprite_entity = world.create_entity()
    pos = pygame.Vector2(pos[0] - txtsurf.get_width() // 2, pos[1] - txtsurf.get_height() // 2)
    world.add_component(sprite_entity,
                        CTextText(pos, txtsurf))
    return sprite_entity


def create_text(world: esper.World, interface_config_info: dict, key: str):
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
    vel = pygame.Vector2(0, 0)

    entity = create_sprite(world, p, vel, interface_surface)
    world.add_component(entity, CTagText())
    return entity
