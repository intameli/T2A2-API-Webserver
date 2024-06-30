from flask import Blueprint, request
from models.match import Match, MatchSchema
from models.match_player import Match_Player
from init import db
from flask_jwt_extended import jwt_required
from auth import admin_only

match_bp = Blueprint('matches', __name__, url_prefix='/matches')


@match_bp.route('/')
@jwt_required()
def all_matches():
    """ get all matches

    db is queried for all matches
    """
    stmt = db.select(Match)
    matches = db.session.scalars(stmt).all()
    return MatchSchema(many=True, exclude=("court_id",)).dump(matches)


@match_bp.route("/<int:id>")
@jwt_required()
def single_match(id):
    """ get a single match

    The db is queried for a single match with a corresponding id
    """
    matches = db.get_or_404(Match, id)
    return MatchSchema(exclude=('court_id',)).dump(matches)


@match_bp.route("/", methods=["POST"])
@admin_only
def create_match():
    """ create a new match

    no db queries in this endpoint
    """
    match_info = MatchSchema(only=["time", "players", "court_id"], unknown="exclude").load(
        request.json
    )
    match = Match(
        time=match_info["time"],
        court_id=match_info['court_id']
    )
    db.session.add(match)
    db.session.commit()
    join = [
        Match_Player(
            match_id=match.id,
            player_id=match_info['players'][0]['id']),
        Match_Player(
            match_id=match.id,
            player_id=match_info['players'][1]['id'])
    ]
    db.session.add_all(join)
    db.session.commit()
    return MatchSchema(exclude=("court_id",)).dump(match), 201


@match_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@admin_only
def update_match(id):
    """ update match

    The db is queried for a single match with a corresponding id
    """
    match = db.get_or_404(Match, id)
    match_info = MatchSchema(only=["time", 'results', 'court_id'], unknown="exclude").load(
        request.json
    )
    match.time = match_info.get("time", match.time)
    new_results = match_info.get("results", 0)
    if new_results:
        most_games = -1
        winner = 0
        for result in match.results:
            new_result = next(
                (x for x in new_results if x['player_id'] == result.player_id), None)
            result.games_won = new_result['games_won']
            result.tie_break = new_result.get('tie_break', result.tie_break)
            if result.games_won > most_games:
                winner = result.player_id
            most_games = result.games_won
        for result in match.results:
            if result.player_id == winner:
                result.result = 'Winner'
            else:
                result.result = 'Loser'
    match.court_id = match_info.get("court_id", match.court_id)
    db.session.commit()
    return MatchSchema(exclude=("court_id",)).dump(match)


@match_bp.route("/<int:id>", methods=["DELETE"])
@admin_only
def delete_match(id):
    """ delete a match

    The db is queried for a single match with a corresponding id
    """
    match = db.get_or_404(Match, id)
    db.session.delete(match)
    db.session.commit()
    return {}
