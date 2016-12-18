import yaml

from cerberus import Validator


class ModelManager:
    def __init__(self, lazy_server):
        self.lazy_server = lazy_server
        self.load_models()

    def load_models(self):
        with open('models.yaml') as models_file:
            self.models = yaml.load(models_file)

    def validate_model(self, name, data, update=False):
        schema = self.models[name]['validations']
        v = Validator(schema)
        return v.validate(data, update=update), v.errors
