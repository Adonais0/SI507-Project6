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

    db_cursor.execute("CREATE TABLE Sites(id SERIAL, name VARCHAR(128) PRIMARY KEY,type VARCHAR(128), state_id INTEGER, location VARCHAR(255), description TEXT)")
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

def csv_to_dict_list(csvFile,i,s_id):
    f = csv.reader(open(csvFile,'r'))
    next(f)
    list_of_dict = []
    for row in f:
        row.insert(0,i)
        i = i+1
        row[3], row[2] = row[2], row[3]
        del row[-2]

        dict_of_csv = {}
        dict_of_csv['id'] = row[0]
        dict_of_csv['name'] = row[1]
        dict_of_csv['type'] = row[2]
        dict_of_csv['state_id'] = s_id
        dict_of_csv['location'] = row[3]
        dict_of_csv['description'] = row[4]
        list_of_dict.append(dict_of_csv)
    return list_of_dict
states_list = [{'id':1,'name':'arkansas'},{'id':2,'name':'michigan'},{'id':3,'name':'california'}]
# Make sure to commit your database changes with .commit() on the database connection.
db_connection,db_cursor = get_connection_and_cursor()#connect to the database
setup_database()
dict_list = []
ar_dict_list = csv_to_dict_list('arkansas.csv',1,1)
print(len(ar_dict_list))
mi_dict_list = csv_to_dict_list('michigan.csv',len(ar_dict_list)+1,2)
print(len(ar_dict_list)+len(mi_dict_list))
ca_dict_list = csv_to_dict_list('california.csv',16,3)
for d in ar_dict_list:
    dict_list.append(d)
for d in mi_dict_list:
    dict_list.append(d)
for d in ca_dict_list:
    dict_list.append(d)

for ar_dict in states_list:
    print(ar_dict)
    insert(db_connection, db_cursor, "states", ar_dict)
    #successfully inserted state table
for d in dict_list:
    print(d['id'])
    insert(db_connection, db_cursor, "sites", d)

# Write code to be invoked here (e.g. invoking any functions you wrote above)
def execute_and_print(query, numer_of_results=1):
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    for r in results[:numer_of_results]:
        print(r)
    print('--> Result Rows:', len(results))
    print()
    return results


# Write code to make queries and save data in variables here.
all_locations = execute_and_print('SELECT "location" FROM "sites" ')
print(all_locations)

beautiful_sites = execute_and_print(""" SELECT "name" FROM "sites" WHERE "description" LIKE '%beautiful%' """)
print(beautiful_sites)

natl_lakeshores = execute_and_print(""" SELECT COUNT(*) FROM "sites" WHERE "type" LIKE 'National Lakeshore' """)
print(natl_lakeshores)

michigan_names = execute_and_print(""" SELECT ("sites"."name") FROM "sites" INNER JOIN "states" ON ("sites"."state_id" = 2)""")
print(michigan_names)

total_number_arkansas = execute_and_print("""
SELECT COUNT(*) FROM "sites"
  WHERE
    state_id = 1 """)
print(total_number_arkansas)




# We have not provided any tests, but you could write your own in this file or another file, if you want.
