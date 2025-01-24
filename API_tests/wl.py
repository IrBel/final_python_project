import pytest
import requests
from requests.exceptions import Timeout, RequestException
from jsonschema import validate
from unittest.mock import patch
from logger import get_logger

# Setup basic configuration for logging
logger = get_logger(__name__)


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
    logger.info("Starting test: test_get_post")
    try:
        response = requests.get(f"{base_url}/posts/1", headers=headers, timeout=5)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        post_data = response.json()
        validate(instance=post_data, schema=post_schema)

        logger.info(f"Response data validated successfully: {post_data}")
        assert post_data['id'] == 1
        logger.info("test_get_post passed.")

    except Timeout as e:
        logger.error(f"Timeout error occurred: {e}")
        pytest.fail(f"Request timed out: {e}")
    except RequestException as e:
        logger.error(f"Request exception occurred: {e}")
        pytest.fail(f"Request failed: {e}")


# POST using payload
def test_create_post(base_url, headers):
    logger.info("Starting test: test_create_post")
    payload = {
        "userId": 1,
        "title": "Test Title",
        "body": "Test Body"
    }
    response = requests.post(f"{base_url}/posts", json=payload, headers=headers)
    logger.info(f"POST response: {response.status_code}")

    assert response.status_code == 201
    post_data = response.json()
    validate(instance=post_data, schema=post_schema)

    logger.info(f"Response data validated successfully: {post_data}")
    assert payload.items() <= post_data.items()
    logger.info("test_create_post passed.")


# PUT
def test_update_post(base_url, headers):
    logger.info("Starting test: test_update_post")
    post_id = 1
    updated_payload = {
        "userId": 1,
        "title": "Updated Title",
        "body": "Updated Body"
    }
    response = requests.put(f"{base_url}/posts/{post_id}", json=updated_payload, headers=headers)
    logger.info(f"PUT response: {response.status_code}")

    assert response.status_code == 200
    post_data = response.json()
    validate(instance=post_data, schema=post_schema)
    logger.info(f"Response data validated successfully: {post_data}")

    assert updated_payload.items() <= post_data.items()
    logger.info("test_update_post passed.")


# DELETE
def test_delete_post(base_url, headers):
    logger.info("Starting test: test_delete_post")
    post_id = 1
    response = requests.delete(f"{base_url}/posts/{post_id}", headers=headers)
    logger.info(f"DELETE response: {response.status_code}")

    assert response.status_code == 200

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        check_response = requests.get(f"{base_url}/posts/{post_id}", headers=headers)
        assert check_response.status_code == 404
        logger.info("Post deletion confirmed.")

    logger.info("test_delete_post passed.")