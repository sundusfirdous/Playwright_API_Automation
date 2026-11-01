def test_get_api(playwright):

    request = playwright.request.new_context(
        base_url="https://dummyjson.com"
    )

    response = request.get("/users/2")

    assert response.status == 200

    json_data = response.json()

    print("\nGET Response:", json_data)

    assert json_data["id"] == 2

    request.dispose()

def test_post_api(api_request):

    payload = {
        "firstName": "Alice",
        "lastName": "QA",
        "age": 25
    }

    response = api_request.post(
        "/users/add",
        data=payload
    )

    assert response.status == 201

    json_data = response.json()

    print("\nPOST Response:", json_data)

    assert json_data["firstName"] == "Alice"

def test_put_api(api_request):

    payload = {
        "firstName": "Emily Updated",
        "lastName": "QA Engineer",
        "age": 30
    }

    response = api_request.put(
        "/users/2",
        data=payload
    )

    assert response.status == 200

    json_data = response.json()

    print("\nPUT Response:", json_data)

    assert json_data["firstName"] == "Emily Updated"

def test_patch_api(api_request):

    payload = {
        "age": 35
    }

    response = api_request.patch(
        "/users/2",
        data=payload
    )

    assert response.status == 200

    json_data = response.json()

    print("\nPATCH Response:", json_data)

    assert json_data["age"] == 35

def test_delete_api(api_request):

    response = api_request.delete(
        "/users/2"
    )

    assert response.status == 200

    json_data = response.json()

    print("\nDELETE Response:", json_data)

    assert json_data["isDeleted"] is True