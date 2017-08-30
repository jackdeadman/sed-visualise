from flask import Flask
from flask_cors import CORS

from modules.config import app_config

# Blueprints
from controllers.index import index
from controllers.play import play

def create_app():
    app = Flask(__name__,
            static_url_path='',
            static_folder=app_config['static_folder'])
    app.config['UPLOAD_FOLDER'] = app_config['upload_folder']
    app.secret_key = app_config['secret']
    return app

def register_blueprints(app):
    app.register_blueprint(index)
    app.register_blueprint(play)

if __name__ == '__main__':
    app = create_app()
    CORS(app, resources={"*": {"origins": "*"}})
    register_blueprints(app)
    app.run(threaded=True)