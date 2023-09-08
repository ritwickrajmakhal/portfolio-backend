from flask import Flask, request
import sqlite3
from flask_cors import CORS  # Import Flask-CORS
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://ritwickrajmakhal.github.io"])  # Enable CORS for your app
 
    
@app.route('/api/likes/<int:portfolio_id>', methods=['GET', 'POST'])
def get_likes(portfolio_id):
    # Azure Blob Storage configuration
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=portfolioblobstorage;AccountKey=gWeWtzz57UqCwvwiUeHDI3gLTJv34vAkOhacYe8v/HQbuPdfQsFBExcmBBxYUnKJE4M7u16oFMAI+ASt1yqoTQ==;EndpointSuffix=core.windows.net")
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
        db.close()
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        with open("database.sqlite", "rb") as blob_file:
            blob_client.upload_blob(blob_file, overwrite=True)
        return "success"

if __name__ == '__main__':
    app.run()
