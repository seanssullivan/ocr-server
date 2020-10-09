from flask import Flask, render_template

from server.routes import v1

def create_app():
    # create and configure the app
    app = Flask(__name__)

    @app.route('/')
    def index(name=None):
        return render_template('index.html', name=name)

    app.register_blueprint(v1)
    return app
