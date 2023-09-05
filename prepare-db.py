import sqlite3
db = sqlite3.connect("database.sqlite")
cursor = db.cursor()
# create a table which stores the likes and dislikes for each portfolio
cursor.execute("CREATE TABLE IF NOT EXISTS likesCounter (portfolio_id INTEGER PRIMARY KEY, likes INTEGER DEFAULT 0, dislikes INTEGER DEFAULT 0)")
db.commit()




