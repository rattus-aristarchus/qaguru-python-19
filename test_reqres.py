import jsonschema
import requests

from utils import load_schema


def test_get_users_status_code_is_ok():
    response = requests.get(url="https://reqres.in/api/users")

    assert response.status_code == 200


def test_get_users_per_page():
    response = requests.get(url="https://reqres.in/api/users", params={"per_page": 1})

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["per_page"] == 1


def test_nonexisting_user():
    response = requests.get(url="https://reqres.in/api/users/23")

    assert response.status_code == 404


def test_headers():
    bearer = {"Authorization": "Bearer agagwg"}
    headers = {"Connection": "keep-alive"}
    headers.update(bearer)
    response = requests.get(url="https://reqres.in/api/users", headers=headers)

    assert response.headers.get("connection") == "keep-alive"
    assert response.status_code == 200


def test_post_users_schema_validation():
    schema = load_schema("post_users.json")
    response = requests.post(
        url="https://reqres.in/api/users",
        json={
            "name": "morpheus",
            "job": "leader"
        }
    )

    assert response.status_code == 201
    jsonschema.validate(response.json(), schema)


def test_update_user():
    response = requests.put(
        url="https://reqres.in/api/users/2",
        json={
            "name": "morpheus",
            "job": "zion resident"
        }
    )

    assert response.status_code == 200
    assert response.json()["job"] == "zion resident"


def test_delete():
    response = requests.delete(url="https://reqres.in/api/users/2")

    assert response.status_code == 204


def test_signup_success():
    response = requests.post(
        url="https://reqres.in/api/register",
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == 4
    assert response.json()["token"] == "QpwL5tke4Pnpja7X4"


def test_signup_failure():
    response = requests.post(
        url="https://reqres.in/api/register",
        json={
            "email": "sydney@fife"
        }
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


def test_login_success():
    response = requests.post(
        url="https://reqres.in/api/login",
        json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
    )

    assert response.status_code == 200
    assert response.json()["token"] == "QpwL5tke4Pnpja7X4"


def test_login_failure():
    response = requests.post(
        url="https://reqres.in/api/login",
        json={
            "email": "peter@klaven"
        }
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
