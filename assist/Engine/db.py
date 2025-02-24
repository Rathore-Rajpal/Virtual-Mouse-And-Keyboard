import sqlite3

conn = sqlite3.connect("buddy.db")
cursor = conn.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VAR(100), path VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null,'android studio','C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO sys_command VALUES (null,'one note','C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO sys_command VALUES (null,'one note','C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
#cursor.execute(query)
#conn.commit()

#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VAR(100), url VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO web_command VALUES (null,'canva','https://www.canva.com/')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO web_command VALUES (null,'youtube','https://youtube.com/')"
#cursor.execute(query)
#conn.commit()

