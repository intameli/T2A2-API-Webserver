from flask import Blueprint
from init import db
from models.player import Player

commands = Blueprint('db', __name__)


@commands.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print(db)
