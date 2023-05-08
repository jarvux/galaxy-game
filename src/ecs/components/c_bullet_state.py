from enum import Enum


class CBulletState:
    def __init__(self):
        self.state = BulletState.IDLE


class BulletState(Enum):
    IDLE = 0
    MOVE = 1
