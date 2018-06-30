import os
import tempfile
import pytest
from app import app

@pytest.fixture()
def client():
    #app.config['TESTING'] = True
    #client = app.test_client()
    #yield client

    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_no_valid_b64_left(client):
    rv = client.post('/v1/diff/1111111/left', data="1111111111")
    assert b'Invalid base64 string' in rv.data
    assert rv.status == "400 BAD REQUEST"

def test_no_valid_b64_right(client):
    rv = client.post('/v1/diff/1111111/right', data="1111111111")
    assert b'Invalid base64 string' in rv.data
    assert rv.status == "400 BAD REQUEST"

def test_no_valid_json_left(client):
    rv = client.post('/v1/diff/1111111/left', data="eW91IHNob3VsZCBoaXJlIG1lIHRobw==")
    assert b'This is not a valid Json object' in rv.data
    assert rv.status == "400 BAD REQUEST"

def test_no_valid_json_right(client):
    rv = client.post('/v1/diff/1111111/right', data="eW91IHNob3VsZCBoaXJlIG1lIHRobw==")
    assert b'This is not a valid Json object' in rv.data
    assert rv.status == "400 BAD REQUEST"

def test_create_left(client):
    rv = client.post('/v1/diff/1111111/left', data="eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSJ9")
    assert b'"left":"eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSJ9"' in rv.data
    assert rv.status == "200 OK"

def test_create_right(client):
    rv = client.post('/v1/diff/1111111/right', data="eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSJ9")
    assert b'"right":"eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSJ9"' in rv.data
    assert rv.status == "200 OK"

def test_get_id_not_exists(client):
    rv = client.get('/v1/diff/2222222')
    assert b'Resource does not exist' in rv.data
    assert rv.status == "404 NOT FOUND"

def test_get_id_partial_filled_left(client):
    client.post('/v1/diff/3333333/left', data="eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSJ9")
    rv = client.get('/v1/diff/3333333')
    assert b'You need provide left and right objects' in rv.data
    assert rv.status == "400 BAD REQUEST"

def test_get_id_partial_filled_right(client):
    client.post('/v1/diff/4444444/right', data="eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSJ9")
    rv = client.get('/v1/diff/4444444')
    assert b'You need provide left and right objects' in rv.data
    assert rv.status == "400 BAD REQUEST"

def test_get_equal_json(client):
    client.post('/v1/diff/5555555/right', data="eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSJ9")
    client.post('/v1/diff/5555555/left', data="eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSJ9")
    rv = client.get('/v1/diff/5555555')
    assert b'objects have no difference' in rv.data
    assert rv.status == "200 OK"

def test_get_json_diff_size(client):
    client.post('/v1/diff/6666666/right', data="eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSJ9")
    client.post('/v1/diff/6666666/left', data="eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSIsICJtc2cxIjoiaW5kZXJkYWFkIn0=")
    rv = client.get('/v1/diff/6666666')
    assert b'objects should have same size' in rv.data
    assert rv.status == "200 OK"

def test_get_json_diff(client):
    client.post('/v1/diff/7777777/right', data="eyJtc2ciOiJ5b3UgYmV0dGEgaGlyZSBtZSIsICJtc2cxIjoiaW5kZXJkYWFkIn0=")
    client.post('/v1/diff/7777777/left', data="eyJtc2cwIjoieW91IGJldHRhIGhpcmUgbWUiLCAibXNnMSI6IklOREVSREFBRCJ9")
    rv = client.get('/v1/diff/7777777')
    assert b'delete' in rv.data
    assert b'insert' in rv.data
    assert b'update' in rv.data
    assert rv.status == "200 OK"
