import os
import tempfile
import json
import pytest
from flask import jsonify, g

import api
from db import SAMPLE_ID, populate_db, create_db, init_db
from util import encrypt, get_secret

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    with api.app.app_context():
        init_db(mock=True)

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])


def test_empty_db(client):
    rv = client.get('/')
    assert b'Hello' in rv.data

def post_user(client, s, c, u, key=None):
    data = {'date':'now', 'result':2700, 'detail':'it"s fake'}
    if key is None:
        with api.app.app_context():
            key = get_secret(s)
    encrypt(data, key)
    data = json.dumps(data)
    return client.post('/api/v0/s/{}/c/{}/user/{}'.format(s, c, u), 
        data=data)

def test_post_user(client):
    rv = post_user(client, SAMPLE_ID, 'single15', 'admin')
    assert b'Successful' in rv.data
    with api.app.app_context():
        conn = api.get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM score where username = "admin"')
        assert len(c.fetchall()) == 1


def test_post_user_cheat(client):
    rv = post_user(client, SAMPLE_ID, 'single15', 'admin', key="randomwrong")
    assert b'Bad JSON' in rv.data


def test_secret_key_created(client):
    with api.app.app_context():
        assert len(api.get_secret(SAMPLE_ID)) == 20