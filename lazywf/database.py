from os import environ

import dataset
from clint.textui import indent


class DatabaseManager:
    def __init__(self, lazy_server):
        self.lazy_server = lazy_server
        self.DATABASE_URL = environ.get('DATABASE_URL', None)

        self.db_connect()

    def db_connect(self):
        if self.DATABASE_URL:
            self.logger.info('Connecting to database')
            with indent(4):
                self.db = dataset.connect(self.DATABASE_URL)
                self.logger.info('Database URL: {}'.format(self.db.url))
        else:
            self.logger.warning('NOT connecting to database: DATABASE_URL environment variable is not set.')
            self.db = None

    def get_table(self, table_name):
        return self.db[table_name]
