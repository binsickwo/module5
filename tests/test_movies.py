import random
import uuid
from datetime import datetime

import allure
import pytest

from db_models.user import UserDBModel
from utils.data_generator import DataGenerator

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("GET /movies")
class TestGetMovies:

    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Get all movies and verify response structure")
    @allure.description("Verify that the GET /movies endpoint returns proper pagination structure with movies list")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("testid", "GET-MOVIES-001")
    def test_get_all_movies(self, api_manager):
        response = api_manager.movies_api.get_movies_typed()
        assert hasattr(response, "movies")
        assert hasattr(response, "count")
        assert hasattr(response, "page")
        assert hasattr(response, "pageSize")
        assert hasattr(response, "pageCount")
        assert isinstance(response.movies, list)
        assert response.count > 0
        assert len(response.movies) > 0

    @pytest.mark.positive
    @pytest.mark.pagination
    @allure.title("Get movies with default pagination")
    @allure.description("Verify that default pagination returns page 1 with pageSize 10")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_default_pagination(self, api_manager):
        response = api_manager.movies_api.get_movies_typed()

        assert response.page == 1
        assert response.pageSize == 10

    @pytest.mark.parametrize("minPrice,maxPrice,location,genreId", [(random.randint(1,500),random.randint(501,1000),("MSK", "SPB"), random.randint(1,10))])
    @pytest.mark.positive
    @pytest.mark.filtering
    @allure.title("Get movies with multiple filters")
    @allure.description("Verify that movies can be filtered by price range, location, and genre simultaneously")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_filtered(self,common_user, minPrice, maxPrice, location, genreId):
        params = {"minPrice": minPrice, "maxPrice": maxPrice, "locations": location, "genreId": genreId}
        response = common_user.api.movies_api.get_movies_typed(params=params)


    @pytest.mark.positive
    @pytest.mark.pagination
    @allure.title("Get movies with custom pagination")
    @allure.description("Verify that custom pagination parameters (page 2, pageSize 5) work correctly")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_custom_pagination(self, api_manager):
        params = {"page": 2, "pageSize": 5}
        response = api_manager.movies_api.get_movies_typed(params=params)

        assert response.page == 2
        assert response.pageSize == 5
        assert len(response.movies) <= 5

    @pytest.mark.positive
    @pytest.mark.filtering
    @allure.title("Filter movies by genre")
    @allure.description("Verify that filtering by genreId returns only movies of that genre")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_filter_by_genre(self, api_manager):
        genre_id = 1
        params = {"genreId": genre_id}
        response = api_manager.movies_api.get_movies_typed(params=params)

        assert hasattr(response, "movies")
        for movie in response.movies:
            assert movie.genreId == genre_id

    @pytest.mark.positive
    @pytest.mark.filtering
    @allure.title("Filter movies by location MSK")
    @allure.description("Verify that filtering by location MSK returns only movies in Moscow")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_filter_by_location_msk(self, api_manager):
        params = {"locations": ["MSK"]}
        response = api_manager.movies_api.get_movies_typed(params=params)

        assert hasattr(response, "movies")
        for movie in response.movies:
            assert movie.location == "MSK"

    @pytest.mark.positive
    @pytest.mark.filtering
    @allure.title("Filter movies by location SPB")
    @allure.description("Verify that filtering by location SPB returns only movies in Saint Petersburg")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_filter_by_location_spb(self, api_manager):
        params = {"locations": ["SPB"]}
        response = api_manager.movies_api.get_movies_typed(params=params)

        assert hasattr(response, "movies")
        for movie in response.movies:
            assert movie.location == "SPB"

    @pytest.mark.positive
    @pytest.mark.filtering
    @allure.title("Filter movies by price range")
    @allure.description("Verify that filtering by minPrice and maxPrice returns movies within the specified price range")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_filter_by_price_range(self, api_manager):
        min_price = 200
        max_price = 500
        params = {"minPrice": min_price, "maxPrice": max_price}
        response = api_manager.movies_api.get_movies_typed(params=params)

        assert hasattr(response, "movies")
        for movie in response.movies:
            assert min_price <= movie.price <= max_price

    @pytest.mark.positive
    @pytest.mark.filtering
    @allure.title("Filter movies by published status")
    @allure.description("Verify that filtering by published=True returns only published movies")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_filter_by_published(self, api_manager):
        params = {"published": True}
        response = api_manager.movies_api.get_movies_typed(params=params)

        assert hasattr(response, "movies")
        for movie in response.movies:
            assert movie.published is True

    @pytest.mark.positive
    @pytest.mark.filtering
    @allure.title("Sort movies by createdAt ascending")
    @allure.description("Verify that sorting by createdAt in ascending order returns movies sorted from oldest to newest")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_sort_by_created_at_asc(self, api_manager):
        params = {"createdAt": "asc"}
        response = api_manager.movies_api.get_movies_typed(params=params)

        assert hasattr(response, "movies")
        if len(response.movies) > 1:
            for i in range(len(response.movies) - 1):
                assert response.movies[i].createdAt <= response.movies[i + 1].createdAt

    @pytest.mark.positive
    @pytest.mark.filtering
    @allure.title("Sort movies by createdAt descending")
    @allure.description("Verify that sorting by createdAt in descending order returns movies sorted from newest to oldest")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("testid", "GET-MOVIES-010")
    def test_get_movies_sort_by_created_at_desc(self, api_manager):
        params = {"createdAt": "desc"}
        response = api_manager.movies_api.get_movies_typed(params=params)

        assert hasattr(response, "movies")
        if len(response.movies) > 1:
            for i in range(len(response.movies) - 1):
                assert response.movies[i].createdAt >= response.movies[i + 1].createdAt

    @pytest.mark.negative
    @pytest.mark.validation
    @pytest.mark.edge_case
    @allure.title("Get movies with invalid page number")
    @allure.description("Verify that requesting page -1 returns 400 Bad Request")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("testid", "GET-MOVIES-011")
    def test_get_movies_invalid_page(self, api_manager):
        params = {"page": -1}
        api_manager.movies_api.get_movies(params=params, expected_status=400)

    @pytest.mark.negative
    @pytest.mark.validation
    @pytest.mark.edge_case
    @allure.title("Get movies with zero page size")
    @allure.description("Verify that requesting pageSize of 0 returns 400 Bad Request")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("testid", "GET-MOVIES-012")
    def test_get_movies_invalid_page_size(self, api_manager):
        params = {"pageSize": 0}
        api_manager.movies_api.get_movies(params=params, expected_status=400)

    @pytest.mark.negative
    @pytest.mark.validation
    @pytest.mark.edge_case
    @allure.title("Get movies with page size exceeding limit")
    @allure.description("Verify that requesting pageSize greater than 20 returns 400 Bad Request")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("testid", "GET-MOVIES-013")
    def test_get_movies_page_size_too_large(self, api_manager,common_user):
        params = {"pageSize": 21}
        #api_manager.movies_api.get_movies(params=params, expected_status=400)
        common_user.api.movies_api.get_movies(params=params,expected_status=400)


@allure.story("GET /movies/{id}")
class TestGetMovieById:
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Get movie by ID and verify all fields")
    @allure.description("Verify that a movie can be retrieved by ID and all fields match expected values")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("testid", "GET-MOVIE-001")
    def test_get_movie_by_id(self, api_manager, created_movie):

        response = api_manager.movies_api.get_movie_by_id_typed(created_movie["id"])

        assert response.id == created_movie["id"]
        assert response.name == created_movie["name"]
        assert response.price == created_movie["price"]
        assert response.description == created_movie["description"]
        assert response.imageUrl == created_movie["imageUrl"]
        assert response.location == created_movie["location"]
        assert response.published == created_movie["published"]
        assert response.genreId == created_movie["genreId"]
        assert response.genre.name == created_movie["genre"]["name"]
        assert response.createdAt == created_movie["createdAt"]
        assert response.rating == created_movie["rating"]

    @pytest.mark.positive
    @allure.title("Get movie by ID and verify reviews structure")
    @allure.description("Verify that movie reviews array contains proper structure with userId, rating, text, and user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("testid", "GET-MOVIE-002")
    def test_get_movie_by_id_reviews_structure(self, api_manager, created_movie):
        movie_id = created_movie["id"]

        response = api_manager.movies_api.get_movie_by_id_typed(movie_id)

        assert isinstance(response.reviews, list)
        if len(response.reviews) > 0:
            review = response.reviews[0]
            assert review.userId is not None
            assert 0 <= review.rating <= 10
            assert review.text is not None
            assert review.createdAt is not None
            assert review.user is not None

    @pytest.mark.negative
    @pytest.mark.edge_case
    @allure.title("Get movie by non-existent ID")
    @allure.description("Verify that requesting a non-existent movie ID returns 404 Not Found")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("testid", "GET-MOVIE-003")
    def test_get_movie_by_id_not_found(self, api_manager):
        non_existent_id = 999999
        api_manager.movies_api.get_movie_by_id(non_existent_id, expected_status=404)


@allure.story("POST /movies")
class TestCreateMovie:
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Create a new movie successfully")
    @allure.description("Verify that a new movie can be created with valid data and all fields are returned correctly")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("testid", "POST-MOVIE-001")
    def test_create_movie(self, api_manager, movie_data):
        response = api_manager.movies_api.create_movie(movie_data)
        data = response.json()

        assert data["name"] == movie_data["name"]
        assert data["description"] == movie_data["description"]
        assert data["price"] == movie_data["price"]
        assert data["location"] == movie_data["location"]
        assert data["published"] == movie_data["published"]
        assert data["genreId"] == movie_data["genreId"]
        assert "id" in data
        assert "createdAt" in data

        api_manager.movies_api.delete_movie(data["id"])

    @pytest.mark.negative
    @pytest.mark.auth
    @allure.title("Create movie with user privileges (403 Forbidden)")
    @allure.description("Verify that a regular user cannot create a movie and receives 403 Forbidden")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("testid", "POST-MOVIE-002")
    def test_privelege_error_user_creation(self, common_user, movie_data):
        response = common_user.api.movies_api.create_movie(movie_data,expected_status=403)

        data = response.json()

        assert data["statusCode"] == 403
        assert data["message"] == "Forbidden resource"

    @pytest.mark.negative
    @pytest.mark.auth
    @allure.title("Create movie without authentication (401 Unauthorized)")
    @allure.description("Verify that unauthenticated request to create movie returns 401 Unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("testid", "POST-MOVIE-003")
    def test_create_movie_without_auth(self, unauth_movies_api, movie_data):
        unauth_movies_api.create_movie(movie_data, expected_status=401)

    @pytest.mark.parametrize("mutation,expected_status", [
        ({"_delete": "name"}, 400),
        ({"_delete": "price"}, 400),
        ({"_delete": "description"}, 400),
        ({"_delete": "location"}, 400),
        ({"_delete": "genreId"}, 400),
        ({"location": "INVALID"}, 400),
        ({"name": ""}, 400),
    ], ids=["missing_name", "missing_price", "missing_description",
            "missing_location", "missing_genre_id", "invalid_location", "empty_name"])
    @pytest.mark.negative
    @pytest.mark.validation
    @allure.title("Create movie with invalid data")
    @allure.description("Verify that movie creation fails with 400 Bad Request for missing or invalid required fields")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("testid", "POST-MOVIE-004")
    def test_create_movie_invalid_data(self, api_manager, movie_data, mutation, expected_status):
        data = movie_data.copy()
        if "_delete" in mutation:
            del data[mutation["_delete"]]
        else:
            data.update(mutation)
        api_manager.movies_api.create_movie(data, expected_status=expected_status)


@allure.story("PATCH /movies/{id}")
class TestUpdateMovie:
    @pytest.mark.parametrize("field,new_value", [
        ("name", "Updated Movie Name"),
        ("price", 999),
        ("description", "Updated description for test"),
    ], ids=["name", "price", "description"])
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Update movie field successfully")
    @allure.description("Verify that individual movie fields (name, price, description) can be updated and persisted")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("testid", "PATCH-MOVIE-001")
    def test_update_movie_field(self, admin_auth, api_manager, created_movie, field, new_value):
        update_data = {field: new_value}
        response = api_manager.movies_api.update_movie(created_movie["id"], update_data)
        data = response.json()
        get_response = api_manager.movies_api.get_movie_by_id_typed(created_movie["id"])

        assert data[field] == new_value
        assert data["id"] == created_movie["id"]
        assert getattr(get_response, field) == new_value
        assert get_response.id == created_movie["id"]

    @pytest.mark.negative
    @pytest.mark.edge_case
    @allure.title("Update non-existent movie (404 Not Found)")
    @allure.description("Verify that updating a non-existent movie returns 404 Not Found")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("testid", "PATCH-MOVIE-002")
    def test_update_movie_not_found(self, admin_auth, api_manager):
        non_existent_id = 999999
        update_data = {"name": "Updated Name"}

        api_manager.movies_api.update_movie(non_existent_id, update_data, expected_status=404)

    @pytest.mark.negative
    @pytest.mark.auth
    @allure.title("Update movie without authentication (401 Unauthorized)")
    @allure.description("Verify that unauthenticated request to update movie returns 401 Unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("testid", "PATCH-MOVIE-003")
    def test_update_movie_without_auth(self, unauth_movies_api):
        update_data = {"name": "Updated Name"}

        unauth_movies_api.update_movie(1, update_data, expected_status=401)


@allure.story("DELETE /movies/{id}")
class TestDeleteMovie:
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Delete movie successfully")
    @allure.description("Verify that a movie can be deleted and returns 404 on subsequent GET request")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("testid", "DELETE-MOVIE-001")
    def test_delete_movie(self, api_manager, movie_data):
        create_response = api_manager.movies_api.create_movie(movie_data)
        movie_id = create_response.json()["id"]

        response = api_manager.movies_api.delete_movie(movie_id)
        data = response.json()

        assert data["id"] == movie_id

        api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)

    @pytest.mark.negative
    @pytest.mark.edge_case
    @allure.title("Delete non-existent movie (404 Not Found)")
    @allure.description("Verify that deleting a non-existent movie returns 404 Not Found")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("testid", "DELETE-MOVIE-002")
    def test_delete_movie_not_found(self, api_manager):
        non_existent_id = 999999

        api_manager.movies_api.delete_movie(non_existent_id, expected_status=404)

    @pytest.mark.negative
    @pytest.mark.auth
    @allure.title("Delete movie without authentication (401 Unauthorized)")
    @allure.description("Verify that unauthenticated request to delete movie returns 401 Unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("testid", "DELETE-MOVIE-003")
    def test_delete_movie_without_auth(self, unauth_movies_api):
        unauth_movies_api.delete_movie(1, expected_status=401)


@allure.story("Database Operations")
@pytest.mark.db
@allure.title("Create and delete user in database")
@allure.description("Verify that a user can be created in the database, retrieved, and then deleted")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("testid", "DB-USER-001")
def test_create_user_db(db_session):
    user_data = {
        "id": str(uuid.uuid4()),
        "email": DataGenerator.generate_random_email(),
        "full_name": "Test User",
        "password": "hashed_password",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "verified": False,
        "banned": False,
        "roles": ["USER"],
    }
    user = UserDBModel(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    db_session.delete(user)
    db_session.commit()

@pytest.mark.db
@pytest.mark.critical
@allure.title("Create movie in database and verify via API delete")
@allure.description("Verify that a movie created in database can be deleted via API and is no longer accessible")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("testid", "DB-MOVIE-001")
def test_create_movie_db(db_helper, movie_db_data, super_admin):

    with allure.step("check the movie is not existent in the database, before any checks"):
        movie_exists = db_helper.get_movie_by_name(movie_db_data["name"])
        assert movie_exists is None

    with allure.step("creating the movie in the database and then checking it exists in the database"):
        movie = db_helper.create_test_movie(movie_db_data)
        movie_exists = db_helper.get_movie_by_name(movie_db_data["name"])
        assert movie_exists is not None

    with allure.step("removing the movie from the database and checking it no longer exists in the database"):
        super_admin.api.movies_api.delete_movie(movie.id)
        movie_after_delete = db_helper.get_movie_by_id(movie.id)
        assert movie_after_delete is None



