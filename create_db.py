import mysql.connector

# Connect to MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shiva"
)

cursor = conn.cursor()

# Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS sportsphere CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

print("Database 'sportsphere' created successfully!")

# Close connection
conn.close()
