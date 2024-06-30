from init import app
from blueprints.cli import commands
from blueprints.match_bp import match_bp
from blueprints.player_bp import player_bp
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError


app.register_blueprint(commands)
app.register_blueprint(match_bp)
app.register_blueprint(player_bp)


@app.errorhandler(405)
@app.errorhandler(404)
def not_found(err):
    return {"error": "Not Found"}, 404


@app.errorhandler(ValidationError)
def invalid_request(err):
    return {"error": vars(err)["messages"]}, 400


@app.errorhandler(KeyError)
def missing_key(err):
    return {"error": f"Missing field: {str(err)}"}, 400


@app.errorhandler(IntegrityError)
def dup_key(err):
    return {"error": "email already associated with another player"}
