import pytest
from marshmallow import ValidationError
from accounts.schemas import LoginSchema
from ..helpers import RowProxyMock


@pytest.fixture
def schema():
    return LoginSchema()


def test_login_successfully(mocker, app, schema):
    result = mocker.Mock()
    result.fetchone.return_value = \
        RowProxyMock(id=1, activated_at=True, pw_hash='yay')
    mocker.patch('accounts.schemas.repo', return_value=result)

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }
    with app.app_context():
        mocker.patch('accounts.schemas.passlib_ext.crypt_ctx.verify',
                     return_value=True)
        data = schema.load(login_data)
    assert data['id'] == 1
    assert len(data) == 1


def test_login_wrong_password(mocker, app, schema):
    result = mocker.Mock()
    result.fetchone.return_value = \
        RowProxyMock(id=1, activated_at=True, pw_hash='yay')
    mocker.patch('accounts.schemas.repo', return_value=result)

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }

    with app.app_context():
        mocker.patch('accounts.schemas.passlib_ext.crypt_ctx.verify',
                     return_value=False)
        with pytest.raises(ValidationError) as excinfo:
            schema.load(login_data)
        assert 'password' in excinfo.value.messages


def test_login_passed_even_not_activate(mocker, app, schema):
    result = mocker.Mock()
    result.fetchone.return_value = \
        RowProxyMock(id=1, activated_at=None, pw_hash='yay')
    mocker.patch('accounts.schemas.repo', return_value=result)

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }

    with app.app_context():
        mocker.patch('accounts.schemas.passlib_ext.crypt_ctx.verify',
                     return_value=True)
        data = schema.load(login_data)
    assert data['id'] == 1
    assert len(data) == 1


def test_login_account_not_found(mocker, app, schema):
    result = mocker.Mock()
    result.fetchone.return_value = None
    mocker.patch('accounts.schemas.repo', return_value=result)

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }

    with app.app_context():
        mocker.patch('accounts.schemas.passlib_ext.crypt_ctx.verify',
                     return_value=True)
        with pytest.raises(ValidationError) as excinfo:
            schema.load(login_data)
        assert 'username_or_email' in excinfo.value.messages
