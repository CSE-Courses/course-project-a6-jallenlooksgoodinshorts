import mysql.connector
from mysql.connector import errorcode

def connect():
    return mysql.connector.connect(user='t8UFMyPCs3',password='RZfgggcfAg',host='remotemysql.com',database='t8UFMyPCs3')


def testConn():
    try:
        db = connect()
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

        return rs[0]

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username/password issue')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('databse not found')
    else:
        conn.close()

    #Have return email of new user

def loginUser(username, password):
    inputCommand = "SELECT * FROM username WHERE NAMES = %s AND password = %s"
    try:
        conn = connect()
        statement = conn.cursor(prepared=True)
        statement.execute(inputCommand, (username, password))

        rs = statement.fetchone()

        if rs is not None:
            print("Successful Login")
        else:
            print("Username/Password not found")

        statement.close()
        conn.close()

        return rs[0]

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()

#have return email of validated user