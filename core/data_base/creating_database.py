import sqlite3 as sq

connection = sq.connect("database.db")
cursor = connection.cursor()


async def create_database():
    cursor.execute(
        """
	    CREATE TABLE IF NOT EXISTS users (
	        user_id INTEGER PRIMARY KEY,
	        username TEXT,
	        first_name TEXT,
	        last_name TEXT
	    )
	"""
    )
    connection.commit()
    connection.close()
