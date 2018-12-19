from flask import current_app
from ..app import create_app, db


class BasicTestCase():
    def set_up(self):
        self.app = create_app('testing')
        self.app_context = self.app_context()
        self.app_context.push()
        db.create_all()

    def tear_down(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        assert current_app is not None

    def test_app_is_testing(self):
        assert current_app.config['TESTING']
