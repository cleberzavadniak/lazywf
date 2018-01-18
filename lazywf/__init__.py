import yaml
from os import environ

import bottle
from cerberus import Validator
import dataset
from clint.textui import indent

from .logger import Logger
from .rest import RestOperationsManager


class TheLaziestWebFrameworkEVER:
    def __init__(self):
        self.DATABASE_URL = environ.get('DATABASE_URL', None)

        self.logger = Logger(self)

        # Bottle app:
        self.app = bottle.Bottle()

        self.load_models()
        self.db_connect()

        self.create_internal_routes()
        self.create_routes()
        self.load_rest_manager()

        self.enable_cors()

    def load_rest_manager(self):
        if self.models:
            self.rest_manager = RestOperationsManager(self)

    def add_cors_headers(self, response=None):
        response = response or bottle.response

        if self.cors_origins is None:
            return response

        the_headers = response.headers

        the_headers['Access-Control-Allow-Origin'] = self.cors_origins
        the_headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        the_headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

    def enable_cors(self):
        self.cors_origins = environ.get('CORS_ORIGINS', None)
        self.app.hook('after_request')(self.add_cors_headers)

    # ---------------------------------------
    # Models and Database:
    def load_models(self):
        try:
            return self.do_load_models()
        except FileNotFoundError:
            self.logger.warning('NOT loading models: models.yaml file does not exist.')
            self.models = None
            return

    def do_load_models(self):
        with open('models.yaml') as models_file:
            self.models = yaml.load(models_file)

    def db_connect(self):
        if self.DATABASE_URL and self.models:
            self.logger.info('Connecting to database')
            with indent(4):
                self.db = dataset.connect(self.DATABASE_URL)
                self.logger.info('Database URL: {}'.format(self.db.url))
        else:
            self.logger.warning('NOT connecting to database: DATABASE_URL environment variable is not set or no models definitions available.')
            self.db = None

    def get_table(self, table_name):
        return self.db[table_name]

    # -------------------
    def add_route(self, path, method, callback, **kwargs):
        self.logger.info('add_route: {} {}'.format(method, path))
        return self.app.route(path, method, callback=callback, **kwargs)

    def create_routes(self):
        # Child class can implement.
        pass

    def create_internal_routes(self):
        self.add_route('/static/<filename:path>', 'GET', callback=self.serve_static)

    def validate_model(self, name, data, update=False):
        if not data:
            return False, {"__all__": "No document provided."}

        schema = self.models[name]['validations']
        v = Validator(schema)
        return v.validate(data, update=update), v.errors

    # Error page:
    @bottle.error(404)  # TODO: check if this works properly.
    def error404(self, error):
        return 'Not found ({}).'.format(error)

    # Static files:
    def serve_static(self, filename):
        response = bottle.static_file(filename, root='static')
        self.add_cors_headers(response)
        return response

    # REST API:
    # Templates
    def render(self, template_name, context={}):
        return bottle.template('templates/{}'.format(template_name), **context)

    # Run the server!!!
    def run(self):
        port = int(environ.get('PORT', 8080))
        host = environ.get('HOST', 'localhost')
        debug_mode = environ.get('DEBUG', 'True') == 'True'
        return bottle.run(self.app, host=host, port=port, debug_mode=debug_mode)
