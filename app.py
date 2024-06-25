from init import app
from blueprints.cli import commands

app.register_blueprint(commands)


@app.route('/')
def test():
    return 'Hello World'


# print(app.url_map)
