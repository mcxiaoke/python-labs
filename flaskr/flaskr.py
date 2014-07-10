# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import sqlite3
from datetime import datetime
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

import config

































# create app
app = Flask(__name__)
app.config.from_object(config)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(app.config['SCHEMA_FILE']) as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('SELECT id,title,abstract,text,created_at,user_id FROM entries ORDER BY id DESC')
    entries = [dict(id=row[0], title=row[1], abstract=row[2], text=row[3], created_at=row[4], user_id=row[5]) for row in
               cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/p/<int:id>')
def show_entry(id):
    cur = g.db.execute("SELECT id,title,abstract,text,created_at,user_id FROM entries WHERE id=?", (id,))
    row = cur.fetchone()
    entry = None
    if row:
        entry = dict(id=row[0], title=row[1], abstract=row[2], text=row[3], created_at=row[4], user_id=row[5])
    print "show_entry:", entry
    return render_template('show_entry.html', entry=entry)


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    logged_in = session.get('logged_in')
    logged_user = session.get('logged_user')
    print "add_entry, logged_in:", logged_in
    print "add_entry, logged_user:", logged_user
    if request.method == 'POST':
        if not logged_in or not logged_user:
            abort(401)
        user_id = session.get('logged_user')
        title = request.form['title']
        abstract = title
        text = request.form['text']
        created_at = datetime.strftime(datetime.now(), app.config['DATE_FORMAT'])
        g.db.execute("INSERT INTO entries (title,abstract,text,created_at,user_id) VALUES (?,?,?,?,?)",
                     [title, abstract, text, created_at, user_id])
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))
    if not logged_in or not logged_user:
        return redirect(url_for('login'))
    return render_template('add_entry.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'invalid password'
        else:
            session['logged_in'] = True
            session['logged_user'] = request.form['username']
            print request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('logged_user', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()


