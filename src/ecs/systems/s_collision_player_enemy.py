

import esper
import pygame
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_explosion
from src.engine.scenes.scene import Scene


def system_collision_player_enemy(world: esper.World, player_entity: int,
                                  level_cfg: dict, explosion_info: dict,screen:pygame.Surface, num_lives: int, scene: Scene):
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)   
    pl_p = world.component_for_entity(player_entity, CPlayerState)   
    surface = screen.get_rect()
    pl_rect = pl_s.area.copy()
    pl_rect.topleft = pl_t.pos

    for enemy_entity, (c_s, c_t, _) in components:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        if ene_rect.colliderect(pl_rect):
            world.delete_entity(enemy_entity)
            pl_t.pos.x =  surface.centerx
            pl_t.pos.y =  surface.bottom
            create_explosion(world, c_t.pos, explosion_info)
            pl_p.num_lives -= 1
            if  pl_p.num_lives == 0 :
                scene.switch_scene("GAME_OVER_SCENE")
