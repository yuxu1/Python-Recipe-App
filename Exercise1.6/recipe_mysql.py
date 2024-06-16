# Connect script to MySQL server
# Import module
import mysql.connector

# Initialize connection object 'conn'
conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

# Initialize cursor object from conn
cursor = conn.cursor()

# Create & access database (avoid duplicate)
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

# Create Recipes table (avoid duplicate)
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    ingredients VARCHAR(225),
    cooking_time INT,
    difficulty VARCHAR(20)
)''')