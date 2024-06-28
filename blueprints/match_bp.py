from flask import Blueprint, request
from models.match import Match, MatchSchema
from models.player import Player, PlayerSchema
from models.match_player import Match_Player, Match_PlayerSchema
from init import db

match_bp = Blueprint('matches', __name__, url_prefix='/matches')


@match_bp.route('/join')
def join_table():
    stmt = db.select(Match_Player)
    matches = db.session.scalars(stmt).all()
    return Match_PlayerSchema(many=True).dump(matches)


@match_bp.route('/a')
def all_players():
    stmt = db.select(Player)
    matches = db.session.scalars(stmt).all()
    return PlayerSchema(many=True).dump(matches)


@match_bp.route('/')
def all_matches():
    stmt = db.select(Match)
    matches = db.session.scalars(stmt).all()
    return MatchSchema(many=True).dump(matches)


@match_bp.route('/b')
def single_match():
    matches = db.get_or_404(Match, 1)
    return MatchSchema(exclude=('court_id',)).dump(matches)


# Create

@match_bp.route("/", methods=["POST"])
# @jwt_required()
def create_match():
    match_info = MatchSchema(only=["time", "players", "court_id"], unknown="exclude").load(
        request.json
    )
    print(match_info['players'][1]['id'])
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
    return MatchSchema().dump(match), 201


@match_bp.route("/<int:id>", methods=["PUT", "PATCH"])
# @jwt_required()
def update_match(id):
    match = db.get_or_404(Match, id)
    # authorize_owner(card)

    match_info = MatchSchema(only=["time", 'results', 'court_id'], unknown="exclude").load(
        request.json
    )
    match.time = match_info.get("time", match.time)
    new_results = match_info.get("results", match.results)
    most_games = -1
    winner = 0
    for result in match.results:
        new_result = next(
            (x for x in new_results if x['player_id'] == result.player_id), None)
        result.games_won = new_result['games_won']
        if result.games_won > most_games:
            winner = result.player_id
        elif result.games_won == most_games:
            winner = 0
        most_games = result.games_won
    for result in match.results:
        if winner == 0:
            result.result = 'Tie'
        elif result.player_id == winner:
            result.result = 'Winner'
        else:
            result.result = 'Loser'
    match.court_id = match_info.get("court_id", match.court_id)
    db.session.commit()
    return MatchSchema().dump(match)


# Delete

@match_bp.route("/<int:id>", methods=["DELETE"])
# @jwt_required()
def delete_match(id):
    match = db.get_or_404(Match, id)
    # authorize_owner(card)
    db.session.delete(match)
    db.session.commit()
    return {}
