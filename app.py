from flask import Flask, request
import json
import sqlite3
from flask_cors import CORS  # Import Flask-CORS
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

app = Flask(__name__)
# Enable CORS for your app
CORS(app, origins=["http://localhost:3000",
     "https://ritwickrajmakhal.github.io"])


def download_file():
    # Azure Blob Storage configuration
    blob_service_client = BlobServiceClient.from_connection_string(
        "DefaultEndpointsProtocol=https;AccountName=portfolioblobstorage;AccountKey=gWeWtzz57UqCwvwiUeHDI3gLTJv34vAkOhacYe8v/HQbuPdfQsFBExcmBBxYUnKJE4M7u16oFMAI+ASt1yqoTQ==;EndpointSuffix=core.windows.net")
    container_name = "databases"
    blob_name = "database.sqlite"
    db = sqlite3.connect("database.sqlite")

    # Download the SQLite database file from Azure Blob Storage to the local file system
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    with open("database.sqlite", "wb") as blob_file:
        blob_data = blob_client.download_blob()
        blob_data.readinto(blob_file)
    cursor = db.cursor()
    return cursor, db, container_client, blob_client


def upload_file(db, container_client, blob_client):
    # Upload the SQLite database file from the local file system to Azure Blob Storage
    with open("database.sqlite", "rb") as blob_file:
        blob_client.upload_blob(blob_file, overwrite=True)
    db.close()


@app.route('/api/likes', methods=['GET', 'POST'])
def get_likes():
    cursor, db, container_client, blob_client = download_file()
    portfolio_id = request.args.get('portfolioid')
    if request.method == 'GET':
        # get the likes for the portfolio_id
        cursor.execute(
            "SELECT likes FROM likesCounter WHERE portfolio_id = ?", (portfolio_id,))
        data = cursor.fetchone()
        cursor.close()
        if data is None:
            return "0"
        else:
            return str(data[0])
    else:
        # increment the likes by 1 if the portfolio_id exists else create a new entry
        cursor.execute(
            "INSERT INTO likesCounter (portfolio_id, likes) VALUES (?, 1) ON CONFLICT(portfolio_id) DO UPDATE SET likes = likes + 1", (portfolio_id,))
        db.commit()
        cursor.close()
        upload_file(db, container_client, blob_client)
        return "success"


@app.route('/api/comments', methods=['GET', 'POST'])
def get_comments():
    portfolio_id = request.args.get('portfolioid')
    cursor, db, container_client, blob_client = download_file()
    if request.method == 'GET':
        # get the comments for the portfolio_id
        cursor.execute(
            "SELECT * FROM comments WHERE portfolio_id = ?", (portfolio_id,))
        # Fetch all the data rows and convert them to dictionaries
        columns = [desc[0] for desc in cursor.description]
        # Fetch all the data rows
        data = cursor.fetchall()

        # Create a list of dictionaries where column names are used as keys
        result_data = [dict(zip(columns, row)) for row in data]

        # Convert the result_data to JSON
        json_data = json.dumps(result_data)

        return json_data
    else:
        comment = request.args.get('comment')
        username = request.args.get('username')
        cursor.execute("INSERT INTO comments (portfolio_id, username, comment) VALUES (?, ?, ?) ",
                       (portfolio_id, username if username else 'Anonymous', comment,))
        db.commit()
        cursor.close()
        upload_file(db, container_client, blob_client)
        return "success"


if __name__ == '__main__':
    app.run()
