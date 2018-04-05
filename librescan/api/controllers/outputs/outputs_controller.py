from flask import abort, request, send_file, Response
from librescan.api.app import app
from librescan.utils.output.impl import PDFBeads
from librescan.config import config


@app.route('/api/projects/<p_project_id>/outputs/pdf')
def get_pdf(p_project_id):
    config.change_project(p_project_id)
    try:
        return send_file(
            PDFBeads.get(),
            mimetype='application/pdf'
        )
    except FileNotFoundError as err:
        abort(404, f'File Not Found: {str(err)}')
    except (TypeError, ValueError) as err:
        abort(400, str(err))