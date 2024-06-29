from datetime import timedelta
from flask import Blueprint
# from auth import admin_only
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from init import db, bcrypt
from models.player import Player, PlayerSchema
from auth import admin_only


player_bp = Blueprint("players", __name__, url_prefix='/players')


@player_bp.route('/')
@jwt_required()
def all_players():
    stmt = db.select(Player)
    matches = db.session.scalars(stmt).all()
    return PlayerSchema(many=True).dump(matches)


@player_bp.route("/login", methods=["POST"])
def login():
    """_summary_

    Returns:
        _type_: _description_
    """
    params = PlayerSchema(only=["email", "password"]).load(
        request.json, unknown="exclude"
    )
    stmt = db.select(Player).where(Player.email == params["email"])
    player = db.session.scalar(stmt)
    if player and bcrypt.check_password_hash(player.password, params["password"]):
        token = create_access_token(
            identity=player.id, expires_delta=timedelta(hours=2))
        return {"token": token}
    else:
        return {"error": "Invalid email or password"}, 401


@player_bp.route('/', methods=['POST'])
@admin_only
def create_player():
    params = PlayerSchema(
        only=["email", "password", "name", "is_admin"]).load(request.json)
    return params
