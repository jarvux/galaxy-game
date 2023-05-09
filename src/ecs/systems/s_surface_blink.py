
import esper
import time
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_blink import CTagBlink

def system_surface_blink(world:esper.World):
    components = world.get_components(CSurface, CTagBlink)
    for _, (c_s, c_t) in components:
        delta = time.time() - c_t.timestamp
        num = (int(delta / c_t.interval) % 2)
        if num == 0 and not c_s.visible:
            c_s.visible = True
        elif num != 0 and c_s.visible:
            c_s.visible = False
