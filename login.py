import mysql.connector
from mysql.connector import errorcode


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
