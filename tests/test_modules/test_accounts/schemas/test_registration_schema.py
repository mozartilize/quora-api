import pytest
from marshmallow import ValidationError
import accounts.schemas  # noqa
from accounts.schemas import RegistrationSchema


@pytest.fixture
def schema():
    return RegistrationSchema()


def test_valid_data(mocker, app, schema):
    mocker.patch('accounts.schemas.unique', return_value=None)
    with app.app_context():
        data = schema.load({
            'email': 'test@example.com',
            'username': 'test',
            'password': 'test'
        })
    assert data['email'] == 'test@example.com'
    assert data['username'] == 'test'
    assert 'pw_hash' in data
    assert 'password' not in data


@pytest.mark.parametrize(
    'override_data',
    ({'email': ''}, {'username': ''}, {'password': ''}))
def test_invalid_blank_data(mocker, app, schema, override_data):
    mocker.patch('accounts.schemas.unique', return_value=None)
    raw_data = {
        'email': 'test@example.com',
        'username': 'test',
        'password': 'test'
    }
    raw_data.update(override_data)
    with app.app_context():
        with pytest.raises(ValidationError) as excinfo:
            schema.load(raw_data)
    assert len(excinfo.value.messages) == 1
    assert list(override_data.keys())[0] in excinfo.value.messages


@pytest.mark.parametrize('field', ('email', 'username'))
def test_invalid_unique_data(mocker, app, schema, field):
    def side_effect(table, _field, value):
        if _field == field:
            raise ValidationError(
                '{} already exists'.format(_field.capitalize()), _field)

    mocker.patch('accounts.schemas.unique', side_effect=side_effect)
    raw_data = {
        'email': 'test@example.com',
        'username': 'test',
        'password': 'test'
    }
    with app.app_context():
        with pytest.raises(ValidationError) as excinfo:
            schema.load(raw_data)
    assert len(excinfo.value.messages) == 1
    assert field in excinfo.value.messages
