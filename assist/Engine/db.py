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



#SEARCHING
#query = 'Shweta'
#query = query.strip().lower()

#cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#results = cursor.fetchall()
#print(results[0][0])

#query = "DELETE FROM contacts"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO contacts VALUES (null,'Shweta Verma','7020264223','')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO contacts VALUES (null,'raj','9175442260','')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO contacts VALUES (null,'Arya Rai','8010645336','')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO contacts VALUES (null,'Ritesh Sable','8530778124','')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO contacts VALUES (null,'Yash Padwal','8731809331','')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO contacts VALUES (null,'Ayush','8943078101','')"
#cursor.execute(query)
#conn.commit

#query = "INSERT INTO contacts VALUES (null,'Sister','6377281524','')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO contacts VALUES (null,'Mom','8829976187','')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO contacts VALUES (null,'Mum','8829976187','')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO sys_command VALUES (null,'virtual keyboard','C:\\VirtualMouseProject\\assist\\www\\virtualKeyBoard.html')"
#cursor.execute(query)
#conn.commit()

#query = "UPDATE sys_command set name = 'imagemaster' where id = 18"
#cursor.execute(query)
#conn.commit() 

# Insert statements for popular websites

# Google
query = "INSERT INTO web_command VALUES (null, 'google', 'https://www.google.com/')"
cursor.execute(query)
conn.commit()

# Facebook
query = "INSERT INTO web_command VALUES (null, 'facebook', 'https://www.facebook.com/')"
cursor.execute(query)
conn.commit()

# Twitter
query = "INSERT INTO web_command VALUES (null, 'twitter', 'https://www.twitter.com/')"
cursor.execute(query)
conn.commit()

# Instagram
query = "INSERT INTO web_command VALUES (null, 'instagram', 'https://www.instagram.com/')"
cursor.execute(query)
conn.commit()

# LinkedIn
query = "INSERT INTO web_command VALUES (null, 'linkedin', 'https://www.linkedin.com/')"
cursor.execute(query)
conn.commit()

# Reddit
query = "INSERT INTO web_command VALUES (null, 'reddit', 'https://www.reddit.com/')"
cursor.execute(query)
conn.commit()

# GitHub
query = "INSERT INTO web_command VALUES (null, 'github', 'https://www.github.com/')"
cursor.execute(query)
conn.commit()

# Stack Overflow
query = "INSERT INTO web_command VALUES (null, 'stackoverflow', 'https://stackoverflow.com/')"
cursor.execute(query)
conn.commit()

# Wikipedia
query = "INSERT INTO web_command VALUES (null, 'wikipedia', 'https://www.wikipedia.org/')"
cursor.execute(query)
conn.commit()

# Amazon
query = "INSERT INTO web_command VALUES (null, 'amazon', 'https://www.amazon.com/')"
cursor.execute(query)
conn.commit()

# Netflix
query = "INSERT INTO web_command VALUES (null, 'netflix', 'https://www.netflix.com/')"
cursor.execute(query)
conn.commit()

# Spotify
query = "INSERT INTO web_command VALUES (null, 'spotify', 'https://www.spotify.com/')"
cursor.execute(query)
conn.commit()

# Dropbox
query = "INSERT INTO web_command VALUES (null, 'dropbox', 'https://www.dropbox.com/')"
cursor.execute(query)
conn.commit()

# Zoom
query = "INSERT INTO web_command VALUES (null, 'zoom', 'https://zoom.us/')"
cursor.execute(query)
conn.commit()

# Pinterest
query = "INSERT INTO web_command VALUES (null, 'pinterest', 'https://www.pinterest.com/')"
cursor.execute(query)
conn.commit()

# WhatsApp Web
query = "INSERT INTO web_command VALUES (null, 'whatsapp web', 'https://web.whatsapp.com/')"
cursor.execute(query)
conn.commit()

# Microsoft
query = "INSERT INTO web_command VALUES (null, 'microsoft', 'https://www.microsoft.com/')"
cursor.execute(query)
conn.commit()

# Insert statements for more popular websites

# Gmail
query = "INSERT INTO web_command VALUES (null, 'gmail', 'https://mail.google.com/')"
cursor.execute(query)
conn.commit()

# Google Photos
query = "INSERT INTO web_command VALUES (null, 'google photos', 'https://photos.google.com/')"
cursor.execute(query)
conn.commit()

# Apple
query = "INSERT INTO web_command VALUES (null, 'apple', 'https://www.apple.com/')"
cursor.execute(query)
conn.commit()

# Google Maps
query = "INSERT INTO web_command VALUES (null, 'google maps', 'https://maps.google.com/')"
cursor.execute(query)
conn.commit()

# iCloud
query = "INSERT INTO web_command VALUES (null, 'icloud', 'https://www.icloud.com/')"
cursor.execute(query)
conn.commit()

# Google Drive
query = "INSERT INTO web_command VALUES (null, 'google drive', 'https://drive.google.com/')"
cursor.execute(query)
conn.commit()












