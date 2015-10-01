from flask import session
from flask_oauth import OAuth
import logging
import os
import requests

from you_should_read import db


REDIRECT_URI = '/authorized/google'


logger = logging.getLogger(__name__)


oauth = OAuth()
google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'
    },
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=os.environ['GOOGLE_CLIENT_ID'],
    consumer_secret=os.environ['GOOGLE_CLIENT_SECRET'])


@google.tokengetter
def get_access_token():
    return session.get('access_token')


def logged_in(conn):
    access_token = session.get('access_token')
    if not access_token:
        return False

    url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': 'OAuth %s' % access_token[0]}
    response = requests.get(url, headers=headers)

    if response.status_code >= 400:
        logger.error('Error using Google OAUTH. %s : %s', response.status_code,
                     response.text)
        return False


    resp = response.json()
    user_id = db.get_user_id_from_social(conn, resp['id'])

    if not user_id:
        user_id = db.add_user(conn, resp['id'], resp['name'], resp['email'],
                              resp['picture'])

    session['user_id'] = user_id

    return True
