#
# Flask-Minilog
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import logging

from flask import Blueprint, request
from six.moves.http_client import OK


class Minilog(object):
    """
    Flask-Minilog

    Documentation:
    https://flask-minilog.readthedocs.io

    API:
    http://mixu.net/minilog

    :param app: Flask app to initialize with. Defaults to `None`
    """

    app = None

    logger = None

    def __init__(self, app=None, blueprint=None, url_prefix=None, logger=None):
        if app is not None:
            self.init_app(app, blueprint, url_prefix, logger)

    def init_app(self, app, blueprint=None, url_prefix=None, logger=None):

        self.app = app

        blueprint = blueprint or Blueprint('minilog', __name__, url_prefix=url_prefix)
        blueprint.add_url_rule('/minilog', 'minilog', self.handle_logs, methods=('POST',))

        self.logger = logger or logging.getLogger(__name__)

    def handle_logs(self):
        """
        http://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-javascript/
        """

        # self.logger.info(request.get_data(as_text=True))

        client_id = request.args.get('client_id')
        logs = request.get_json()['logs']
        for log in logs:
            level = logging.getLevelName(log[1].upper())
            message = log[2]
            self.logger.log(level, '%s: %s', client_id, message)

        return self.app.response_class(status=OK)


# EOF
