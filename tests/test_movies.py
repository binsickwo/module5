import pytest


class TestGetMovies:
    def test_get_all_movies(self, api_manager):
        response = api_manager.movies_api.get_movies()
        data = response.json()

        assert "movies" in data
        assert "count" in data
        assert "page" in data
        assert "pageSize" in data
        assert "pageCount" in data
        assert isinstance(data["movies"], list)
        assert data["count"] > 0
        assert len(data["movies"]) > 0

    def test_get_movies_default_pagination(self, api_manager):
        response = api_manager.movies_api.get_movies()
        data = response.json()

        assert data["page"] == 1
        assert data["pageSize"] == 10

    def test_get_movies_custom_pagination(self, api_manager):
        params = {"page": 2, "pageSize": 5}
        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        assert data["page"] == 2
        assert data["pageSize"] == 5
        assert len(data["movies"]) <= 5

    def test_get_movies_filter_by_genre(self, api_manager):
        genre_id = 1
        params = {"genreId": genre_id}
        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        assert "movies" in data
        for movie in data["movies"]:
            assert movie["genreId"] == genre_id

    def test_get_movies_filter_by_location_msk(self, api_manager):
        params = {"locations": ["MSK"]}
        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        assert "movies" in data
        for movie in data["movies"]:
            assert movie["location"] == "MSK"

    def test_get_movies_filter_by_location_spb(self, api_manager):
        params = {"locations": ["SPB"]}
        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        assert "movies" in data
        for movie in data["movies"]:
            assert movie["location"] == "SPB"

    def test_get_movies_filter_by_price_range(self, api_manager):
        min_price = 200
        max_price = 500
        params = {"minPrice": min_price, "maxPrice": max_price}
        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        assert "movies" in data
        for movie in data["movies"]:
            assert min_price <= movie["price"] <= max_price

    def test_get_movies_filter_by_published(self, api_manager):
        params = {"published": True}
        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        assert "movies" in data
        for movie in data["movies"]:
            assert movie["published"] is True

    def test_get_movies_sort_by_created_at_asc(self, api_manager):
        params = {"createdAt": "asc"}
        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        assert "movies" in data
        movies = data["movies"]
        if len(movies) > 1:
            for i in range(len(movies) - 1):
                assert movies[i]["createdAt"] <= movies[i + 1]["createdAt"]

    def test_get_movies_sort_by_created_at_desc(self, api_manager):
        params = {"createdAt": "desc"}
        response = api_manager.movies_api.get_movies(params=params)
        data = response.json()

        assert "movies" in data
        movies = data["movies"]
        if len(movies) > 1:
            for i in range(len(movies) - 1):
                assert movies[i]["createdAt"] >= movies[i + 1]["createdAt"]

    def test_get_movies_invalid_page(self, api_manager):
        params = {"page": -1}
        api_manager.movies_api.get_movies(params=params, expected_status=400)

    def test_get_movies_invalid_page_size(self, api_manager):
        params = {"pageSize": 0}
        api_manager.movies_api.get_movies(params=params, expected_status=400)

    def test_get_movies_page_size_too_large(self, api_manager):
        params = {"pageSize": 21}
        api_manager.movies_api.get_movies(params=params, expected_status=400)


class TestGetMovieById:
    def test_get_movie_by_id(self, api_manager, created_movie):

        response = api_manager.movies_api.get_movie_by_id(created_movie["id"])
        data = response.json()

        assert data["id"] == created_movie["id"]
        assert data["name"] == created_movie["name"]
        assert data["price"] == created_movie["price"]
        assert data["description"] == created_movie["description"]
        assert data["imageUrl"] == created_movie["imageUrl"]
        assert data["location"] == created_movie["location"]
        assert data["published"] == created_movie["published"]
        assert data["genreId"] == created_movie["genreId"]
        assert data["genre"] == created_movie["genre"]
        assert data["createdAt"] == created_movie["createdAt"]
        assert data["rating"] == created_movie["rating"]

    def test_get_movie_by_id_reviews_structure(self, api_manager, created_movie):
        movie_id = created_movie["id"]

        response = api_manager.movies_api.get_movie_by_id(movie_id)
        data = response.json()

        assert isinstance(data["reviews"], list)
        if len(data["reviews"]) > 0:
            review = data["reviews"][0]
            assert "userId" in review
            assert "rating" in review
            assert "text" in review
            assert "createdAt" in review
            assert "user" in review

    def test_get_movie_by_id_not_found(self, api_manager):
        non_existent_id = 999999
        api_manager.movies_api.get_movie_by_id(non_existent_id, expected_status=404)


class TestCreateMovie:
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
    def test_create_movie_invalid_data(self, api_manager, movie_data, mutation, expected_status):
        data = movie_data.copy()
        if "_delete" in mutation:
            del data[mutation["_delete"]]
        else:
            data.update(mutation)
        api_manager.movies_api.create_movie(data, expected_status=expected_status)


class TestUpdateMovie:
    @pytest.mark.parametrize("field,new_value", [
        ("name", "Updated Movie Name"),
        ("price", 999),
        ("description", "Updated description for test"),
    ], ids=["name", "price", "description"])
    def test_update_movie_field(self, admin_auth, api_manager, created_movie, field, new_value):
        update_data = {field: new_value}
        response = api_manager.movies_api.update_movie(created_movie["id"], update_data)
        data = response.json()
        get_response = api_manager.movies_api.get_movie_by_id(created_movie["id"])

        assert data[field] == new_value
        assert data["id"] == created_movie["id"]
        assert get_response.json()[field] == new_value
        assert get_response.json()["id"] == created_movie["id"]

    def test_update_movie_not_found(self, admin_auth, api_manager):
        non_existent_id = 999999
        update_data = {"name": "Updated Name"}

        api_manager.movies_api.update_movie(non_existent_id, update_data, expected_status=404)

    def test_update_movie_without_auth(self, unauth_movies_api):
        update_data = {"name": "Updated Name"}

        unauth_movies_api.update_movie(1, update_data, expected_status=401)


class TestDeleteMovie:
    def test_delete_movie(self, api_manager, movie_data):
        create_response = api_manager.movies_api.create_movie(movie_data)
        movie_id = create_response.json()["id"]

        response = api_manager.movies_api.delete_movie(movie_id)
        data = response.json()

        assert data["id"] == movie_id

        api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)

    def test_delete_movie_not_found(self, api_manager):
        non_existent_id = 999999

        api_manager.movies_api.delete_movie(non_existent_id, expected_status=404)

    def test_delete_movie_without_auth(self, unauth_movies_api):
        unauth_movies_api.delete_movie(1, expected_status=401)
