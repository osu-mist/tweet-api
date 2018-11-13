from flask import Flask, jsonify, request
from flask_basicauth import BasicAuth
import json
import yaml
import ssl
app = Flask(__name__)
basic_auth = BasicAuth(app)
app.config['JSON_SORT_KEYS'] = False
app.config['BASIC_AUTH_FORCE'] = True


@app.route('/tweets')
def get():
    # Opening and reading the db file
    with open('db.json', 'r') as jfile:
        jsondata = json.load(jfile)
    # Parsing the username and mood from url
    username = request.args.get('username')
    mood = request.args.get('mood')
    # return 400 for not providing a username
    if username is None:
        return jsonify(errors('400', 'No username provided')), 400
    # looking up the username in the DB
    for user in jsondata['UserData']:
        if username == user['Username']:
            return jsonify(get_tweet(jsondata, user, mood))
    # if the username does not exist in DB this line will be excuted
    # to return an empty array
    return jsonify(get_tweet(jsondata, None, None))

# lookes up all the tweets that belong to the username provided
# and looks for the mood if provided
def get_tweet(jsondata, user, mood):
    tweetdata = {
        "data": [
        ]
    }
    if user is None:
        return tweetdata
    for tweets in jsondata['TweetData']:
        if user['UserID'] == tweets['UserID']:
            if mood is None or mood is not None and mood == tweets['Mood']:
                response_data = {}
                response_data['id'] = user['UserID']
                response_data['type'] = "string"
                response_data['attributes'] = {
                    "username": user['Username'],
                    "userFullName": user['UserFullName'],
                    "timeAndDate": tweets['TimeAndDate'],
                    "title": tweets['Title'],
                    "mood": tweets['Mood'],
                    "tweet": tweets['TweetMsg']
                }
                tweetdata["data"].append(response_data)
    return tweetdata


def errors(status, detail):
    aboutur = "https://developer.oregonstate.edu/documentation/error-reference"
    if status is '400':
        title = "Username is invalid"
    error = {
        "errors": [
        ]
    }
    response_error = {}
    response_error['status'] = status
    response_error['links'] = {
        "about": f'{aboutur}#1{status}'
    }
    response_error['code'] = f'1{status}'
    response_error['title'] = title
    response_error['detail'] = detail
    error['errors'].append(response_error)
    return error


if __name__ == '__main__':
    with open('config.yaml', 'r') as yfile:
        yamldata = yaml.load(yfile)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(
        yamldata['server']['certPath'],
        yamldata['server']['keyPath']
        )
    app.config['BASIC_AUTH_USERNAME'] = yamldata['authentication']['username']
    app.config['BASIC_AUTH_PASSWORD'] = yamldata['authentication']['password']
    app.run(debug=True, port=yamldata['server']['port'], ssl_context=context)
