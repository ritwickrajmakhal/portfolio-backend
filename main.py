from flask import Flask
import sqlite3
app = Flask(__name__)

@app.route('/api/likes/<int:portfolio_id>', methods=['POST'])
def add_like(portfolio_id):
    db = sqlite3.connect("database.sqlite")
    cursor = db.cursor()
    # increment the likes by 1 if the portfolio_id exists else create a new entry
    cursor.execute("INSERT INTO likesCounter (portfolio_id, likes) VALUES (?, 1) ON CONFLICT(portfolio_id) DO UPDATE SET likes = likes + 1", (portfolio_id,))
    db.commit()
    return "success"

@app.route('/api/dislikes/<int:portfolio_id>', methods=['POST'])
def add_dislike(portfolio_id):
    db = sqlite3.connect("database.sqlite")
    cursor = db.cursor()
    # increment the dislikes by 1 if the portfolio_id exists else create a new entry
    cursor.execute("INSERT INTO likesCounter (portfolio_id, dislikes) VALUES (?, 1) ON CONFLICT(portfolio_id) DO UPDATE SET dislikes = dislikes + 1", (portfolio_id,))
    db.commit()
    return "success"

@app.route('/api/likes/<int:portfolio_id>', methods=['GET'])
def get_likes(portfolio_id):
    db = sqlite3.connect("database.sqlite")
    cursor = db.cursor()
    # get the likes for the portfolio_id
    cursor.execute("SELECT likes FROM likesCounter WHERE portfolio_id = ?", (portfolio_id,))
    data = cursor.fetchone()
    if data is None:
        return "0"
    else:
        return str(data[0])
    
@app.route('/api/dislikes/<int:portfolio_id>', methods=['GET'])
def get_dislikes(portfolio_id):
    db = sqlite3.connect("database.sqlite")
    cursor = db.cursor()
    # get the dislikes for the portfolio_id
    cursor.execute("SELECT dislikes FROM likesCounter WHERE portfolio_id = ?", (portfolio_id,))
    data = cursor.fetchone()
    if data is None:
        return "0"
    else:
        return str(data[0])
    

if __name__ == '__main__':
    app.run(debug=True)