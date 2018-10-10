import random
import string
import db
import hashlib

def random_key():
    char_set = string.ascii_lowercase + string.digits 
    N = 20
    key = ''.join(random.SystemRandom().choice(char_set) for _ in range(N))
    return key


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class APIError(Exception):
    def __init__(self, message):
        self.message = message

def get_secret(service):
    c = db.get_db().cursor()
    c.execute("SELECT secret_key FROM service WHERE id=?", (service,))
    return c.fetchone()[0]

def verify(data, key):
    assert all(x in data for x in ["date", "result", "detail", "token"])
    s = data["date"] + str(data["result"]) + data["detail"] + key
    s = s.encode("utf-8")
    return hashlib.sha1(s).hexdigest() == data["token"]

def encrypt(data, key):
    assert all(x in data for x in ["date", "result", "detail"])
    s = data["date"] + str(data["result"]) + data["detail"] + key
    s = s.encode("utf-8")
    data["token"] = hashlib.sha1(s).hexdigest()

