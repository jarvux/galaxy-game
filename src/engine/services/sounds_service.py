import pygame
class SoundsService:
    def __init__(self) -> None:
        self._sounds = {}

    def play(self,path:str):
        if path not in self._sounds:
           self._sounds[path] = pygame.mixer.Sound(path)
        self._sounds[path].play()