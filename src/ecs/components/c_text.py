import pygame

class CText:
    def __init__(self, pos:pygame.Vector2,text: str) -> None:
        self.pos = pos
        self.text = text