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

def loginUser(username, password):
    inputCommand = "SELECT * FROM username WHERE NAMES = %s AND password = %s"
    try:
        con = mysql.connector.connect(user="root", password="1234", host="localhost", database="userdata")
        statement = con.cursor(prepared=True)
        statement.execute(inputCommand, (username, password))

        rs = statement.fetchone()

        if rs is not None:
            print("Successful Login")
        else:
            print("Username/Password not found")

        statement.close()
        con.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            con.close()
