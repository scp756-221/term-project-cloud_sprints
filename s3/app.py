"""
SFU CMPT 756
Sample application---playlist service.
"""

# Standard library modules
import logging
import sys

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Playlist process')

bp = Blueprint('app', __name__)

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}


@bp.route('/', methods=['GET'])
@metrics.do_not_track()
def hello_world():
    return ("If you are reading this in a browser, your service is "
            "operational. Switch to curl/Postman/etc to interact using the "
            "other HTTP verbs.")


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")


@bp.route('/', methods=['GET'])
def list_all():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    # list all songs here
    return {}


@bp.route('/', methods=['POST'])
def create_playlist():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        playlist_name = content['Name']
        song_list = content['Playlist'].strip().split(',')
    except Exception:
        return json.dumps({"message": "error reading arguments"})

    if len(song_list) != 0:
        url_read = db['name'] + '/' + db['endpoint'][0]
        for ms_id in song_list:
            payload_music = {"objtype": "music", "objkey": ms_id}
            get_song = requests.get(
                url_read,
                params=payload_music,
                headers={'Authorization': headers['Authorization']}
            )
            if get_song.json()['Count'] == 0:
                return Response(json.dumps({"error":
                                f"failed to get the music_id {ms_id}"}),
                                status=600,
                                mimetype='application/json')

    url_write = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url_write,
        json={"objtype": "playlist",
              "Name": playlist_name,
              "Playlist": song_list},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


# @bp.route('/<playlist_id>/write', methods=['POST'])
# def add_song(playlist_id):
#     headers = request.headers
#     # check header here
#     if 'Authorization' not in headers:
#         return Response(json.dumps({"error": "missing auth"}),
#                         status=401,
#                         mimetype='application/json')
#     try:


@bp.route('/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')

    payload = {"objtype": "playlist", "objkey": playlist_id}
    url_read = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url_read,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    url_delete = db['name'] + '/' + db['endpoint'][2]
    response = requests.delete(
        url_delete,
        params={"objtype": "playlist", "objkey": playlist_id},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/playlist/')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)