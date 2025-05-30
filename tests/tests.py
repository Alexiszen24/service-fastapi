import faker
import pytest

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
fake = faker.Faker()

client.fake_user_email = fake.email()
client.fake_user_password = fake.password()
client.fake_user_name = fake.first_name()
client.new_user_id = 0
client.auth_token = ""


def test_signup():
    response = client.post("/auth/signup",
                           json={"email": client.fake_user_email,
                                 "password": client.fake_user_password,
                                 "name": client.fake_user_name}
    )
    assert response.status_code == 201
    client.new_user_id = response.json()


def test_login():
    response = client.post("/auth/login",
                           data={"username": client.fake_user_email,
                                 "password": client.fake_user_password}
    )
    assert response.status_code == 200
    client.auth_token = response.json()['access_token']


def test_me():
    response = client.get("/utils/me", headers={"Authorization": f"Bearer {client.auth_token}"})
    assert response.status_code == 200
    assert response.json() == client.new_user_id


def test_line_create():
    line_name = "L-056"
    client = TestClient(app)
    response = client.post("/v1/lines/",
                           json={"name": line_name}
    )
    assert response.status_code == 201
    assert response.json()['name'] == line_name


def test_lines_list():
    client = TestClient(app)
    response = client.get("/v1/lines/")
    assert response.status_code == 200
    assert response.json()['offset'] == 0


def test_events_list():
    client = TestClient(app)
    response = client.get("/v1/events/1")
    assert response.status_code == 200
    assert response.json()['offset'] == 0
