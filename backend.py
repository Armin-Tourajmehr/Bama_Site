import mysql.connector

# First You have to build your database in SQL

# Connect to database
def connect():
    cnx = mysql.connector.connect(user='root', password='****', host='127.0.0.1', database='bama')
    cnx.close()


def insert_name_model(name, model, func, city, price):
    cnx = mysql.connector.connect(user='root', password='****', host='127.0.0.1', database='bama')
    cur = cnx.cursor()
    cur.execute('INSERT IGNORE INTO sell VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' %
                (name, model, func, city, price))
    cnx.commit()
    cnx.close()



def select_date():
    cnx = mysql.connector.connect(user='root', password='****', host='127.0.0.1', database='bama')
    cur = cnx.cursor()
    cur.execute('SELECT * FROM sell WHERE price IS NOT NULL')
    rows = cur.fetchall()
    cnx.close()
    return rows


connect()
