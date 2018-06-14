import pytest
import json

data = {'username': 'test',
        'password': 'test',
        'email': 'test@example.com'}


@pytest.mark.parametrize(('content_type', 'data'),
    ((None, data), ('application/json', json.dumps(data))))
def test_regist_account(client, content_type, data):
    res = client.post('/api/v1/accounts',
        data=data,
        content_type=content_type)
    assert res.status_code == 201
    assert 'id' in res.json
    assert 'Location' in res.headers
