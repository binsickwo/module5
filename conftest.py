import pytest
import requests
from clients.api_manager import ApiManager
from clients.movies_api import MoviesApi
from config.admin_credentials import SuperAdminCreds
from constants.roles import Roles
from db_requester.db_helpers import DBHelper
from entities.user import User
from models.base_models import TestUser
from utils.data_generator import DataGenerator
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

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
    api_manager.auth_api.authenticate((SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD))
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
def movie_db_data():
    return DataGenerator.generate_movie_db_data()

@pytest.fixture()
def created_movie(admin_auth, api_manager, movie_data):
    response = api_manager.movies_api.create_movie(movie_data)
    movie = response.json()
    yield movie
    api_manager.movies_api.delete_movie(movie["id"])

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session()

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )
    super_admin.api.auth_api.authenticate(super_admin.creds)

    return super_admin


@pytest.fixture(scope="function")
def test_user() -> TestUser:
    password = DataGenerator.generate_random_password()
    return TestUser(
        email= DataGenerator.generate_random_email(),
        fullName = DataGenerator.generate_random_name(),
        password=  password,
        passwordRepeat=  password,
        roles= [Roles.USER]
    )


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.model_dump(mode='json')
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session

    admin_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.ADMIN.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }
