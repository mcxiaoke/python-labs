# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import sys
import sqlite3

from flask import Flask, g
from flask import request
from flask import make_response
from flask import abort, redirect, url_for
from flask import render_template


app = Flask(__name__)
app.secret_key = 'q\x07t\\r\xe5\xd1\xa5n\xdd\x8dwq\xdc\xd3\xb59Wr\x91\x1eC\xf4F'

DATABASE = '/database/data.db'


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    try:
        username = request.cookies.get('username')
        print 'username from cookie', username
    except KeyError:
        print 'no cookie named username'

    resp = make_response(render_template("index.html", name=username))
    resp.set_cookie('username', 'mcxiaoke')
    return resp


@app.route('/none')
def none():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    abort(401)


@app.route('/hello/')
@app.route('/hello/<username>')
def hello(username=None):
    return 'hello,%s!' % username


if __name__ == '__main__':
    print sys.path
    app.run(host='0.0.0.0', port=5000, debug=True)


