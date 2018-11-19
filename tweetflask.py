from flask import Flask, jsonify, request
from flask_basicauth import BasicAuth
from datetime import datetime

import json
import yaml
import ssl


app = Flask(__name__)


@app.route('/tweets')
def get():
    # Opening and reading the db file
    with open('db.json', 'r') as jfile:
        jsondata = json.load(jfile)
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
    # if the username does not exist in DB this line will be excuted
    # to return an empty array
    return jsonify(get_tweet(jsondata, None, None))


# looks up all the tweets that belong to the username provided
# and looks for the mood if provided
def get_tweet(jsondata, user, mood):
    tweetdata = {
        'data': [
        ]
    }
    if user is None:
        return tweetdata
    for tweets in jsondata['TweetData']:
        if user['UserID'] == tweets['UserID']:
            if not mood or mood.lower() == tweets['Mood'].lower():
                response_data = {}
                response_data['id'] = tweets['TweetID']
                response_data['type'] = "tweet"
                time = datetime.strptime(tweets['TimeAndDate'],
                                         '%d-%b-%y %I.%M.%S.%f %p %z')
                response_data['attributes'] = {
                    'username': user['Username'],
                    'userFullName': user['UserFullName'],
                    'timeAndDate': time.isoformat(),
                    'title': tweets['Title'],
                    'mood': tweets['Mood'],
                    'tweet': tweets['TweetMsg']
                }
                tweetdata["data"].append(response_data)
    return tweetdata


def errors(status, detail):
    error_base_url = "https://developer.oregonstate.edu/documentation"
    reference_error = "/error-reference"
    code = f'1{status}'
    errordictionary = {
        '400': 'Bad Request',
        '401': 'Authentication faild',
        '404': 'Page not found',
        '500': 'Unexpected Internal error'
    }
    title = errordictionary[status]
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


class ChallengeAuth(BasicAuth):
    def challenge(self):
        return jsonify(errors('401', 'Wrong username or password')), 401


if __name__ == '__main__':
    app.config['JSON_SORT_KEYS'] = False
    app.config['BASIC_AUTH_FORCE'] = True

    basic_auth = ChallengeAuth(app)
    with open('config.yaml', 'r') as yfile:
        yamldata = yaml.load(yfile)
    secureProtocol = yamldata['server']['secureProtocol']
    try:
        context = ssl.SSLContext(getattr(ssl, secureProtocol))
    except AttributeError as e:
        exit('Invalid secureProtocol')

    context.load_cert_chain(
        yamldata['server']['certPath'],
        yamldata['server']['keyPath']
        )
    app.config['BASIC_AUTH_USERNAME'] = yamldata['authentication']['username']
    app.config['BASIC_AUTH_PASSWORD'] = yamldata['authentication']['password']

    app.run(debug=True, port=yamldata['server']['port'], ssl_context=context)
