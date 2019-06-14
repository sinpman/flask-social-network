# from peewee import *
#
# DATABASE = SqliteDatabase('social.db')
#
# DATABASE.execute('''select * from user''')
# print ("Opened database successfully")
#
#

#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('social.db')
print("Opened database successfully")

cursor = conn.execute("select * from user")
print(cursor.description)



cursor2 = conn.execute("select * from post")
print(cursor2.description)
for i in cursor2:
    print(i)

print("Operation done successfully")
conn.close()