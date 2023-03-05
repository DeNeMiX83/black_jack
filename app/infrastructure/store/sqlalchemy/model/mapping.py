from app.infrastructure.store.sqlalchemy.model import (
    game_mapping, game_state_mapping, chat_mapping, player_mapping
)
from app.infrastructure.db.sqlalchemy.models.base import Base


def start_mappers():
    mapper_registry = Base.registry
    chat_mapping(mapper_registry)
    game_mapping(mapper_registry)
    game_state_mapping(mapper_registry)
    player_mapping(mapper_registry)