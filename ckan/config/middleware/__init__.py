# encoding: utf-8

"""WSGI app initialization"""

from ckan.types import CKANApp
from ckan.common import CKANConfig
import logging

from ckan.config.environment import load_environment
from ckan.config.middleware.flask_app import make_flask_stack
from typing import Optional

from flask.ctx import RequestContext


log = logging.getLogger(__name__)

# This is a test Flask request context to be used internally.
# Do not use it!
_internal_test_request_context: Optional[RequestContext] = None


def make_app(conf: CKANConfig) -> CKANApp:
    '''
    Initialise both the pylons and flask apps, and wrap them in dispatcher
    middleware.
    '''

    load_environment(conf)

    flask_app = make_flask_stack(conf)

    # Set this internal test request context with the configured environment so
    # it can be used when calling url_for from tests
    global _internal_test_request_context
    _internal_test_request_context = flask_app._wsgi_app.test_request_context()

    return flask_app
