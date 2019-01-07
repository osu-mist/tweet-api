# Tweet API

## Purpose
The purpose of this project is to learn how to implement APIs, by creating a swagger file, implementing the database and learn about RESTful API by using Flask.

## Description
Tweets is a social media website that you can use to post information, news, and can also be used for personal use. In this application the user should be able to post a new tweet, view tweets, edit a tweet, and delete a tweet.

## Getting Started

### Prerequisites

1. install python3 from [Python](https://www.python.org/downloads/).
2. Generate a self signed certificate with [OpenSSL](https://www.openssl.org/):

```shell
$ openssl req -newkey rsa:2048 -new -nodes -keyout key.pem -out csr.pem
$ openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out server.crt
```
3. Create a config.yaml file, look at `config-example.yaml` for an example.

## Usage
Run the application:
```shell
$ python3 tweetfask.py
```
## GET/

### /tweets
Returns all the tweets by the username provided, or returns all the tweets by the username and the mood if provided.

## GET/{id}
### /tweets/{id}
Returns a tweet by the tweet ID provided.
Returns a 404 if a tweet ID doesn't exist 
