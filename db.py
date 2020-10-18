import mysql.connector
from mysql.connector import errorcode
import os 
import sys

def connect():
    database = mysql.connector.connect( user = 'k7aqgz64ljyxr9w9', 
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

def newUser(email,password,fname,lname,username):
    inputValues = "INSERT INTO users VALUES(%s,%s,%s,%s,%s);"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputValues, (email,password,fname,lname,username))
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

def createActivity(title, description, image): # Needs to be updated for likes
    inputValues = "INSERT INTO activities (title, description, image, likes) VALUES(%s,%s,%s,%s);"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputValues, (title,description,image,0)) # Needs to be updated for likes
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

def joinActivityDB(user_id, activity_id) :
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

def getActivityIDs(user_id) :
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

#have return email of validated user