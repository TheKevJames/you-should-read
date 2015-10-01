from flask import (Flask, flash, g, redirect, render_template, request,
                   session, url_for)
import sqlite3

from you_should_read import auth
from you_should_read import bayes
from you_should_read import convert
from you_should_read import db


DATABASE = 'database/database.db'
SECRET_KEY = 'chang3-m3'


app = Flask(__name__, static_url_path='')
app.secret_key = SECRET_KEY


def get_conn():
    conn = getattr(g, '_database', None)
    if not conn:
        conn = g._database = sqlite3.connect(DATABASE)
    return conn


@app.teardown_appcontext
def close_connection(_e):
    conn = getattr(g, '_database', None)
    if conn:
        conn.close()


@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return auth.google.authorize(callback=callback)


@app.route(auth.REDIRECT_URI)
@auth.google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@app.route('/')
def index():
    conn = get_conn()
    if not auth.logged_in(conn):
        return redirect(url_for('login'))

    try:
        include_read = request.args['include_read'] == 'true'
    except Exception:
        include_read = False

    top_rated = db.get_top_rated(conn, session['user_id'],
                                 include_read=include_read)
    for record in top_rated:
        record['length'] = convert.length_to_display(record['length'])
        record['rating'] = round(record['rating'], 2)

    recommended = db.get_recommended(conn, session['user_id'],
                                     include_read=include_read)
    for record in recommended:
        record['length'] = convert.length_to_display(record['length'])
        record['rating'] = round(record['rating'], 2)

    return render_template('index.html', top_rated=top_rated,
                           recommended=recommended)


@app.route('/media/<media_id>', methods=['GET'])
def media_by_id(media_id):
    conn = get_conn()
    status_value = db.get_status(conn, session['user_id'], media_id)

    record = db.get_media(conn, session['user_id'], media_id=media_id)
    if not record:
        flash('Could not find media with id "%s"' % media_id)
        return redirect(url_for('index'))

    record['length'] = convert.length_to_display(record['length'])
    record['rating'] = round(record['rating'], 2)
    record['status'] = convert.status_to_display(status_value)

    received = db.get_recommendations_received(conn, session['user_id'],
                                               media_id)
    sent = db.get_recommendations_sent(conn, session['user_id'], media_id)

    users = [u for u in db.get_users(conn)
             if u['id'] != session['user_id'] and \
                u['id'] not in (s['user_id'] for s in sent)]

    return render_template('media.html', media=record, received=received,
                           sent=sent, users=users)


@app.route('/search', methods=['GET'])
def search():
    conn = get_conn()
    record = db.get_media(conn, session['user_id'],
                          title=request.args['query'])

    if record:
        return redirect('/media/%s' % record['id'])
    else:
        flash('Could not find media with title "%s"' % request.args['query'])
        return redirect(url_for('index'))


@app.route('/add', methods=['POST'])
def add():
    conn = get_conn()
    media_id = db.add_media(conn, request.form['title'],
                            request.form['author'], request.form['link'],
                            request.form['description'],
                            request.form['length'], session['user_id'])
    if media_id == -1:
        flash('Could not insert duplicate media record. '
              'Try searching instead!')
        return redirect(url_for('index'))

    return redirect('/media/%s' % media_id)


@app.route('/media', methods=['GET'])
def media():
    conn = get_conn()
    code = db.update_media(conn, request.args['id'],
                           {request.args['field']: request.args['value']})

    return 'ok' if code == 200 else 'error'


@app.route('/rate', methods=['GET'])
def rate():
    conn = get_conn()
    code = db.update_rating(conn, session['user_id'], request.args['id'],
                            request.args['rating'])

    c = bayes.update(conn, request.args['id'])
    code = code if code > c else c

    return 'ok' if code == 200 else 'error'


@app.route('/recommend', methods=['GET'])
def recommend():
    conn = get_conn()
    code = db.update_recommendation(conn, session['user_id'],
                                    request.args['to_user'],
                                    request.args['id'], request.args['value'])

    return 'ok' if code == 200 else 'error'


@app.route('/status', methods=['GET'])
def status():
    conn = get_conn()
    code = db.update_status(conn, session['user_id'], request.args['id'],
                            request.args['value'])

    return 'ok' if code == 200 else 'error'
