import datetime

import bottle


def json_operation(f):
    def new_function(self, model_name, *args, **kwargs):
        model = self.models[model_name]
        data = bottle.request.json
        return f(self, model_name, model, data, *args, **kwargs)

    return new_function


class RestOperationsManager:
    def __init__(self, lazy_server):
        self.lazy_server = lazy_server
        self.models = lazy_server.models
        self.db = lazy_server.db

        self.create_routes()

    def create_routes(self):
        self.lazy_server.add_route('/api/<model_name>/', 'POST', callback=self.create)
        self.lazy_server.add_route('/api/<model_name>/<key>/', 'PATCH', callback=self.update)
        self.lazy_server.add_route('/api/<model_name>/<key>/', 'GET', callback=self.retrieve)
        self.lazy_server.add_route('/api/<model_name>/', 'GET', callback=self.list)

    def validate_model(self, *args):
        return self.lazy_server.validate_model(*args)

    @staticmethod
    def get_parameters_for_search(model, keys):
        key_fields = model['constraints']['keys']
        search_by = {}
        key_index = 0
        for field_name in key_fields:
            search_by[field_name] = keys[key_index]
            key_index += 1

        return search_by

    @json_operation
    def create(self, model_name, model, data):
        is_valid, errors = self.validate_model(model_name, data)

        if not is_valid:
            return bottle.HTTPResponse(status=400, body=errors)

        table = self.db[model_name]

        keys = model['constraints'].get('keys', None)
        if keys:
            search_by = self.get_parameters_for_search(model, [value for key, value in data.items() if key in keys])
            if table.find_one(**search_by):
                return bottle.HTTPResponse(status=400, body={'constraints': 'These fields must be unique: {}'.format(keys)})

        data['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        table.insert(data)
        return bottle.HTTPResponse(status=201, body=data)

    @staticmethod
    def update_table(model, table, data):
        key_fields = model['constraints']['keys']
        return table.update(data, key_fields)

    @json_operation
    def update(self, model_name, model, data, key):
        keys = key.split(',')
        is_valid, errors = self.validate_model(model_name, data, update=True)

        if not is_valid:
            return bottle.HTTPResponse(status=400, body=errors)

        table = self.db[model_name]

        search_by = self.get_parameters_for_search(model, keys)
        entry = table.find_one(**search_by)
        if not entry:
            return bottle.HTTPResponse(status=404, body={'constraints': 'Not found: {}'.format(search_by)})

        data.update(search_by)
        data['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.update_table(model, table, data)
        entry = table.find_one(**search_by)  # XXX: is there a "refresh_from_db", maybe?
        entry['updated_at'] = str(entry['updated_at'])
        return bottle.HTTPResponse(status=200, body=entry)

    def retrieve(self, model_name, key):
        keys = key.split(',')
        table = self.db[model_name]

        model = self.models[model_name]
        search_by = self.get_parameters_for_search(model, keys)
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
