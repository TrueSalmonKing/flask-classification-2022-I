from app import app
from . import classifications
from .classifications_id import *
import json
from app import app
from flask import Response, request

config = Configuration()

@app.route("/download_json/<string:job_id>", methods=['GET'])
def download_json(job_id):
    """API for returning the results in a JSON file"""
    
    response = classifications_id(job_id)

    return Response(
        json.dumps(response['data']),
        mimetype='application/json',
        headers={
            'Content-disposition':
                "attachment; filename=download_results.json"
            }
    )