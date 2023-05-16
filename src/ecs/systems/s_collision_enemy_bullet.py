

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.create.prefab_creator import create_explosion, update_hi_score, update_score


def system_collision_enemy_bullet(world: esper.World, explosion_info: dict, score_entity: int, hi_score_entity: int):
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy, CEnemyHunterState)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)

    for enemy_entity, (c_s, c_t, c_ene, c_state) in components_enemy:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        for bullet_entity, (c_b_s, c_b_t, _) in components_bullet:
            bull_rect = c_b_s.area.copy()
            bull_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bull_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                new_score = update_score(world ,c_state.score, score_entity)
                update_hi_score(world, new_score, hi_score_entity)
                create_explosion(world, c_t.pos, explosion_info)
