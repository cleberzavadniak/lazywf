#!env python3

from lazywf import TheMostLazyWebFrameworkEVER


class Lazy(TheMostLazyWebFrameworkEVER):
    def create_routes(self):
        self.add_route('/', 'GET', self.index)

    def index(self):
        return self.render('index.html')

Lazy().run()
