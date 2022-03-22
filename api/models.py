import psycopg2

from api.app import db
import sqlalchemy as sqla
from psycopg2 import errors

class App(db.Model):
    __tablename__ = 'app'

    id = sqla.Column(sqla.Integer, primary_key=True)
    token = sqla.Column(sqla.String(255), index=True, nullable=False, unique=True)

    @staticmethod
    def get_by_token(token):
        a = App.query.filter_by(token=token).first()
        return a.id if a else None


class StoryMetadata(db.Model):
    __tablename__ = 'story_metadata'

    app_id = sqla.Column(sqla.Integer, index=True)
    story_id = sqla.Column(sqla.Integer, primary_key=True)
    metadata_ = sqla.Column("metadata", sqla.String(255))

    @staticmethod
    def select(token):
        return db.session.query(StoryMetadata, App).filter(App.id == StoryMetadata.app_id).filter(
            App.token == token).all()

    @staticmethod
    def story_exists(sid):
        story = StoryMetadata.query.filter_by(story_id=sid).first()
        return story.id if story else None

    def __repr__(self):
        return f'<StoryMetaData {self.app_id} {self.story_id} {self.metadata_}>'


class StoryEvent(db.Model):
    __tablename__ = 'story_event'

    app_id = sqla.Column(sqla.Integer, primary_key=True)
    story_id = sqla.Column(sqla.Integer, primary_key=True)
    user_id = sqla.Column(sqla.Integer, primary_key=True)
    date_ = sqla.Column("date", sqla.DATE, primary_key=True)
    type_ = sqla.Column("type", sqla.String(64), primary_key=True)
    count = sqla.Column(sqla.Integer)

    @staticmethod
    def operate(app_id, story_id, user_id, event_date, type):
        try:
            event = StoryEvent.query.filter_by(app_id=app_id, story_id=story_id, user_id=user_id, date_=event_date,
                                               type_=type).first()
            if event:
                event.count += 1
            else:
                event_to_save = StoryEvent(app_id=app_id, story_id=story_id, user_id=user_id, date_=event_date,
                                           type_=type, count=1)
                db.session.add(event_to_save)

            db.session.commit()
        except Exception as e:
            return e

        return True

    @staticmethod
    def get_dau(token, event_date):
        dau = db.session.query(StoryEvent, App).filter(App.id == StoryEvent.app_id).filter(
            App.token == token, StoryEvent.date_ == event_date).all()

        return dau
