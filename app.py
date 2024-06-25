from init import app


@app.route('/')
def test():
    return 'Hello World'
