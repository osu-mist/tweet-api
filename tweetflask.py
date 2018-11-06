from flask import Flask, jsonify, Response, request
from flask_restful import Api, Resource
import json
app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False


@app.route('/tweets')
def get():
    jsondata = json.load(open('db.json'))
    username = request.args.get('username')
    id = request.args.get('id')
    if username is None and id is None:
        return jsonify(errors('400', 'No username or ID provided')), 400

    for user in jsondata['UserData']:
        if username is not None:
            if username == user['Username']:
                return jsonify(get_tweet(jsondata, user))
        return jsonify(errors('400', 'The username is invalid')), 400
        if id is not None:
            if id == user['UserID']:
                return jsonify(get_tweet(jsondata, user))
        return jsonify(errors('400', 'The id is invalid')), 400


def get_tweet(jsondata, user):
    tweetdata = {
        "data": [
        ]
    }
    for tweets in jsondata['TweetData']:
        if user['UserID'] == tweets['UserID']:
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
    aboutlink = "https://developer.oregonstate.edu/documentation/error-reference"
    if status is '400':
        title = "Username is invalid"
    error = {
        "errors": [
        ]
    }
    response_error = {}
    response_error['status'] = status
    response_error['links'] = {
        "about": f'{aboutlink}#1{status}'
    }
    response_error['code'] = f'1{status}'
    response_error['title'] = title
    response_error['detail'] = detail
    error['errors'].append(response_error)
    return error


if __name__ == '__main__':
    app.run(debug=True, port=5000)
