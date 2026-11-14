import logging

import connexion
from flask_testing import TestCase

from habit_tracker.encoder import JSONEncoder
from habit_tracker.errors import register_error_handlers
from habit_tracker.store import store


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../openapi/')
        app.app.json_encoder = JSONEncoder
        app.add_api('openapi.yaml', pythonic_params=True, validate_responses=True)
        register_error_handlers(app.app)
        return app.app

    def setUp(self):
        store.clear()
