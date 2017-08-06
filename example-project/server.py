#!env python3

from lazywf import TheLaziestWebFrameworkEVER


class Lazy(TheLaziestWebFrameworkEVER):
    def create_routes(self):
        self.add_route('/', 'GET', self.index)

    def index(self):
        return self.render('index.html')

Lazy().run()
