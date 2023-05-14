import pygame

class CEnemySpawner:
    def __init__(self, spawn_events_data:dict,enemies_position_data:dict,initial_position:dict) -> None:
        self.current_time:float = 0
        self.spawn_event_data:list[SpawnEventData] = []
        row_position   = initial_position["x"]
        colum_position = initial_position["y"]
        for row in enemies_position_data : 
            row_position += 25
            colum_position = 0
            for column in row : 
                enemy_type = column
                colum_position += 25
                if enemy_type == 0:
                    continue
                position= pygame.Vector2(colum_position,row_position)
                self.spawn_event_data.append(SpawnEventData(get_data_enemy(enemy_type,spawn_events_data),position))

class SpawnEventData:
    def __init__(self, event_data:dict, position : pygame.Vector2) -> None:
        self.time:float = event_data["time"]
        self.enemy_type:str =  event_data["enemy_type"]
        self.position:pygame.Vector2 = position
        self.triggered = False

def get_data_enemy(enemy_type:int,enemies_data: dict):
    for data in  enemies_data : 
        if data["enemy_type"] == enemy_type:
            return data
    return None