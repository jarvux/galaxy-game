from enum import Enum


class CPlayerState:
    def __init__(self, num_lives:int):
        self.state = PlayerState.IDLE
        self.num_lives =num_lives


class PlayerState(Enum):
    IDLE = 0
    MOVE = 1
