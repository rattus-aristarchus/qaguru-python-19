import jsonschema
import requests

from utils import load_schema


def test_get_users_status_code_is_ok():
    response = requests.get(url="https://reqres.in/api/users")
    print(response.text)
    assert response.status_code == 200


def test_get_users_per_page():
    response = requests.get(url="https://reqres.in/api/users", params={"per_page": 1})

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["per_page"] == 1


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
