import esper
import random
from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState, HunterState
from src.engine.service_locator import ServiceLocator



def system_enemy_hunter_random(world: esper.World, player_entity: int, hunter_info: dict):
    pl_t = world.component_for_entity(player_entity, CTransform)
    components = world.get_components(CEnemyHunterState, CAnimation, CTransform, CVelocity)

    if(get_enemy_running(components)<2 ) and len(components) > 0 :
        random_index = random.randint(0,len(components)-1)
        _, (c_st, c_a, c_t, c_v) = components[random_index]
        c_st.state = HunterState.CHASE
        set_animation(c_a, "MOVE") 


def get_enemy_running(components:list):
    cant = 0 
    for _, (c_st, c_a, c_t, c_v) in components:
       if c_st.state == HunterState.CHASE :
           cant+=1
     
    return cant