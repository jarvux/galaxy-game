import pygame

class CSurface:
    def __init__(self, size:pygame.Vector2, color:pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()
        self.color = color
        self.visible = True
        self.font = None

    @classmethod
    def from_surface(cls, surface:pygame.Surface):
        c_surf = cls(pygame.Vector2(0,0), pygame.Color(255,255,255))
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf
    
    @classmethod
    def from_text(cls, text:str, font:pygame.font.Font, color:pygame.color):
        c_surf = cls(pygame.Vector2(0,0), color)
        c_surf.surf = font.render(text, True, color)
        c_surf.area = c_surf.surf.get_rect()
        c_surf.font = font
        return c_surf
    
    def update_text(self, text:str):
        self.surf = self.font.render(text, True, self.color)
        self.area = self.surf.get_rect()

    def get_area_relative(area:pygame.Rect, pos_topleft:pygame.Vector2):
        new_rect = area.copy()
        new_rect.topleft = pos_topleft.copy()
        return new_rect
    
