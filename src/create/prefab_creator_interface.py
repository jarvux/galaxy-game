from enum import Enum
import pygame
import esper
from src.create.prefab_creator import create_sprite

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_blink import CTagBlink
from src.ecs.components.tags.c_tag_menu import CTagMenu
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

def create_text(world:esper.World, screen:pygame.Surface ,txt:str, size:int, font: str, 
                color:pygame.Color, pos:pygame.Vector2, vel:pygame.Vector2=None, alignment="NONE", blink:int = None) -> int:
    font = ServiceLocator.fonts_service.get(font, size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    final_pos = pos
    if alignment == "CENTER":
        final_pos.x = screen.get_width()/2 - txt_s.area.centerx
    if alignment == "LEFT":
        final_pos.x = screen.get_width()/4 - txt_s.area.centerx
    if alignment == "RIGHT":
        final_pos.x = 3*screen.get_width()/4 - txt_s.area.centerx
    vel = pygame.Vector2(0, 0) if vel is None else vel
    world.add_component(text_entity,
                        CVelocity(vel))
    world.add_component(text_entity, CTagMenu(final_pos))
    origin = pygame.Vector2(final_pos.x, final_pos.y + screen.get_height())
    world.add_component(text_entity,
                        CTransform(origin))
    if blink is not None:
        ("Creat tag")
        world.add_component(text_entity, CTagBlink(blink))
    return text_entity

def create_image(world:esper.World, screen:pygame.Surface ,path:str, pos:pygame.Vector2, vel:pygame.Vector2=None, alignment="NONE", scale:int = 1, blink:int = None):
    image_surface = ServiceLocator.images_service.get(path)
    image_surface = pygame.transform.scale_by(image_surface, scale)
    final_pos = pos
    if alignment == "CENTER":
        final_pos.x = screen.get_width()/2 - image_surface.get_width()/2
    if alignment == "LEFT":
        final_pos.x = screen.get_width()/4 - image_surface.get_width()/2
    if alignment == "RIGHT":
        final_pos.x = 3*screen.get_width()/4 - image_surface.get_width()/2
    velocity = pygame.Vector2(0, 0) if vel is None else vel
    origin = pygame.Vector2(final_pos.x, final_pos.y + screen.get_height())
    image_entity = create_sprite(world, origin, velocity, image_surface)
    world.add_component(image_entity, CTagMenu(final_pos))
    if blink is not None:
        world.add_component(image_entity, CTagBlink(blink))
    return image_entity

def create_menu(world: esper.World, menu_config_info: dict, screen:pygame.Surface ):
    for key, config in menu_config_info.items():
        alignment = "NONE" if config.get("alignment") is None else config["alignment"].upper() 
        blink = None if config.get("blink_time") is None else config["blink_time"]
        if config["type"].lower() == "text":
            entity = create_text(world, 
                        screen,
                        config["text"], 
                        config["size"], 
                        config["font"], 
                        pygame.Color(config["color"]["r"],config["color"]["g"],config["color"]["b"]), 
                        pygame.Vector2(config["position"]["x"], config["position"]["y"]),
                        pygame.Vector2(config["velocity"]["x"], config["velocity"]["y"]), 
                        alignment,
                        blink)
        elif config["type"].lower() == "image":
            entity = create_image( world,
                         screen, 
                         config["image"],
                         pygame.Vector2(config["position"]["x"], config["position"]["y"]),
                         pygame.Vector2(config["velocity"]["x"], config["velocity"]["y"]), 
                         alignment,
                         config["scale"],
                         blink)
