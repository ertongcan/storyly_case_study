import unittest
import os

from api import create_app, db
from dotenv import load_dotenv
from config import Config

load_dotenv()


class TestConfig(Config):
    SERVER_NAME = '127.0.0.1:5000'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']


class BaseTestCase(unittest.TestCase):
    config = TestConfig

    def setUp(self):
        self.app = create_app(self.config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.close()
        self.app_context.pop()

    def test_get_stories(self):
        st = self.client.get('/api/stories/token_1')
        assert st.status_code == 200

    def test_get_dau(self):
        st = self.client.get('/api/event/dau/token_1/2022-03-22')
        assert st.status_code == 200

    def test_save_event(self):
        st = rv = self.client.post('/api/event/token_1', json={
             "story_id": 1,
             "event_type": "impression",
             "user_id": "3"
        })
        assert st.status_code == 200
        assert rv.json['message'] == 'Event added to queue'


if __name__ == '__main__':
    unittest.main()
