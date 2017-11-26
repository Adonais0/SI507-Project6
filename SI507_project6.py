# Import statements
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import requests
from config import *
import sys
import json
import csv

# Write code / functions to set up database connection and cursor here.
def get_connection_and_cursor():
    try:
        if db_password != "": #database has password
            db_connection = psycopg2.connect("dbname = '{0}' user='{1}' password='{2}'".format(db_name,db_user,db_password))
            print("connect successfully to database")
        else: #database doesn't have password
            db_connection = psycopg2.connect("dbname = '{0}' user='{1}'".format(db_name,db_user))
    except:
        print("Fail to connect to server")
        sys.exit(1)
    db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, db_cursor

# Write code / functions to create tables with the columns you want and all database setup here.
def setup_database():
    #create table Sites
    #FOREIGN KEY(child_id) REFERENCES child(id),
    db_cursor.execute("CREATE TABLE States(id SERIAL UNIQUE, name VARCHAR(128) PRIMARY KEY)")

    db_cursor.execute("CREATE TABLE Sites(id SERIAL, name VARCHAR(128) PRIMARY KEY,type VARCHAR(128), state_id INTEGER REFERENCES States (id), location VARCHAR(255), description TEXT)")
    #create table

    db_connection.commit()
    print('Setup database complete')

# Write code / functions to deal with CSV files and insert data into the database here.
def insert(conn, cur, table, data_dict, no_return=True):
    column_names = data_dict.keys()
    print(column_names,"column_names")
    if not no_return: #if return
        query = sql.SQL('INSERT INTO {0}({1}) VALUES({2}) ON CONFLICT DO NOTHING RETURNING id').format(
            sql.SQL(table),
            sql.SQL(', ').join(map(sql.Identifier, column_names)),
            sql.SQL(', ').join(map(sql.Placeholder, column_names))
        )
    else:
        query = sql.SQL('INSERT INTO {0}({1}) VALUES ({2}) ON CONFLICT DO NOTHING').format(
            sql.SQL(table),
            sql.SQL(', ').join(map(sql.Identifier, column_names)),
            sql.SQL(', ').join(map(sql.Placeholder,column_names))
        )
    query_string = query.as_string(conn)
    cur.execute(query_string, data_dict)
    db_connection.commit()
    print("successfully inserted")
    if not no_return:
        return cur.fetchone()

def csv_to_dict_list(csvFile):
    f = csv.reader(open(csvFile,'r'))
    next(f)
    i = 1
    list_of_dict = []
    for row in f:
        row.insert(0,i)
        i = i+1
        row[3], row[2] = row[2], row[3]
        #row.insert(3,0)# state id to be modified later
        del row[-2]

        dict_of_csv = {}
        dict_of_csv['id'] = row[0]
        dict_of_csv['name'] = row[1]
        dict_of_csv['type'] = row[2]
        #dict_of_csv['state_id'] = row[3]
        dict_of_csv['location'] = row[3]
        dict_of_csv['description'] = row[4]
        list_of_dict.append(dict_of_csv)
    return list_of_dict
states_list = [{'id':1,'name':'arkansas'},{'id':2,'name':'michigan'},{'id':3,'name':'california'}]
# Make sure to commit your database changes with .commit() on the database connection.
db_connection,db_cursor = get_connection_and_cursor()#connect to the database
setup_database()
ar_dict_list = csv_to_dict_list('arkansas.csv')
for ar_dict in states_list:
    print(ar_dict)
    insert(db_connection, db_cursor, "states", ar_dict)
# for ar_dict in ar_dict_list:
#     insert(db_connection, db_cursor, "sites", ar_dict)


# Write code to be invoked here (e.g. invoking any functions you wrote above)
# if __name__ == '__main__':
#     #execute command line arguments
#     command = None
#     search_term = None
#     if len(sys.argv) > 1:
#         command = sys.argv[1]
#         if len(sys.argv) > 2:
#             search_term = sys.argv[2]
#
#     if command == 'setup':
#         print('setting up the database')
#         setup_database()
#     elif command == 'search':
#         print('searching', search_item)


# Write code to make queries and save data in variables here.






# We have not provided any tests, but you could write your own in this file or another file, if you want.
