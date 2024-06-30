from datetime import timedelta
from flask import Blueprint
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from init import db, bcrypt
from models.player import Player, PlayerSchema
from auth import admin_only


player_bp = Blueprint("players", __name__, url_prefix='/players')


@player_bp.route('/<int:id>')
@jwt_required()
def all_players(id):
    """get one player by id

    A player object is retrieved from the db 
    player objects contain direct access to match_player
    """
    player = db.get_or_404(Player, id)
    return PlayerSchema(exclude=("password",)).dump(player)


@player_bp.route("/login", methods=["POST"])
def login():
    """ logs in a player

    Player object that has matching email is retrieved from the db
    """
    params = PlayerSchema(only=["email", "password"]).load(
        request.json, unknown="exclude"
    )
    stmt = db.select(Player).where(Player.email == params["email"])
    player = db.session.scalar(stmt)
    if player and bcrypt.check_password_hash(player.password, params["password"]):
        token = create_access_token(
            identity=player.id, expires_delta=timedelta(hours=10))
        return {"token": token}
    else:
        return {"error": "Invalid email or password"}, 401


@player_bp.route('/', methods=['POST'])
@admin_only
def create_player():
    """ create new player

    no db queries
    """
    player_info = PlayerSchema(
        only=["email", "password", "name", "admin"]).load(request.json)
    password = player_info['password']
    player = Player(
        name=player_info['name'],
        email=player_info['email'],
        password=bcrypt.generate_password_hash(password).decode("utf8"),
        admin=player_info.get('admin', False)
    )
    db.session.add(player)
    db.session.commit()
    return PlayerSchema(exclude=('password',)).dump(player), 201
