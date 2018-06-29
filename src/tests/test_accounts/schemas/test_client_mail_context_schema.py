import pytest
from marshmallow import ValidationError
from accounts.schemas import ClientMailContextSchema


@pytest.fixture
def schema():
    return ClientMailContextSchema()


def test_valid_context(schema):
    data = schema.load({
        'subject': 'Welcome',
        'sender': 'mozart <mozart@gmail.com>',
        'url': 'https://example.com/accounts/activation'
    })
    assert len(data) == 3


@pytest.mark.parametrize(
    'override_data',
    ({'subject': 'Hello\nthere'}, {'sender': 'mozart'}, {'url': 'foo'})
)
def test_invalid_context(schema, override_data):
    raw_data = {
        'subject': 'Welcome',
        'sender': 'mozart <mozart@gmail.com>',
        'url': 'https://example.com/accounts/activation'
    }
    raw_data.update(override_data)
    with pytest.raises(ValidationError) as excinfo:
        schema.load(raw_data)
    assert len(excinfo.value.messages) == 1
    assert list(override_data.keys())[0] in excinfo.value.messages
