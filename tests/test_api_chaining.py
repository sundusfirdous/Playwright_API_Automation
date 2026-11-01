import pytest
import json
import csv
from playwright.sync_api import APIRequestContext


# Read JSON Data
def get_JSON_Data():

    with open("./test_data/data.json", "r") as file:
        data = json.load(file)

    return [
        (item["firstName"], item["lastName"], item["age"])
        for item in data
    ]


# Read CSV Data
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


# POST - JSON Data
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


# GET - CSV Data
@pytest.mark.parametrize(
    "user_id",
    [1, 2, 3]
)
def test_get(api_request: APIRequestContext, user_id):

    response = api_request.get(f"/users/{user_id}")

    assert response.status == 200

    data = response.json()

    assert data["id"] == user_id


# PUT - CSV Data
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


# PATCH
@pytest.mark.parametrize(
    "age",
    [25, 30, 35]
)
def test_patch(api_request: APIRequestContext, age):

    response = api_request.patch(
        "/users/2",
        data={"age": age}
    )

    assert response.status == 200

    data = response.json()

    assert data["age"] == age


# DELETE
@pytest.mark.parametrize(
    "user_id",
    [2, 3]
)
def test_delete(api_request: APIRequestContext, user_id):

    response = api_request.delete(f"/users/{user_id}")

    assert response.status == 200

    data = response.json()

    assert data["isDeleted"] is True

# Negative GET - Invalid User ID
@pytest.mark.parametrize("user_id", [9999, 10000, 0])
def test_get_invalid_user(api_request: APIRequestContext, user_id):

    response = api_request.get(f"/users/{user_id}")

    assert response.status == 404

    print("Status:", response.status)
    print("Response:", response.text())

# Negative Test - Invalid Bearer Token
def test_invalid_token(playwright):

    request = playwright.request.new_context(
        base_url="https://dummyjson.com",
        extra_http_headers={
            "Authorization": "Bearer invalid_token_123"
        }
    )

    response = request.get("/auth/me")

    assert response.status == 401

    print("Status:", response.status)
    print("Response:", response.text())

    request.dispose()

# Negative POST - Missing Mandatory Fields
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

    print("Request:", request_body)
    print("Status:", response.status)
    print("Response:", response.text())

    assert response.status in [200, 201, 400, 422]