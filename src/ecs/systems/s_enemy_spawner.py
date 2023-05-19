import esper
from src.create.prefab_creator import create_enemy_square, create_enemy_hunter
from src.ecs.components.c_enemy_spawner import CEnemySpawner, SpawnEventData

def system_enemy_spawner(world: esper.World, enemies_data: dict, delta_time: float):
    components = world.get_component(CEnemySpawner)
    c_spw: CEnemySpawner
    for _,  c_spw in components:
        c_spw.ref_distance += c_spw.ref_velocity * delta_time
        if abs(c_spw.ref_distance) > abs(c_spw.max_distance):
            c_spw.ref_velocity *= -1
        c_spw.current_time += delta_time
        spw_evt: SpawnEventData
        for spw_evt in c_spw.spawn_event_data:
            if c_spw.current_time >= spw_evt.time and not spw_evt.triggered:
                spw_evt.triggered = True
                create_enemy_hunter(world,
                                    spw_evt.position,
                                    enemies_data[str(spw_evt.enemy_type)], spw_evt.enemy_type)