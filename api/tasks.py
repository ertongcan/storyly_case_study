import logging
from datetime import date

from api import create_app
from api.models import StoryEvent, App


def operate_event(token, req):
    # out of context, reentering
    app = create_app()
    app.app_context().push()

    app_id = App.get_by_token(token)

    if app_id is None:
        logging.error(f"Unknown token received {token}")

    story_id = req['story_id']
    user_id = req['user_id']
    date_ = date.today()
    type_ = req['event_type']

    StoryEvent.operate(app_id, story_id, user_id, date_, type_)
