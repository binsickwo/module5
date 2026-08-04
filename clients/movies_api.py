from custom_requester.custom_requester import CustomRequester
from config.base_urls import API_BASE_URL
from models.base_models import FindAllMoviesResponse, FindOneMovieResponse, MovieResponse

MOVIES_ENDPOINT = '/movies'


class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def get_movies(self, params=None, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status,
            **kwargs
        )


    def get_movies_typed(self, params=None, expected_status=200, **kwargs):
        response = self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status,
            **kwargs
        )
        return FindAllMoviesResponse(**response.json())



    def get_movie_by_id(self, movie_id, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
            **kwargs
        )
    def get_movie_by_id_typed(self, movie_id, expected_status=200, **kwargs):
        response = self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
            **kwargs
        )
        return FindOneMovieResponse(**response.json())


    def create_movie(self, movie_data, expected_status=201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status,
            **kwargs
        )

    def create_movie_typed(self, movie_data, expected_status=201, **kwargs):
        response = self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status,
            **kwargs
        )
        return MovieResponse(**response.json())

    def update_movie(self, movie_id, movie_data, expected_status=200, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=movie_data,
            expected_status=expected_status,
            **kwargs
        )

    def update_movie_typed(self, movie_id, movie_data, expected_status=200, **kwargs):
        response = self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=movie_data,
            expected_status=expected_status,
            **kwargs
        )

        return MovieResponse(**response.json())

    def delete_movie(self, movie_id, expected_status=200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
            **kwargs
        )

    def delete_movie_typed(self, movie_id, expected_status=200, **kwargs):
        response = self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
            **kwargs
        )
        return MovieResponse(**response.json())
