import pygame
import pygame.freetype


class FontService:
    def __init__(self) -> None:
        self._fonts = {}

    def get(self, key: str, path: str, size: int) -> pygame.Surface:
        if key not in self._fonts:
            self._fonts[key] = pygame.font.Font(path, size)
        return self._fonts[key]
