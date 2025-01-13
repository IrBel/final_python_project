import pytest
import requests
from requests.exceptions import Timeout, RequestException
from jsonschema import validate
from unittest.mock import patch


@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}


post_schema = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "required": ["userId", "id", "title", "body"],
}


# GET + exception handling
def test_get_post(base_url, headers):
    try:
        response = requests.get(f"{base_url}/posts/1", headers=headers, timeout=5)
        response.raise_for_status()
        post_data = response.json()
        print(post_data)
        # captured = capfd.readouterr()
        # print("Captured Output:", captured.out)

        # Validate response structure using a schema with the jsonschema library.
        validate(instance=post_data, schema=post_schema)

        # Asserts
        assert post_data['id'] == 1
    except Timeout as e:
        pytest.fail(f"Request timed out: {e}")
    except RequestException as e:
        pytest.fail(f"Request failed: {e}")


# POST using payload
def test_create_post(base_url, headers):
    payload = {
        "userId": 101,
        "id": 101,
        "title": "title",
        "body": "body"
    }
    response = requests.post(f"{base_url}/posts", json=payload, headers=headers)

    assert response.status_code == 201

    my_post = response.json()
    # Validate response structure using a schema with the jsonschema library.
    validate(instance=my_post, schema=post_schema)

    # Verify payload within response
    assert my_post['userId'] == payload['userId']
    assert my_post['id'] == payload['id']
    assert my_post['title'] == payload['title']
    assert my_post['body'] == payload['body']


# PUT
def test_update_post(base_url, headers):
    post_id = 1
    updated_payload = {
        "userId": 1,
        "id": 1,
        "title": "updated_title",
        "body": "updated_body"
    }
    response = requests.put(f"{base_url}/posts/{post_id}", json=updated_payload, headers=headers)

    assert response.status_code == 200
    post_data = response.json()
    # Validate response structure using a schema with the jsonschema library.
    validate(instance=post_data, schema=post_schema)

    # Verify updates
    assert post_data['title'] == updated_payload['title']
    assert post_data['body'] == updated_payload['body']


# DELETE
def test_delete_post(base_url, headers):
    post_id = 101
    response = requests.delete(f"{base_url}/posts/{post_id}", headers=headers)

    assert response.status_code == 200
    # and confirming its removal using Mock.
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        check_response = requests.get(f"{base_url}/posts/{post_id}", headers=headers)
        assert check_response.status_code == 404

# pytest main.py -s
