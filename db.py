from sys import stderr
import mysql.connector
from mysql.connector import errorcode
import os
import sys


def connect():

    database = mysql.connector.connect(user='k7aqgz64ljyxr9w9',
                                       password='j5zmy2v2ujgcjptt',
                                       host='durvbryvdw2sjcm5.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
                                       database='mh4057an9aee5vxa'
                                       )

    return database


def rawConnect():

    database = mysql.connector.connect(user='k7aqgz64ljyxr9w9',
                                       password='j5zmy2v2ujgcjptt',
                                       host='durvbryvdw2sjcm5.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
                                       database='mh4057an9aee5vxa',
                                       raw=True
                                       )

    return database


def testConn():
    try:
        conn = connect()
        print("Connected")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username/password issue')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('databse not found')
    else:
        conn.close()


def newUser(email, password, fname, lname, username):

    inputValues = "INSERT INTO users(email, password, fname, lname, username, about, interests) VALUES(%s,%s,%s,%s,%s,'None','None');"

    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(
            inputValues, (email, password, fname, lname, username))
        conn.commit()
        rs = statement.fetchone()

        statement.close()
        conn.close()

        return True

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username/password issue')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('databse not found')
    else:
        return False


def loginUser(username, password):
    inputCommand = "SELECT * FROM users WHERE email = %s AND password = %s"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputCommand, (username, password))

        rs = statement.fetchone()

        if rs is not None:
            print("Successful Login")
            statement.close()
            conn.close()

            return True
        else:
            print("Username/Password not found")

            statement.close()
            conn.close()

            return False

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return False


def getUser(username):
    inputCommand = "SELECT id FROM users WHERE email = %s "
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputCommand, (username,))

        rs = statement.fetchone()

        if rs is not None:
            print("Successful Login")
            statement.close()
            conn.close()

            return True
        else:
            print("Username/Password not found")

            statement.close()
            conn.close()

            return False

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return False


def userInfo(username):
    inputCommand = "SELECT user_id, email, fname, lname, username, about, interests FROM users WHERE email = (%s)"
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (username,))

        rs = statement.fetchone()
        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()

        return False


def userInfoInquiry(username):
    inputCommand = "SELECT user_id, email, fname, lname, username, about, interests FROM users WHERE fname LIKE (%s) OR username LIKE (%s)"
    combined = "%" + username + "%"
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (combined, combined,))

        rs = statement.fetchall()
        print("rs-------------------", flush=True)
        print(rs, flush=True)
        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        print("rs-------------------", flush=True)

        return False


def firstNameUser(user_id):
    inputCommand = "SELECT username FROM users WHERE email = (%s)"
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (user_id,))

        rs = statement.fetchone()
        statement.close()
        conn.close()
        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return False


def createActivity(title, description, image, likes):  # updated for likes
    inputValues = "INSERT INTO activities (title, description, image, likes) VALUES(%s,%s,%s,%s);"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputValues, (title, description,
                                        image, likes))  # updated for likes
        conn.commit()
        rs = statement.lastrowid

        statement.close()
        conn.close()

        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username/password issue')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('databse not found')
    else:
        return False


def getAllActivities():
    inputCommand = "SELECT title, description, image, likes, activity_id FROM activities"
    try:
        conn = connect()
        statement = conn.cursor()
        x = ()
        statement.execute(inputCommand, x)

        rs = statement.fetchall()

        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return False


def getActivity(activity_id):
    inputCommand = "SELECT title, description, image, likes, activity_id, happy, neutral, sad, totalcomments FROM activities WHERE activity_id = (%s)"
    try:
        conn = rawConnect()
        statement = conn.cursor()
        statement.execute(inputCommand, (activity_id,))

        rs = statement.fetchone()

        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return False


def joinActivityDB(user_id, activity_id):
    inputCommand = "INSERT INTO activitymembers (user_id, activity_id) VALUES(%s,%s)"
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (user_id, activity_id))
        conn.commit()
        rs = statement.fetchone()

        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return False


def getActivityUsers(activity_id):
    inputCommand = "SELECT user_id FROM activitymembers WHERE activity_id = (%s)"
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (activity_id,))
        rs = statement.fetchall()
        print("ASDASDASDASDASD", flush=True)
        print(rs, flush=True)
        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return False


def getActivityIDs(user_id):
    inputCommand = "SELECT activity_id FROM activitymembers WHERE user_id = (%s)"
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (user_id,))

        rs = statement.fetchall()

        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return False

# have return email of validated user


def editInfo(username, about, interests, location, gender):
    inputCommand = "UPDATE users SET about = %s, interests = %s, location = %s, gender = %s WHERE email = (%s)"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputCommand, (about, interests,
                                         location, gender, username,))
        conn.commit()
        rs = statement
        print(rs, file=sys.stderr)
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        elif err:
            print(err, file=sys.stderr)
        else:
            conn.close()
        return False


def settings(username, password, email):
    inputCommand = "UPDATE users SET username = %s, password = %s WHERE email = (%s)"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputCommand, (username, password, email,))
        conn.commit()
        rs = statement
        print(rs, file=sys.stderr)
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        elif err:
            print(err, file=sys.stderr)
        else:
            conn.close()
        return False


def writecomment(user_id, activity_id, body):
    inputCommand = "INSERT INTO comments (user_id, activity_id, body) VALUES(%s,%s,%s)"
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (user_id, activity_id, body))
        conn.commit()
        rs = statement.fetchone()

        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return False


def getcomments(activity_id):
    inputCommand = "SELECT activity_id, user_id, body FROM comments WHERE activity_id = (%s)"
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (activity_id,))

        rs = statement.fetchall()

        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return False


def getInfo(username):
    inputComand = "SELECT about, interests, location, gender, email FROM users WHERE email = (%s)"
    print(username, file=sys.stderr)
    try:
        conn = connect()

        statement = conn.cursor(prepared=True)
        statement.execute(inputComand, (username,), multi=True)

        return statement.fetchall()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error", file=sys.stderr)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found", file=sys.stderr)
        elif err:
            print(err, file=sys.stderr)
        else:
            conn.close()

        return ['No database access', 'No database access']


def changeProfPic(user, picture):

    inputValues = "DELETE FROM profilepictures WHERE user_id = (%s);"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        # Needs to be updated for likes
        statement.execute(inputValues, (user,))
        conn.commit()
        statement.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username/password issue')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('databse not found')
        else:
            print(err, file=sys.stderr)

    inputValues = "INSERT INTO profilepictures (user_id, picture) VALUES(%s,%s);"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        # Needs to be updated for likes
        statement.execute(inputValues, (user, picture))
        conn.commit()
        statement.close()
        conn.close()

        return True

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username/password issue')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('databse not found')
        else:
            print(err, file=sys.stderr)
    else:
        return False


def getPic(username):

    inputComand = "SELECT picture FROM profilepictures WHERE user_id = (%s)"
    try:
        conn = rawConnect()
        statement = conn.cursor()
        statement.execute(inputComand, (username,))
        rs = statement.fetchone()
        return rs

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error", file=sys.stderr)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found", file=sys.stderr)
        elif err:
            print(err, file=sys.stderr)
        else:
            conn.close()
        return ['No database access', 'No database access']


def updateSentiments(activity_id, happy, neutral, sad, totalComments):

    print("Sentiment Values", file=sys.stderr)
    print(happy, file=sys.stderr)
    print(neutral, file=sys.stderr)
    print(sad, file=sys.stderr)
    print(totalComments, file=sys.stderr)

    inputComand = "UPDATE activities SET happy = %s, neutral = %s, sad = %s, totalcomments = %s WHERE activity_id = (%s)"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputComand, (happy, neutral,
                                        sad, totalComments, activity_id,))
        conn.commit()
        statement.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
            return err


def checkLikeDB(user_id, activity_id):
    inputCommand = "SELECT user_id FROM activitylikes WHERE (user_id = %s AND activity_id = %s)"

    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (user_id, activity_id,))

        rs = statement.fetchone()
        statement.close()
        conn.close()
        if rs is not None:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
            return err


def addLike(title, user_id, activity_id):
    inputCommand = "UPDATE activities SET likes = likes + 1 WHERE (title = %s AND activity_id = %s)"
    inputCommand2 = "INSERT INTO activitylikes (user_id, activity_id) VALUES(%s,%s)"
    inputCommand3 = "SELECT user_id FROM activitylikes WHERE (user_id = %s AND activity_id = %s)"
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand3, (user_id, activity_id,))

        rs = statement.fetchone()

        if rs is not None:
            return False

        statement.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print(err, file=sys.stderr)
            conn.close()
            return err

        statement.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print(err, file=sys.stderr)
            conn.close()
            return err

    try:
        conn2 = connect()
        statement2 = conn2.cursor()
        print(user_id, file=sys.stderr)
        print(activity_id, file=sys.stderr)
        statement2.execute(inputCommand2, (user_id, activity_id,))
        conn2.commit()

        statement2.close()
        conn2.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print(err, file=sys.stderr)
            conn.close()
            return err


def removeLike(user_id, activity_id):
    inputCommand = "DELETE FROM activitylikes WHERE (user_id = (%s) AND activity_id = (%s))"

    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputCommand, (user_id, activity_id,))
        conn.commit()

        statement.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
            print(err, file=sys.stderr)
            return False


def getLikes(activity_id):
    inputCommand = "SELECT * FROM activitylikes WHERE activity_id = %s"
    likes = 0
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (activity_id,))
        for row in statement:
            likes = likes + 1

        return likes

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print(err, file=sys.stderr)
            conn.close()
            return False
