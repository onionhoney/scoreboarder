from flask import current_app, g
import sqlite3

SAMPLE_ID = 10928
SECRET_KEY = 'happytreefriends0148'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(mock=False):
    db = get_db()
    create_db(db)
    if mock:
        populate_db(db)

def create_db(conn):
    c = conn.cursor()

    c.execute(""" CREATE TABLE IF NOT EXISTS service
    (id INT, 
    name TEXT, 
    description TEXT, 
    app_name TEXT, 
    owner_email TEXT, 
    creation_date DATE, 
    secret_key TEXT,
    unique (id)
    ) """)

    c.execute(""" CREATE TABLE IF NOT EXISTS category
    (serviceid INT, 
    name TEXT, 
    description TEXT,
    ascending BOOLEAN, 
    FOREIGN KEY(serviceid) REFERENCES service(id), 
    unique (serviceid, name)
    )""")

    c.execute(""" CREATE TABLE IF NOT EXISTS account
    (serviceid INT, 
    username TEXT, 
    email TEXT,
    wcaid TEXT, 
    description TEXT, 
    FOREIGN KEY(serviceid) REFERENCES service(id), 
    unique (serviceid, username)
    ) """)

    c.execute(""" CREATE TABLE IF NOT EXISTS score
    (
    serviceid INT,
    categoryname TEXT, 
    username TEXT, 
    date TEXT, 
    result INT, 
    detail TEXT,
    FOREIGN KEY(serviceid) REFERENCES service(id),
    FOREIGN KEY(categoryname) REFERENCES category(name),
    FOREIGN KEY(username) REFERENCES account(username), 
    unique (serviceid, categoryname, username, date, result)
    ) """)
    conn.commit()


def populate_db(conn):
    c = conn.cursor()
    service1 = (SAMPLE_ID, 'service0', 'test sc', '15puzzle.com', 'zhouhengsun@gmail.com', '2018-10-09T21:32:05Z', SECRET_KEY)
    c.execute("INSERT INTO service VALUES (?,?,?,?,?,?,?)", service1)

    cat1 = (SAMPLE_ID, 'single15', '', True)
    c.execute("INSERT INTO category VALUES (?,?,?,?)", cat1)

    person1 = (SAMPLE_ID, 'onionhoney', 'onionhoney@github.io', 
    '2008SUNZ01', 'fake')
    person2 = (SAMPLE_ID, 'tianxing', 'tianxing@outlook.com', 
    'xxx', 'good')
    c.execute("INSERT INTO account VALUES (?,?,?,?,?)", person1)
    c.execute("INSERT INTO account VALUES (?,?,?,?,?)", person2)

    scores = [(SAMPLE_ID, 'single15', 'onionhoney', '2018-10-09T21:32:05Z', '4800', '{}'),
    (SAMPLE_ID, 'single15', 'onionhoney', '2018-10-09T21:33:05Z', '7900', '{}'),
    (SAMPLE_ID, 'single15', 'onionhoney', '2018-10-09T21:34:05Z', '10100', '{}'),
    (SAMPLE_ID, 'single15', 'tianxing', '2018-10-08T08-08:08Z', '4600', '{}'),
    (SAMPLE_ID, 'single15', 'tianxing', '2018-09-08T08-08:08Z', '4700', '{}'),
    (SAMPLE_ID, 'single15', 'tianxing', '2018-08-08T08-08:08Z', '4800', '{}'),
    (SAMPLE_ID, 'single15', 'tianxing', '2018-07-08T08-08:08Z', '5700', '{}')]

    c.executemany("INSERT INTO score VALUES (?,?,?,?,?,?)", scores)

    bad_score = (SAMPLE_ID, 'single15', 'xx', '2018-10-09T21:34:05Z', '1', '{}')
    c.execute("INSERT INTO score VALUES (?,?,?,?,?,?)", bad_score)
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect("score.db")
    create_db(conn)
    populate_db(conn)