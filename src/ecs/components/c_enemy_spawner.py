import pygame

from src.engine.service_locator import ServiceLocator


class CEnemySpawner:
     def __init__(self, level_data: dict, enemies_data: dict, screen: pygame.Surface) -> None:
        self.ref_velocity = -20
        self.ref_distance = 0
        self.max_distance = 50
        self.current_time: float = 0
        self.spawn_event_data: list[SpawnEventData] = []
        surface = screen.get_rect()
        position_x =  (surface.width/2)-((len(level_data["enemy_spawn_events"])/2)*55)+74
        row_position = level_data["position"]["x"]
        
        colum_position = level_data["position"]["y"]
        delta_x = level_data["delta"]["x"]
        delta_y = level_data["delta"]["y"]
        for row in level_data["enemy_spawn_events"]:
            row_position += delta_y
            colum_position = 0
            num_rows = len(row)
            e_set = set(row)
            e_set.discard(0)
            e_type = e_set.pop()
            e_width = (ServiceLocator.images_service.get(enemies_data[str(e_type)]["image"]).get_width())/enemies_data[str(e_type)]["animations"]["number_frames"]
            item = 1
            for column in row:
                enemy_type = column
                colum_position = ((screen.get_width()-((num_rows-1)*delta_x))/2)+(item-1)*(delta_x) - e_width/2
                item += 1
                if enemy_type == 0:
                    continue
                position = pygame.Vector2(colum_position, row_position)
                self.spawn_event_data.append(SpawnEventData(get_data_enemy(enemy_type, level_data["enemy_config"]), position))


class SpawnEventData:
    def __init__(self, event_data: dict, position: pygame.Vector2) -> None:
        self.time: float = event_data["time"]
        self.enemy_type: str = event_data["enemy_type"]
        self.position: pygame.Vector2 = position
        self.triggered = False


def get_data_enemy(enemy_type: int, enemies_data: dict):
    for data in enemies_data:
        if data["enemy_type"] == enemy_type:
            return data
    return None
