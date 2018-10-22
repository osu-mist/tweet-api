-- USERDATA table for holding the user information (username, user full name, and user id)
CREATE TABLE USERDATA(
    userid NUMBER NOT NULL,
    username VARCHAR2(255 char) NOT NULL,
    userfullname VARCHAR2(255 char),
    PRIMARY KEY (userid)
);
-- sequence counter for the unique user id, starts from 1 and increment by 1
CREATE SEQUENCE seq_userid
MINVALUE 1
START WITH 1
INCREMENT BY 1
CACHE 10;

--INSERT INTO USERDATA (userid)
--VALUES (seq_userid.nextval);

-- TWEETDATA table holds the tweet information, (message, tweet id, title, mode)
CREATE TABLE TWEETDATA(
    userid NUMBER,
    id NUMBER  NOT NULL,
    tweetmsg VARCHAR2(255 char),
    title VARCHAR2(255 char),
    mood VARCHAR2(255 char),
    FOREIGN KEY (userid) REFERENCES USERDATA(userid),
    PRIMARY KEY (id)
);
-- sequence counter for the unique user tweet id, starts from 1 and increment by 1
CREATE SEQUENCE seq_tweet
MINVALUE 1
START WITH 1
INCREMENT BY 1
CACHE 10;

--INSERT INTO TWEETDATA (id)
--VALUES (seq_userid.nextval);
