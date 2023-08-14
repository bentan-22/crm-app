import mysql.connector

# Connect to the MySQL server
dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    password='pAsswoRd321'  # Use 'password' instead of 'passwd'
)

# Prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE website")

print("All done!")

# Close the cursor and connection
cursorObject.close()
dataBase.close()