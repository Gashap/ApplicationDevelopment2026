#!/usr/bin/env python3

import connexion

from habit_tracker import encoder
from habit_tracker.errors import register_error_handlers


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.app.config['JSON_AS_ASCII'] = False
    app.add_api('openapi.yaml',
                arguments={'title': 'Habit Tracker API'},
                pythonic_params=True)
    register_error_handlers(app.app)

    app.run(port=8080)


if __name__ == '__main__':
    main()
