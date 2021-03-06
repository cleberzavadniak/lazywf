import pytest


from lazywf import TheLaziestWebFrameworkEVER


@pytest.fixture
def server():
    class MyTestServer(TheLaziestWebFrameworkEVER):
        def load_models(self):
            self.models = {}

        def db_connect(self):
            self.DATABASE_URL = 'sqlite:///:memory:'
            super().db_connect()

    return MyTestServer()
