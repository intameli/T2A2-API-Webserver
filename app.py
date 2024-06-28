from init import app
from blueprints.cli import commands
from blueprints.match_bp import match_bp


app.register_blueprint(commands)
app.register_blueprint(match_bp)


@app.route('/')
def test():
    return 'World'


# print(app.url_map)
