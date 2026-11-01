import pytest
from playwright.sync_api import Playwright

from config import BASE_URL, USERNAME, PASSWORD


@pytest.fixture(scope="session")
def login_token(playwright: Playwright):

    request = playwright.request.new_context(
        base_url=BASE_URL
    )

    response = request.post(
        "/auth/login",
        data={
            "username": USERNAME,
            "password": PASSWORD,
            "expiresInMins": 30
        }
    )

    assert response.status == 200

    response_data = response.json()
    token = response_data["accessToken"]

    print("\nToken extracted successfully!")

    request.dispose()

    return token


@pytest.fixture(scope="session")
def api_request(playwright, login_token):

    request = playwright.request.new_context(
        base_url=BASE_URL,

        extra_http_headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {login_token}",
            "X-Test-Environment": "QA"
        }
    )

    yield request

    request.dispose()