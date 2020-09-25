import mysql.connector
from mysql.connector import errorcode


def testConn():
    try:
        conn = mysql.connector.connect(user='kgood',password='cse442a6',host='127.0.0.1',database='userdata')
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
        conn = mysql.connector.connect(user='kgood',password='cse442a6',host='127.0.0.1',database='userdata')
        statement = conn.cursor(prepared=True)
        statement.execute(inputValues, (email,password,fname,lname,username))
        conn.commit()

        statement.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username/password issue')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('databse not found')
    else:
        conn.close()
