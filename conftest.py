import pytest
import requests
from clients.api_manager import ApiManager
from clients.movies_api import MoviesApi
from config.admin_credentials import ADMIN_EMAIL, ADMIN_PASSWORD
from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    manager = ApiManager(session)
    return manager


@pytest.fixture(scope="session")
def admin_auth(api_manager):
    api_manager.auth_api.authenticate((ADMIN_EMAIL, ADMIN_PASSWORD))
    return api_manager


@pytest.fixture()
def unauth_movies_api():
    fresh_session = requests.Session()
    api = MoviesApi(fresh_session)
    yield api
    fresh_session.close()


@pytest.fixture()
def movie_data():
    return DataGenerator.generate_movie_data()


@pytest.fixture()
def created_movie(admin_auth, api_manager, movie_data):
    response = api_manager.movies_api.create_movie(movie_data)
    movie = response.json()
    yield movie
    api_manager.movies_api.delete_movie(movie["id"])

