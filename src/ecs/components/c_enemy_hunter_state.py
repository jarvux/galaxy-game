from enum import Enum
import math
import pygame


class CEnemyHunterState:
    def __init__(self, start_pos: pygame.Vector2, score: int):
        self.state = HunterState.IDLE
        self.start_pos = pygame.Vector2(start_pos.x, start_pos.y)
        self.chase_sound_channel = None
        self.score = score
        self.start_rot_pos = pygame.Vector2(0, 0)
        self.angle = math.pi


class HunterState(Enum):
    IDLE = 0
    PREPARE_CHASE = 1
    CHASE = 2
    RETURN = 3
    RETURN_HOME = 4
