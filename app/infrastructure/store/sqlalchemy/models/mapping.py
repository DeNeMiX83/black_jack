from app.infrastructure.store.sqlalchemy.models import (
    game_mapping,
    game_state_mapping,
    chat_mapping,
    player_mapping,
    user_mapping,
    player_cards_mapping,
    admin_mapping,
)
from app.infrastructure.store.sqlalchemy.models.base import Base


def start_mappers():
    mapper_registry = Base.registry
    user_mapping(mapper_registry)
    chat_mapping(mapper_registry)
    game_mapping(mapper_registry)
    game_state_mapping(mapper_registry)
    player_mapping(mapper_registry)
    player_cards_mapping(mapper_registry)
    admin_mapping(mapper_registry)
