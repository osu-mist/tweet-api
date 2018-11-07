from flask import Flask, jsonify, request
import json
import ssl
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/tweets')
def get():
    with open('db.json', 'r') as jfile:
        jsondata = json.load(jfile)
    username = request.args.get('username')
    mood = request.args.get('mood')
    if username is None:
        return jsonify(errors('400', 'No username provided')), 400

    for user in jsondata['UserData']:
        if username == user['Username']:
            return jsonify(get_tweet(jsondata, user, mood))
    return jsonify(get_tweet(jsondata, None, None))


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
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/Users/Mohammed/Desktop/CA/server.crt', '/Users/Mohammed/Desktop/CA/key.pem')
    app.run(debug=True, port=5000, ssl_context=context)
