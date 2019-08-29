import pytest
from marshmallow import ValidationError
from auth.schemas import LoginSchema
from ..helpers import RowProxyMock


@pytest.fixture
def schema():
    return LoginSchema()

error = {'_schema': 'Authentication failed'}


def test_login_successfully(mocker, app, schema):
    result = mocker.Mock()
    result.fetchone.return_value = \
        RowProxyMock(id=1, activated_at=True, pw_hash='yay')
    mocker.patch('auth.services.repo', return_value=result)

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }
    with app.app_context():
        mocker.patch('auth.services.passlib_ext.crypt_ctx.verify',
                     return_value=True)
        data = schema.load(login_data)
    assert data['id'] == 1
    assert len(data) == 1


@pytest.mark.parametrize('error', [error])
def test_login_wrong_password(mocker, app, schema, error):
    result = mocker.Mock()
    result.fetchone.return_value = \
        RowProxyMock(id=1, activated_at=True, pw_hash='yay')
    mocker.patch('auth.services.repo', return_value=result)

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }

    with app.app_context():
        mocker.patch('auth.services.passlib_ext.crypt_ctx.verify',
                     return_value=False)
        with pytest.raises(ValidationError) as excinfo:
            schema.load(login_data)
        assert excinfo.value.messages == error


def test_login_passed_even_not_activate(mocker, app, schema):
    result = mocker.Mock()
    result.fetchone.return_value = \
        RowProxyMock(id=1, activated_at=None, pw_hash='yay')
    mocker.patch('auth.services.repo', return_value=result)

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }

    with app.app_context():
        mocker.patch('auth.services.passlib_ext.crypt_ctx.verify',
                     return_value=True)
        data = schema.load(login_data)
    assert data['id'] == 1
    assert len(data) == 1


@pytest.mark.parametrize('error', [error])
def test_login_account_not_found(mocker, app, schema, error):
    result = mocker.Mock()
    result.fetchone.return_value = None
    mocker.patch('auth.services.repo', return_value=result)

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }

    with app.app_context():
        mocker.patch('auth.services.passlib_ext.crypt_ctx.verify',
                     return_value=True)
        with pytest.raises(ValidationError) as excinfo:
            schema.load(login_data)
        assert excinfo.value.messages == error
