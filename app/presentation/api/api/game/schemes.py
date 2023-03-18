from marshmallow import Schema, fields
from app.core.game.entities import player_status


class UserStatsResponseSchema(Schema):
    games_results = fields.Nested('PlayerStatsResponseSchema', many=True)


class PlayerStatsResponseSchema(Schema):
    state = fields.Enum(player_status)
    score = fields.Int()
    bet = fields.Int()
