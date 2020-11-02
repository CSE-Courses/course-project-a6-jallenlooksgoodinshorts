import mysql.connector
from mysql.connector import errorcode
import os
import sys


def connect():
    database = mysql.connector.connect(user='k7aqgz64ljyxr9w9',
                                       password='jl2ymrryvog4t8hu',
                                       host='durvbryvdw2sjcm5.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
                                       database='mh4057an9aee5vxa'
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
    inputValues = "INSERT INTO users (email, password, fname, lname, username) VALUES(%s,%s,%s,%s,%s);"
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


def userInfo(username):
    inputCommand = "SELECT email, fname, lname, username, about, interests FROM users WHERE email = %s OR fname = (%s) OR username = (%s)"
    try:
        conn = connect()
        statement = conn.cursor()
        statement.execute(inputCommand, (username, username, username,))

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


def createActivity(title, description, image):  # Needs to be updated for likes
    inputValues = "INSERT INTO activities (title, description, image, likes) VALUES(%s,%s,%s,%s);"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        # Needs to be updated for likes
        statement.execute(inputValues, (title, description, image, 0))
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
    inputCommand = "SELECT title, description, image, likes, activity_id FROM activities WHERE activity_id = (%s)"
    try:
        conn = connect()
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


def editInfo(username, location, gender, about, interests):
    inputCommand = "SELECT * FROM userInfo WHERE email = %s"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputCommand, (username,))

        rs = statement.fetchone()

        if rs is not None:
            updateInfo = "UPDATE userInfo SET location = %s, gender = %s, about = %s, interests = %s WHERE email = %s"
            info = conn.cursor(prepared=True)
            info.execute(updateInfo, (location, gender,
                                      about, interests, username))
            info.close()
            conn.close()
            return True

        else:
            newInfo = "INSERT INTO userInfo (email,location,gender,about,interest) VALUES (%s,%s,%s,%s,%s)"
            info = conn.cursor(prepared=True)
            info.execute(newInfo, (username, location,
                                   gender, about, interests))
            info.close()
            conn.close()
            return True

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
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
