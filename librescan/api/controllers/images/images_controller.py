from flask import abort, request, send_file, Response
from librescan.api import app
from librescan.services import ImageService


@app.app.route('/projects/<p_project_id>/images/<p_image_id>')
def get_image(p_project_id, p_image_id):
    try:
        return send_file(
            ImageService.image_path(p_project_id, p_image_id),
            mimetype='image/jpeg'
        )
    except FileNotFoundError as err:
        abort(404, f'File Not Found: {str(err)}')
    except (TypeError, ValueError) as err:
        abort(400, str(err))


@app.app.route('/projects/<p_project_id>/thumbnails/<p_image_id>')
def get_thumbnail(p_project_id, p_image_id):
    try:
        height = int(request.args.get('height', 500))
        width = int(request.args.get('width', 375))
        image = ImageService.thumbnail(p_project_id, p_image_id, height, width)
        return Response(image, mimetype='image/jpeg')
    except FileNotFoundError as err:
        abort(404, f'File Not Found: {str(err)}')
    except (TypeError, ValueError) as err:
        abort(400, f'Error: height and width parameter must be integers; {str(err)}')

