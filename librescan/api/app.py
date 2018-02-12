
# I don't like this but Flask recommend it
# http://flask.pocoo.org/docs/0.12/patterns/packages/

from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO
from .controllers import (
    ImagesListController,
    ProjectsController,
    ProjectsListController,
    OutputsListController
)

app = Flask(__name__)
api = Api(app)

# Import individual image and thumbnail route
from .controllers.images import images_controller


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


api.add_resource(ProjectsListController, '/api/projects')
api.add_resource(ProjectsController, '/api/projects/<string:_id>')
api.add_resource(ImagesListController, '/api/projects/<string:_id>/images')
api.add_resource(OutputsListController, '/api/projects/<string:_id>/outputs')

# Initialize sockets io support
socketio = SocketIO(app)

