from flask import Flask, request
import sqlite3
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://ritwickrajmakhal.github.io"])  # Enable CORS for your app

@app.route('/api/likes/<int:portfolio_id>', methods=['GET', 'POST'])
def get_likes(portfolio_id):
    db = sqlite3.connect("database.sqlite")
    cursor = db.cursor()
    if request.method == 'GET':

        # get the likes for the portfolio_id
        cursor.execute("SELECT likes FROM likesCounter WHERE portfolio_id = ?", (portfolio_id,))
        data = cursor.fetchone()
        if data is None:
            return "0"
        else:
            return str(data[0])
    else:
        # increment the likes by 1 if the portfolio_id exists else create a new entry
        cursor.execute("INSERT INTO likesCounter (portfolio_id, likes) VALUES (?, 1) ON CONFLICT(portfolio_id) DO UPDATE SET likes = likes + 1", (portfolio_id,))
        db.commit()
        return "success"

if __name__ == '__main__':
    app.run()
