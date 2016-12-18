import bottle

from .logger import Logger
from .rest import RestOperationsManager
from .database import DatabaseManager


class TheLaziestWebFrameworkEVER:
    def __init__(self):
        self.logger = Logger(self)
        self.base_init()
        self.db_manager = DatabaseManager(self)
        self.rest_manager = RestOperationsManager(self, self.db_manager)

    def base_init(self):
        # Bottle app:
        self.app = bottle.Bottle()

        self.create_internal_routes()
        self.create_routes()

    # ---------------------------------------
    def add_route(self, path, method, callback, **kwargs):
        return self.app.route(path, method, callback=callback, **kwargs)

    def create_routes(self):
        # Child class can implement.
        pass

    def create_internal_routes(self):
        self.add_route('/static/<filename>', 'GET', callback=self.serve_static)

    # Error page:
    @bottle.error(404)  # TODO: check if this works properly.
    def error404(self, error):
        return 'Not found ({}).'.format(error)

    # Static files:
    def serve_static(self, filename):
        return bottle.static_file(filename, root='static')

    # Templates
    def render(self, template_name, context={}):
        return bottle.template('templates/{}'.format(template_name), **context)

    # Run the server!!!
    def run(self):
        return bottle.run(self.app, host='localhost', port=8080, debug_mode=True)
