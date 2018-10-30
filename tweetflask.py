from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask import request
import json

app = Flask(__name__)
api = Api(app)
data = json.load(open('db.json'))

@app.route('/tweets')
def get():
    app.logger.info('here?????')
    username = request.args.get('username')
    #return username
    for id in data['UserData']:
        if username == id['Username'] or username == id['UserID']:
            userID = id['UserID']
            for tweets in data['TweetData']:
                if userID == tweets['UserID']:
                    return jsonify(tweets)


#api.add_resource(GetTweetsByUser, '/tweets?username=<string:username>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
