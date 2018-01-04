from flask import Flask, send_file
from flask_restful import Api
from .controllers import ProjectsController, ProjectsListController

app = Flask(__name__)
api = Api(app)


# @app.route('/get_image')
# def get_image():
#     if request.args.get('type') == '1':
#        filename = 'ok.gif'
#     else:
#        filename = 'error.gif'
#     return send_file(filename, mimetype='image/gif')


api.add_resource(ProjectsListController, '/projects')
api.add_resource(ProjectsController, '/projects/<string:_id>')
