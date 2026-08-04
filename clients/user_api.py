from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL
from models.base_models import TestUser, RegisterUserResponse


class UserApi(CustomRequester):
    def __init__(self, session):
        self.session = session
        super().__init__(session, AUTH_BASE_URL)

    def get_user(self, user_locator,expected_status_code=200):
        return self.send_request("GET", f"/user/{user_locator}",expected_status=expected_status_code)

    def get_user_typed(self, user_locator, expected_status_code=200):
        response = self.send_request("GET", f"/user/{user_locator}", expected_status=expected_status_code)
        return RegisterUserResponse(**response.json())

    def create_user(self, user_data: TestUser, expected_status=201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint="/user",
            data=user_data,
            expected_status=expected_status,
            **kwargs
        )
