import pygame
import esper


from src.ecs.components.c_text import CText
from src.ecs.components.c_text_key import CTextText


def system_screen_interface(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CText)
    for _, (c_t) in components:
        screen.blit(c_t[0].text, c_t[0].pos)

def system_screen_text(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CTextText)
    for _, (c_t) in components:
        screen.blit(c_t[0].text, c_t[0].pos)