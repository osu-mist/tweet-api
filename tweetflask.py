from flask import Flask, jsonify, request
from flask_basicauth import BasicAuth
from datetime import datetime

import json
import yaml
import ssl


app = Flask(__name__)


def read_file():
    # Opening and reading the db file
    with open('db.json', 'r') as jfile:
        jsondata = json.load(jfile)
    return jsondata


@app.route('/tweets', strict_slashes=False)
def get():
    jsondata = read_file()
    # Parsing the username and mood from url
    username = request.args.get('username')
    mood = request.args.get('mood')
    # return 400 for not providing a username
    if not username:
        return jsonify(errors('400', 'No username provided')), 400
    # looking up the username in the DB
    for user in jsondata['UserData']:
        if username.upper().lower() == user['Username'].upper().lower():
            return jsonify(get_tweet(jsondata, user, mood))
    # if the username does not exist in DB this line will be executed
    # to return an empty array
    return jsonify(get_tweet(jsondata, None, None))


@app.route('/tweets/<tweet_id>')
def get_ID(tweet_id):
    try:
        return jsonify(tweets[tweet_id])
    except KeyError:
        return jsonify(errors('404', 'tweet does not exist')), 404


# looks up all the tweets that belong to the username provided
# and looks for the mood if provided
def get_tweet(jsondata, user, mood):
    tweet_data = {
        'data': [
        ]
    }
    if user is None:
        return tweet_data
    for tweets in jsondata['TweetData']:
        if user['UserID'] == tweets['UserID']:
                if not mood or mood.lower() == tweets['Mood'].lower():
                    tweet_data['data'].append(get_attributes(user, tweets))
    return tweet_data


def get_attributes(user, tweet_data):
    time = datetime.strptime(tweet_data['TimeAndDate'],
                             '%d-%b-%y %I.%M.%S.%f %p %z')
    response_data = {}
    response_data['id'] = tweet_data['TweetID']
    response_data['type'] = 'tweet'
    response_data['attributes'] = {
        'username': user['Username'],
        'userFullName': user['UserFullName'],
        'timeAndDate': time.isoformat(),
        'title': tweet_data['Title'],
        'mood': tweet_data['Mood'],
        'tweet': tweet_data['TweetMsg']
    }
    return response_data


def errors(status, detail):
    error_base_url = 'https://developer.oregonstate.edu/documentation'
    reference_error = '/error-reference'
    code = f'1{status}'
    error_dictionary = {
        '400': 'Bad Request',
        '401': 'Authentication failed',
        '404': 'Page not found',
        '500': 'Unexpected Internal error'
    }
    title = error_dictionary[status]
    error = {
        'errors': [
        ]
    }
    response_error = {}
    response_error['status'] = status
    response_error['links'] = {
        'about': f'{error_base_url}{reference_error}{code}'
    }
    response_error['code'] = code
    response_error['title'] = title
    response_error['detail'] = detail
    error['errors'].append(response_error)
    return error


def tweets_dectionary():
    jsondata = read_file()
    tweets = {}
    for tweet in jsondata["TweetData"]:
        for user in jsondata['UserData']:
            if tweet['UserID'] == user['UserID']:
                tweets[tweet['TweetID']] = get_attributes(user, tweet)
    return tweets


class ChallengeAuth(BasicAuth):
    def challenge(self):
        return jsonify(errors('401', 'Wrong username or password')), 401


if __name__ == '__main__':

    app.config['JSON_SORT_KEYS'] = False
    app.config['BASIC_AUTH_FORCE'] = True

    basic_auth = ChallengeAuth(app)
    with open('config.yaml', 'r') as yfile:
        yaml_data = yaml.load(yfile)

    server = yaml_data['server']
    authentication = yaml_data['authentication']
    secureProtocol = server['secureProtocol']
    try:
        context = ssl.SSLContext(getattr(ssl, secureProtocol))
    except AttributeError:
        exit('Invalid secureProtocol')

    context.load_cert_chain(
        server['certPath'],
        server['keyPath']
        )
    app.config['BASIC_AUTH_USERNAME'] = authentication['username']
    app.config['BASIC_AUTH_PASSWORD'] = authentication['password']

    tweets = tweets_dectionary()

    app.run(debug=True, port=server['port'], ssl_context=context)
