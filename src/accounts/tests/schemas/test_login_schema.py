import pytest
from unittest.mock import Mock
from marshmallow import ValidationError
import accounts.schemas
from accounts.schemas import LoginSchema
from helpers import RowProxyMock


@pytest.fixture
def schema():
    return LoginSchema()


def test_login_successfully(schema):
    result = Mock()
    result.fetchone.return_value = \
        RowProxyMock(id=1, activated_at=True, pw_hash='yay')
    accounts.schemas.repo = Mock(return_value=result)

    accounts.schemas.passlib_ext = Mock()
    accounts.schemas.passlib_ext.crypt_ctx.verify.return_value = True

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }
    data = schema.load(login_data)
    assert data['id'] == 1
    assert len(data) == 1


def test_login_wrong_password(schema):
    result = Mock()
    result.fetchone.return_value = \
        RowProxyMock(id=1, activated_at=True, pw_hash='yay')
    accounts.schemas.repo = Mock(return_value=result)

    accounts.schemas.passlib_ext = Mock()
    accounts.schemas.passlib_ext.crypt_ctx.verify.return_value = False

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }
    with pytest.raises(ValidationError) as excinfo:
        schema.load(login_data)
    assert 'password' in excinfo.value.messages


def test_login_passed_even_not_activate(schema):
    result = Mock()
    result.fetchone.return_value = \
        RowProxyMock(id=1, activated_at=False, pw_hash='yay')
    accounts.schemas.repo = Mock(return_value=result)

    accounts.schemas.passlib_ext = Mock()
    accounts.schemas.passlib_ext.crypt_ctx.verify.return_value = True

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }
    data = schema.load(login_data)
    assert data['id'] == 1
    assert len(data) == 1


def test_login_account_not_found(schema):
    result = Mock()
    result.fetchone.return_value = None
    accounts.schemas.repo = Mock(return_value=result)

    accounts.schemas.passlib_ext = Mock()
    accounts.schemas.passlib_ext.crypt_ctx.verify.return_value = True

    login_data = {
        'username_or_email': 'test',
        'password': 'test'
    }
    with pytest.raises(ValidationError) as excinfo:
        schema.load(login_data)
    assert 'username_or_email' in excinfo.value.messages
