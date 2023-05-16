import json
import pygame.freetype


class ConfigsService:
    def __init__(self) -> None:
        self._cfgs = {}

    def get(self, path:str) -> dict:
        if path not in self._cfgs:
            with open(path, encoding="utf-8") as file:
                self._cfgs[path] = json.load(file)
        return self._cfgs[path]
    
    def update(self, path:str, value: dict) -> dict:
        self._cfgs[path] = value
