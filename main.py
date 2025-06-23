import sqlite3

conn = sqlite3.connect('database.db')
curs = conn.cursor()


curs.execute('SELECT rowid, * FROM mahasiswatb')
all = curs.fetchall()
for i in all:
    print(f"{i}")


conn.commit()
conn.close()    
