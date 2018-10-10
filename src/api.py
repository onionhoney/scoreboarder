from flask import Flask
from flask import jsonify
from flask import abort, request
from flask import current_app, g
from flask.cli import with_appcontext

import hashlib
import sqlite3

from db import get_db, create_db, populate_db
from util import get_secret, verify, dict_factory, APIError

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["DATABASE"] = "score.db"


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/v0')
def hello_api():
    return 'Hello API user!'


@app.route('/api/v0/s/<int:service>/c/<category>/result', methods=['GET'])
@app.route('/api/v0/s/<int:service>/c/<category>/result/<int:top>', methods=['GET'])
def api_all(service, category, top=5):
    conn = get_db()
    conn.row_factory = dict_factory
    c = conn.cursor()
    top = min(top, 1000)
    c.execute("""SELECT result, username, date FROM score WHERE serviceid is ? AND categoryname is ? 
                 ORDER BY result ASC, date ASC LIMIT ? """, (service, category, top))
    return jsonify(c.fetchall())


@app.route('/api/v0/s/<int:service>/c/<category>/user/<username>', methods=['POST'])
def post_result(service, category, username):
    with get_db() as conn:
        c = conn.cursor()
        # Check for service and category
        c.execute("SELECT 1 FROM service WHERE id = ?", (service,))
        if not c.fetchone():
            raise APIError("Service not found")

        # get the JSON
        try:
            key = get_secret(service)
            data = request.get_json(force=True)
            if not verify(data, key):
                raise Exception
        except:
            raise APIError("Bad JSON")

        score = (service, category, username, data["date"], data["result"], data["detail"])
        c.execute("""INSERT INTO score VALUES (?,?,?,?,?,?)""", score)

        return 'Successful'

    
@app.errorhandler(APIError)
def page_not_found(error):
    return 'Bad request: {}'.format(error), 404
