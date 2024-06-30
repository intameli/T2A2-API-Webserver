from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from functools import wraps
from init import db
from models.player import Player


def admin_only(fn):
    """ check admin

    The database is queried for a player with an id that matches
    the id in the JWT and that also has a true admin value
    """
    @wraps(fn)
    @jwt_required()
    def inner(**kwargs):
        player_id = get_jwt_identity()
        stmt = db.select(Player).where(Player.id == player_id, Player.admin)
        player = db.session.scalar(stmt)
        if player:
            return fn(**kwargs)
        else:
            return {"error": "You must be an admin to access this resource"}, 403

    return inner
