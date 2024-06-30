from flask import Blueprint
from init import db, bcrypt
from datetime import datetime
from models.match import Match, MatchSchema
from models.player import Player
from models.match_player import Match_Player
from models.court import Court

commands = Blueprint('db', __name__)


@commands.cli.command('create')
def create_tables():
    db.drop_all()
    db.create_all()

    db.session.add_all([
        Player(
            name='Jacob',
            email='jacob@gmail.com',
            password=bcrypt.generate_password_hash("password").decode("utf8"),
            admin=True
        ),
        Player(
            name='Alex',
            email='alex@gmail.com',
            password=bcrypt.generate_password_hash("secret").decode("utf8")
        )])
    db.session.add(Court(surface='hard'))
    db.session.add(Court(surface='grass'))
    db.session.commit()

    # m = Match(time=datetime(2024, 7, 2, 10))
    m = Match(time=datetime(2024, 7, 2, 10), court_id=1)

    db.session.add(m)
    db.session.commit()
    arr = [Match_Player(match_id=1, player_id=1),
           Match_Player(match_id=1, player_id=2)]

    db.session.add_all(arr)
    db.session.commit()
    print('Data Added')
