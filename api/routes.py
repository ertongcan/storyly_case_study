from flask import Blueprint, abort, jsonify, make_response, request
from api.app import cache
from api.helper import prepare_response
from api.models import StoryMetadata, StoryEvent
from flask import current_app
from threading import Thread

from api.tasks import operate_event

stories = Blueprint('stories', __name__)
event = Blueprint('event', __name__)


@stories.errorhandler(404)
def not_found(error):
    return jsonify({'message': "No story found!"})


# First assignment
@stories.route('/stories/<string:token>', methods=['GET'])
def get(token):
    query_result = StoryMetadata.select(token) or abort(404)
    result = prepare_response(query_result, current_app)

    return make_response(jsonify(result), 200)


# Second assignment
@stories.route('/stories_enhanced/<string:token>', methods=['GET'])
@cache.cached(timeout=20)
def enhanced_get(token):
    query_result = StoryMetadata.select(token) or abort(404)
    result = prepare_response(query_result, current_app)

    return make_response(jsonify(result), 200)


# Third assignment - runs in background no need for user interaction
@event.route('/event/<string:token>', methods=['POST'])
def insert_event(token):
    thread = Thread(target=operate_event, args=(token, request.json))
    thread.daemon = True
    thread.start()
    return make_response(jsonify({'message': "Event added to queue"}), 200)


# bonus assignment - dau
@event.route('/event/dau/<string:token>/<string:event_date>', methods=['GET'])
def dau(token, event_date):
    try:
        dau = StoryEvent.get_dau(token, event_date)
    except Exception as e:
        return make_response(jsonify({'result': 'Error occured!'}), 500)

    if len(dau) == 0:
        return make_response(jsonify({'result': 'no daily active users'}), 404)


    resp = []
    for results in dau:
        se = results[0] if len(results) > 0 else None
        if se is not None:
            resp.append(se.user_id)

    unique_users = list(set(resp))

    return make_response(jsonify({'result':unique_users}), 200)


