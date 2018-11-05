from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask import request
import json

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False




@app.route('/tweets')
def get():
    jsondata = json.load(open('db.json'))
    username = request.args.get('username')
    id = request.args.get('id')

    try:
        for user in jsondata['UserData']:
            if username != None:
                if username == user['Username']:
                    return jsonify(get_tweet(jsondata, user))
            if id != None:
                if id == user['UserID']:
                    return jsonify(get_tweet(jsondata, user))
    except TypeError:
        return "Invalid input!"

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
            #app.logger.info((tweetdata))
    return tweetdata

#api.add_resource(GetTweetsByUser, '/tweets?username=<string:username>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
