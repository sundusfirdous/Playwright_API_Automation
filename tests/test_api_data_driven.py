
import pytest
import json
import csv
import os

from dotenv import load_dotenv
from playwright.sync_api import Playwright, APIRequestContext


# ==========================================
# ENVIRONMENT CONFIGURATION
# ==========================================

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")

# Validate environment variables
assert BASE_URL, "BASE_URL is missing in .env"
assert API_USERNAME, "API_USERNAME is missing in .env"
assert API_PASSWORD, "API_PASSWORD is missing in .env"


# ==========================================
# AUTHENTICATION - GENERATE BEARER TOKEN
# ==========================================

def get_auth_token(playwright: Playwright):

    request = playwright.request.new_context(
        base_url=BASE_URL
    )

    login_payload = {
        "username": API_USERNAME,
        "password": API_PASSWORD
    }

    response = request.post(
        "/auth/login",
        data=login_payload,
        headers={"Content-Type": "application/json"}
    )

    assert response.status == 200

    token = response.json()["accessToken"]

    request.dispose()

    return token


# ==========================================
# FIXTURE - AUTHENTICATED API REQUEST
# ==========================================

@pytest.fixture
def api_request(playwright: Playwright):

    token = get_auth_token(playwright)

    request = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )

    yield request

    request.dispose()


# ==========================================
# READ JSON TEST DATA
# ==========================================

def get_JSON_Data():

    with open("./test_data/data.json", "r") as file:
        data = json.load(file)

    return [
        (item["firstName"], item["lastName"], item["age"])
        for item in data
    ]


# ==========================================
# READ CSV TEST DATA
# ==========================================

def get_CSV_Data():

    data = []

    with open("./test_data/data.csv", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            data.append((
                row["firstName"],
                row["lastName"],
                int(row["age"])
            ))

    return data


# ==========================================
# GET API - POSITIVE TESTING
# ==========================================

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get(api_request: APIRequestContext, user_id):

    response = api_request.get(f"/users/{user_id}")

    assert response.status == 200

    data = response.json()

    assert data["id"] == user_id

    print("\nGET Response:", data)


# ==========================================
# POST API - JSON DATA-DRIVEN TESTING
# ==========================================

@pytest.mark.parametrize(
    "firstName, lastName, age",
    get_JSON_Data()
)
def test_post(api_request: APIRequestContext, firstName, lastName, age):

    response = api_request.post(
        "/users/add",
        data={
            "firstName": firstName,
            "lastName": lastName,
            "age": age
        }
    )

    assert response.status == 201

    data = response.json()

    assert data["firstName"] == firstName
    assert data["lastName"] == lastName
    assert data["age"] == age

    print("\nPOST Response:", data)


# ==========================================
# PUT API - CSV DATA-DRIVEN TESTING
# ==========================================

@pytest.mark.parametrize(
    "firstName, lastName, age",
    get_CSV_Data()
)
def test_put(api_request: APIRequestContext, firstName, lastName, age):

    response = api_request.put(
        "/users/2",
        data={
            "firstName": firstName,
            "lastName": lastName,
            "age": age
        }
    )

    assert response.status == 200

    data = response.json()

    assert data["firstName"] == firstName
    assert data["lastName"] == lastName
    assert data["age"] == age

    print("\nPUT Response:", data)


# ==========================================
# PATCH API - PARAMETERIZED TESTING
# ==========================================

@pytest.mark.parametrize("age", [25, 30, 35])
def test_patch(api_request: APIRequestContext, age):

    response = api_request.patch(
        "/users/2",
        data={"age": age}
    )

    assert response.status == 200

    data = response.json()

    assert data["age"] == age

    print("\nPATCH Response:", data)


# ==========================================
# DELETE API - PARAMETERIZED TESTING
# ==========================================

@pytest.mark.parametrize("user_id", [2, 3])
def test_delete(api_request: APIRequestContext, user_id):

    response = api_request.delete(f"/users/{user_id}")

    assert response.status == 200

    data = response.json()

    assert data["isDeleted"] is True

    print("\nDELETE Response:", data)


# ==========================================
# NEGATIVE GET - INVALID USER ID
# ==========================================

@pytest.mark.parametrize("user_id", [9999, 10000, 0])
def test_get_invalid_user(api_request: APIRequestContext, user_id):

    response = api_request.get(f"/users/{user_id}")

    assert response.status == 404

    print("\nStatus:", response.status)
    print("Response:", response.text())


# ==========================================
# NEGATIVE TEST - INVALID BEARER TOKEN
# ==========================================

def test_invalid_token(playwright: Playwright):

    request = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Authorization": "Bearer invalid_token_123",
            "Content-Type": "application/json"
        }
    )

    try:
        response = request.get("/auth/me")

        assert response.status == 401

        print("\nStatus:", response.status)
        print("Response:", response.text())

    finally:
        request.dispose()


# ==========================================
# NEGATIVE POST - MISSING FIELDS
# ==========================================

@pytest.mark.parametrize("request_body", [
    {},
    {"firstName": "Sundus"},
    {"lastName": "Firdous"},
    {"age": 25}
])
def test_post_missing_fields(api_request: APIRequestContext, request_body):

    response = api_request.post(
        "/users/add",
        data=request_body
    )

    print("\nRequest:", request_body)
    print("Status:", response.status)
    print("Response:", response.text())

    # DummyJSON may accept incomplete data.
    assert response.status in [200, 201, 400, 422]
