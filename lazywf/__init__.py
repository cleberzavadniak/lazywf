import bottle
from cerberus import Validator
import yaml
import dataset


def json_operation(f):
    def new_function(self, model_name, *args, **kwargs):
        model = self.models[model_name]
        data = bottle.request.json
        return f(self, model_name, model, data, *args, **kwargs)

    return new_function


class TheLaziestWebFrameworkEVER:
    def __init__(self):
        # Bottle app:
        self.app = bottle.Bottle()

        self.load_models()
        self.db_connect()

        self.create_internal_routes()
        self.create_routes()

    def load_models(self):
        with open('models.yaml') as models_file:
            self.models = yaml.load(models_file)

    def db_connect(self):
        self.db = dataset.connect()

    def add_route(self, path, method, callback, **kwargs):
        return self.app.route(path, method, callback=callback, **kwargs)

    def create_routes(self):
        pass

    def create_internal_routes(self):
        self.add_route('/static/<filename>', 'GET', callback=self.serve_static)
        self.add_route('/api/<model_name>/', 'POST', callback=self.create)
        self.add_route('/api/<model_name>/<key>/', 'PATCH', callback=self.update)
        self.add_route('/api/<model_name>/<key>/', 'GET', callback=self.retrieve)
        self.add_route('/api/<model_name>/', 'GET', callback=self.list)

    def validate_model(self, name, data, update=False):
        schema = self.models[name]['validations']
        v = Validator(schema)
        return v.validate(data, update=update), v.errors

    # Error page:
    @bottle.error(404)  # TODO: check if this works properly.
    def error404(self, error):
        return 'Not found ({}).'.format(error)

    # Static files:
    def serve_static(self, filename):
        return bottle.static_file(filename, root='static')

    # REST API:

    @json_operation
    def create(self, model_name, model, data):
        is_valid, errors = self.validate_model(model_name, data)

        if not is_valid:
            return bottle.HTTPResponse(status=400, body=errors)

        table = self.db[model_name]

        if 'unique' in model['constraints']:
            fields = model['constraints']['unique']
            search_by = {}
            for field_name in fields:
                search_by[field_name] = data[field_name]

            if table.find_one(**search_by):
                return bottle.HTTPResponse(status=400, body={'constraints': 'These fields must be unique: {}'.format(fields)})

        table.insert(data)
        return bottle.HTTPResponse(status=201, body=data)

    @json_operation
    def update(self, model_name, model, data, key):
        keys = key.split(',')
        is_valid, errors = self.validate_model(model_name, data, update=True)

        if not is_valid:
            return bottle.HTTPResponse(status=400, body=errors)

        table = self.db[model_name]

        key_fields = model['constraints']['keys']
        search_by = {}
        key_index = 0
        for field_name in key_fields:
            search_by[field_name] = keys[key_index]
            key_index += 1

        entry = table.find_one(**search_by)
        if not entry:
            return bottle.HTTPResponse(status=404, body={'constraints': 'Not found: {}'.format(search_by)})

        data.update(search_by)
        print('table.update({}, {})'.format(data, key_fields))
        table.update(data, key_fields)
        entry = table.find_one(**search_by)  # XXX: is there a "refresh_from_db", maybe?
        return bottle.HTTPResponse(status=200, body=entry)

    def retrieve(self, model_name, key):
        keys = key.split(',')
        table = self.db[model_name]

        model = self.models[model_name]
        key_fields = model['constraints']['keys']
        search_by = {}
        key_index = 0
        for field_name in key_fields:
            search_by[field_name] = keys[key_index]
            key_index += 1

        entry = table.find_one(**search_by)
        if not entry:
            return bottle.HTTPResponse(status=404, body={'constraints': 'Not found: {}'.format(search_by)})

        return bottle.HTTPResponse(status=200, body=entry)

    def list(self, model_name):
        table = self.db[model_name]
        results = {
            'results': [x for x in table],
        }
        return bottle.HTTPResponse(status=200, body=results)

    # Templates
    def render(self, template_name, context={}):
        return bottle.template('templates/{}'.format(template_name), **context)

    # Run the server!!!
    def run(self):
        return bottle.run(self.app, host='localhost', port=8080)
