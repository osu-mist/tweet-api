-- USERDATA table for holding the user information (USERNAME, user full name, and user ID)
CREATE TABLE USERDATA(
    USER_ID NUMBER NOT NULL,
    USERNAME VARCHAR2(255 char) NOT NULL,
    USERFULLNAME VARCHAR2(255 char),
    PRIMARY KEY (USER_ID)
);

COMMENT ON TABLE USERDATA IS 'Contains the data for the user, e.g (USER ID, USERNAME, USER FULL NAME)';
COMMENT ON COLUMN USERDATA.USER_ID IS 'ID OF users';
COMMENT ON COLUMN USERDATA.USERNAME IS 'Username name';
COMMENT ON COLUMN USERDATA.USERFULLNAME IS 'User full name';

-- sequence counter for the unique user ID, starts from 1 and increment by 1
CREATE SEQUENCE seq_USER_ID
MINVALUE 1
START WITH 1
INCREMENT BY 1
CACHE 10;

--INSERT INTO USERDATA (USER_ID)
--VALUES (seq_USER_ID.nextval);

-- TWEET_DATA table holds the tweet information, (message, tweet ID, TITLE, mode)
CREATE TABLE TWEET_DATA(
    USER_ID NUMBER NOT NULL,
    ID  VARCHAR2(255 char)  NOT NULL,
    TWEET_MSG VARCHAR2(255 char),
    TITLE VARCHAR2(255 char),
    MOOD VARCHAR2(255 char),
    TIME_AND_DATE VARCHAR2(255 char),
    FOREIGN KEY (USER_ID) REFERENCES USERDATA(USER_ID),
    PRIMARY KEY (ID)
);

COMMENT ON TABLE TWEET_DATA IS 'Contains inforamtion and content of the tweet';
COMMENT ON COLUMN TWEET_DATA.USER_ID IS 'ID of the owner of the tweet';
COMMENT ON COLUMN TWEET_DATA.ID IS 'ID of the tweet';
COMMENT ON COLUMN TWEET_DATA.TWEET_MSG IS 'Content of tweet message';
COMMENT ON COLUMN TWEET_DATA.TITLE IS 'Title of the tweet message';
COMMENT ON COLUMN TWEET_DATA.MOOD IS 'The mood of the user while typeing the tweet message';
COMMENT ON COLUMN TWEET_DATA.Time_AND_DATE IS 'The time and date of the tweet message';
