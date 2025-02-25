import csv
import sqlite3

conn = sqlite3.connect("buddy.db")
cursor = conn.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VAR(100), path VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null,'android studio','C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO sys_command VALUES (null,'one note','C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO sys_command VALUES (null,'vs code','C:\\Users\\rajpa\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')"
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

#query = "DELETE FROM sys_command WHERE id = 3;"
#cursor.execute(query)
#conn.commit()

# Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
#desired_columns_indices = [0, 30]

# Read data from CSV and insert into SQLite table for the desired columns
#with open('C:\\VirtualMouseProject\\contacts.csv', 'r', encoding='utf-8') as csvfile:

    #csvreader = csv.reader(csvfile)
    #for row in csvreader:
       # if len(row) > max(desired_columns_indices):  # Ensure the row has enough columns
            #selected_data = [row[i] for i in desired_columns_indices]
            #cursor.execute('''INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))
        #else:
            #print(f"Skipping row, not enough columns: {row}")



# Commit changes and close connection
#conn.commit()
#conn.close()

#query = "INSERT INTO contacts VALUES (null,'Shweta','917020264223','')"
#cursor.execute(query)
#conn.commit()

query = "INSERT INTO contacts VALUES (null,'raj','9175442260','')"
cursor.execute(query)
conn.commit()

