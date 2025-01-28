import pytest
import requests
from requests.exceptions import Timeout, RequestException
from jsonschema import validate
from unittest.mock import patch
from core.logger import get_logger

# Initialize the logger
logger = get_logger(__name__)
logger.info(" API logger initialized successfully!")
logger.info("This is an info message.")
logger.debug("This is a debug message.")


@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
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
@pytest.mark.api
def test_get_post(base_url, headers):
    try:
        logger.debug("Starting log for test_get_post")
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
        logger.debug("test_get_post successfully passed")


# POST using payload
@pytest.mark.api
def test_create_post(base_url, headers):
    logger.debug("Starting log for test_create_post")
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
    logger.debug("test_create_post successfully passed")


# PUT
@pytest.mark.api
def test_update_post(base_url, headers):
    logger.debug("Starting log for test_update_post")
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
    logger.debug("test_update_post successfully passed")


# DELETE
@pytest.mark.api
def test_delete_post(base_url, headers):
    logger.debug("Starting log for test_delete_post")
    post_id = 101
    response = requests.delete(f"{base_url}/posts/{post_id}", headers=headers)

    assert response.status_code == 200
    # and confirming its removal using Mock.
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        check_response = requests.get(f"{base_url}/posts/{post_id}", headers=headers)
        assert check_response.status_code == 404
    logger.debug("test_delete_post successfully passed")

# pytest main.py -s

