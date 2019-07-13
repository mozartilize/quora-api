import pytest
import json
from faker import Faker

faker = Faker()

account = lambda: {
    "username": faker.user_name(),
    "password": "test",
    "email": faker.email(),
}

client_mail_info = {
    "subject": "Welcome to Quora",
    "sender": "no-reply <noreply@quora.com>",
    "url": "https://www.quora.com/accounts/activation",
}
valid_data = lambda: dict(account(), **client_mail_info)

invalid_data_email = dict(valid_data(), **{"email": "test"})
invalid_data_username = dict(valid_data(), **{"username": ""})
invalid_data_password = dict(valid_data(), **{"password": ""})


@pytest.mark.parametrize(
    ("content_type", "data"),
    ((None, valid_data()), ("application/json", json.dumps(valid_data()))),
)
def test_regist_account_with_valid_data(client, content_type, data):
    res = client.post("/api/v1/accounts", data=data, content_type=content_type)
    assert res.status_code == 201
    assert "id" in res.json
    assert "Location" in res.headers


@pytest.mark.parametrize(
    ("content_type", "data", "err_key"),
    (
        ("application/json", json.dumps(invalid_data_email), "email"),
        ("application/json", json.dumps(invalid_data_username), "username"),
        ("application/json", json.dumps(invalid_data_password), "password"),
    ),
)
def test_regist_account_with_invalid_data(client, content_type, data, err_key):
    res = client.post("/api/v1/accounts", data=data, content_type=content_type)
    assert res.status_code == 400
    assert "errors" in res.json
    assert len(res.json["errors"].keys()) == 1
    assert err_key in res.json["errors"]
