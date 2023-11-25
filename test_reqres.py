import jsonschema
import requests

from utils import load_schema

#TODO проверку схемы ко всем тестам


base_url = "https://reqres.in/api"


def validate_schema(response, schema_name):
    schema = load_schema(schema_name)
    jsonschema.validate(response.json(), schema)


def test_get_users():
    response = requests.get(base_url+"/users")

    assert response.status_code == 200
    validate_schema(response, "get_users.json")


def test_get_users_per_page():
    response = requests.get(url=base_url+"/users", params={"per_page": 1})

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["per_page"] == 1
    validate_schema(response, "get_users.json")


def test_nonexisting_user():
    response = requests.get(url=base_url+"/users/23")

    assert response.status_code == 404


def test_headers():
    bearer = {"Authorization": "Bearer agagwg"}
    headers = {"Connection": "keep-alive"}
    headers.update(bearer)
    response = requests.get(url=base_url+"/users", headers=headers)

    assert response.headers.get("connection") == "keep-alive"
    assert response.status_code == 200
    validate_schema(response, "get_users.json")


def test_post_users_schema_validation():
    response = requests.post(
        url=base_url+"/users",
        json={
            "name": "morpheus",
            "job": "leader"
        }
    )

    assert response.status_code == 201
    validate_schema(response, "post_users.json")


def test_update_user():
    response = requests.put(
        url=base_url+"/users/2",
        json={
            "name": "morpheus",
            "job": "zion resident"
        }
    )

    assert response.status_code == 200
    print(response.json())
    assert response.json()["job"] == "zion resident"
    validate_schema(response, "put_users.json")


def test_delete_user():
    response = requests.delete(url=base_url+"/users/2")
    assert response.status_code == 204


def test_signup_success():
    response = requests.post(
        url=base_url+"/register",
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == 4
    assert response.json()["token"] == "QpwL5tke4Pnpja7X4"
    validate_schema(response, "post_register.json")


def test_signup_failure():
    response = requests.post(
        url=base_url+"/register",
        json={
            "email": "sydney@fife"
        }
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
    validate_schema(response, "post_register_error.json")


def test_login_success():
    response = requests.post(
        url=base_url+"/login",
        json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
    )

    assert response.status_code == 200
    assert response.json()["token"] == "QpwL5tke4Pnpja7X4"
    validate_schema(response, "post_login.json")


def test_login_failure():
    response = requests.post(
        url=base_url+"/login",
        json={
            "email": "peter@klaven"
        }
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
    validate_schema(response, "post_login_error.json")
