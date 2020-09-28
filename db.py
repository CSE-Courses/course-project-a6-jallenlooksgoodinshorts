import mysql.connector
from mysql.connector import errorcode

def connect():
    database = mysql.connector.connect(user='k7aqgz64ljyxr9w9', password='jl2ymrryvog4t8hu' ,host='durvbryvdw2sjcm5.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', database='mh4057an9aee5vxa')
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
    inputValues = "INSERT INTO users (email, password, first_name, last_name, username)VALUES(%s,%s,%s,%s,%s);"
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
            statement.close()
            conn.close()

            return rs[0]
        else:
            print("Username/Password not found")

            statement.close()
            conn.close()

            return None

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied Error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            conn.close()
        return None

#have return email of validated user