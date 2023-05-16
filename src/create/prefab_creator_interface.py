from enum import Enum
import pygame
import esper
from src.create.prefab_creator import create_sprite

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_blink import CTagBlink
from src.ecs.components.tags.c_tag_header import CTagHeader
from src.ecs.components.tags.c_tag_key import CTagKey
from src.ecs.components.tags.c_tag_menu import CTagMenu
from src.ecs.components.tags.c_tag_text import CTagText
from src.engine.service_locator import ServiceLocator

class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2

def create_text_dinamic(world:esper.World, txt:str, size:int, 
                color:pygame.Color, alignment:TextAlignment,screen:pygame.Surface) -> int:
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx
    
    centerx, centery = screen.get_rect().centerx, screen.get_rect().centery
    deltaY = centery + 50  # adjust so it goes below screen start


    world.add_component(text_entity,
                        CTransform((centerx, centery+deltaY+30) + origin))
    return text_entity

def create_text(world:esper.World, key:str, screen:pygame.Surface ,txt:str, size:int, font: str, 
                color:pygame.Color, pos:pygame.Vector2, vel:pygame.Vector2=None, alignment_x=None, alignment_y=None, blink:int = None, start:str=None) -> int:
    font = ServiceLocator.fonts_service.get(font, size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    final_pos = pos
    if alignment_x != None:
        final_pos.x = (alignment_x * screen.get_width()) - txt_s.area.centerx
    if alignment_y != None:
        final_pos.y = (alignment_y * screen.get_height()) - txt_s.area.centery
    vel = pygame.Vector2(0, 0) if vel is None else vel
    world.add_component(text_entity,
                        CVelocity(vel))
    world.add_component(text_entity, CTagMenu(final_pos))
    if start == "BOTTOM":
        origin = pygame.Vector2(final_pos.x, final_pos.y + screen.get_height())
    else:
        origin = pygame.Vector2(final_pos.x, final_pos.y)
    world.add_component(text_entity,
                        CTransform(origin))
    if blink is not None:
        ("Creat tag")
        world.add_component(text_entity, CTagBlink(blink))
    world.add_component(text_entity, CTagHeader())
    world.add_component(text_entity, CTagKey(key))
    world.add_component(text_entity, CText(final_pos,txt))
    return text_entity

def create_image(world:esper.World, key: str, screen:pygame.Surface ,path:str, pos:pygame.Vector2, vel:pygame.Vector2=None, alignment_x=None, alignment_y=None, scale:int = 1, blink:int = None, start:str=None):
    image_surface = ServiceLocator.images_service.get(path)
    image_surface = pygame.transform.scale_by(image_surface, scale)
    final_pos = pos
    if alignment_x != None:
        final_pos.x = (alignment_x * screen.get_width()) - image_surface.get_width()/2
    if alignment_y != None:
        final_pos.y = (alignment_y * screen.get_height) - image_surface.get_height()/2
    velocity = pygame.Vector2(0, 0) if vel is None else vel
    if start == "BOTTOM":
        origin = pygame.Vector2(final_pos.x, final_pos.y + screen.get_height())
    else:
        origin = pygame.Vector2(final_pos.x, final_pos.y)
    image_entity = create_sprite(world, origin, velocity, image_surface)
    world.add_component(image_entity, CTagMenu(final_pos))
    if blink is not None:
        world.add_component(image_entity, CTagBlink(blink))
    world.add_component(image_entity, CTagHeader())
    world.add_component(image_entity, CTagKey(key))
    return image_entity

def create_menu(world: esper.World, menu_config_info: dict, screen:pygame.Surface ):
    items = {}
    for key, config in menu_config_info.items():
        alignment_x = None if config.get("alignment_x") is None else config["alignment_x"]
        alignment_y = None if config.get("alignment_y") is None else config["alignment_y"]
        blink = None if config.get("blink_time") is None else config["blink_time"]
        velocity = None if config.get("velocity") is None else pygame.Vector2(config["velocity"]["x"], config["velocity"]["y"])
        start = None if config.get("start") is None else config["start"]
        if config["type"].lower() == "text":
            entity = create_text(world, 
                        key,
                        screen,
                        config["text"], 
                        config["size"], 
                        config["font"], 
                        pygame.Color(config["color"]["r"],config["color"]["g"],config["color"]["b"]), 
                        pygame.Vector2(config["position"]["x"], config["position"]["y"]),
                        velocity, 
                        alignment_x,
                        alignment_y,
                        blink,
                        start)
            items[key]=entity
        elif config["type"].lower() == "image":
            scale = 1 if config.get("scale") is None else config["scale"]
            entity = create_image( world, 
                         key,
                         screen, 
                         config["image"],
                         pygame.Vector2(config["position"]["x"], config["position"]["y"]),
                         velocity, 
                         alignment_x,
                         alignment_y,
                         scale,
                         blink, 
                         start)
            items[key]=entity
    return items
