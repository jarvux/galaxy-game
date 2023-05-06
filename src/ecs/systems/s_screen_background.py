import pygame
import esper
from src.create.prefab_creator import create_background

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_background import CTagBackground

def system_screen_background(world: esper.World, screen: pygame.Surface):
    scr_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagBackground)
    #TODO: Inlclude number as a config file
    numStars = 30
    numComponents = len(components)
    fromAxisX = numComponents != 0  
    if numComponents < numStars :
        for num in range(numComponents, numStars):
            create_background(world, screen, fromAxisX)
    #TODO: Sometimes background is visible
    for bullet_entity, (c_t, c_s, _) in components:
        bullet_rect = CSurface.get_area_relative(c_s.area,c_t.pos)
        if not scr_rect.contains(bullet_rect):
            world.delete_entity(bullet_entity)
