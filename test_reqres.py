import jsonschema
import pytest
import requests

from utils import load_schema

base_url = "https://reqres.in/api"


@pytest.fixture
def user_data():
    return {
        "name": "morpheus",
        "job": "zion resident"
    }


@pytest.fixture
def credentials():
    return {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }


@pytest.fixture
def incomplete_credentials():
    return {
        "email": "eve.holt@reqres.in",
    }


def validate_schema(response, schema_name):
    schema = load_schema(schema_name)
    jsonschema.validate(response.json(), schema)


def should_keep_alive_connection(response):
    assert response.headers.get("connection") == "keep-alive"


def test_get_users():
    response = requests.get(base_url+"/users")

    assert response.status_code == 200
    validate_schema(response, "get_users.json")
    should_keep_alive_connection(response)


def test_get_users_per_page():
    response = requests.get(url=base_url+"/users", params={"per_page": 1})

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["per_page"] == 1
    validate_schema(response, "get_users.json")
    should_keep_alive_connection(response)


def test_nonexisting_user():
    response = requests.get(url=base_url+"/users/23")

    assert response.status_code == 404
    should_keep_alive_connection(response)


def test_headers():
    bearer = {"Authorization": "Bearer agagwg"}
    headers = {"Connection": "keep-alive"}
    headers.update(bearer)
    response = requests.get(url=base_url+"/users", headers=headers)

    assert response.status_code == 200
    validate_schema(response, "get_users.json")
    should_keep_alive_connection(response)


def test_create_user(user_data):
    response = requests.post(
        url=base_url+"/users",
        json=user_data
    )

    assert response.status_code == 201
    validate_schema(response, "post_users.json")
    should_keep_alive_connection(response)
    assert response.json()["name"] == user_data["name"]
    assert response.json()["job"] == user_data["job"]


def test_update_user(user_data):
    response = requests.put(
        url=base_url+"/users/2",
        json=user_data
    )

    assert response.status_code == 200
    validate_schema(response, "put_users.json")
    should_keep_alive_connection(response)
    assert response.json()["job"] == user_data["job"]


def test_delete_user():
    response = requests.delete(url=base_url+"/users/2")

    assert response.status_code == 204
    should_keep_alive_connection(response)


def test_signup_success(credentials):
    response = requests.post(
        url=base_url+"/register",
        json=credentials
    )

    assert response.status_code == 200
    assert response.json()["id"] == 4
    assert response.json()["token"] == "QpwL5tke4Pnpja7X4"
    validate_schema(response, "post_register.json")
    should_keep_alive_connection(response)


def test_signup_failure(incomplete_credentials):
    response = requests.post(
        url=base_url+"/register",
        json=incomplete_credentials
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
    validate_schema(response, "post_register_error.json")
    should_keep_alive_connection(response)


def test_login_success(credentials):
    response = requests.post(
        url=base_url+"/login",
        json=credentials
    )

    assert response.status_code == 200
    assert response.json()["token"] == "QpwL5tke4Pnpja7X4"
    validate_schema(response, "post_login.json")
    should_keep_alive_connection(response)


def test_login_failure(incomplete_credentials):
    response = requests.post(
        url=base_url+"/login",
        json=incomplete_credentials
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
    validate_schema(response, "post_login_error.json")
    should_keep_alive_connection(response)
