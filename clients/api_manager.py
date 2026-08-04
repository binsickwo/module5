from clients.auth_api import AuthApi
from clients.movies_api import MoviesApi


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthApi(session)
        self.movies_api = MoviesApi(session)


