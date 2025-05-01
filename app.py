from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# MongoDB connection string from Render environment variable
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

# Use database and collections
db = client["website"]  # You can change this name if desired
signups_collection = db["signups"]
clicks_collection = db["clicks"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/save-user', methods=['POST'])
def save_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    org = data.get("org")

    # Store in MongoDB
    signups_collection.insert_one({
        "name": name,
        "email": email,
        "org": org
    })

    return jsonify({"status": "success"}), 200

@app.route('/api/track-click', methods=['POST'])
def track_click():
    clicks_collection.insert_one({"event": "button_clicked"})
    return jsonify({"status": "click recorded"}), 200

@app.route('/api/track-video-play', methods=['POST'])
def track_video_play():
    clicks_collection.insert_one({"event": "video_played"})
    return jsonify({"status": "video play recorded"}), 200

if __name__ == '__main__':
    app.run(port=4242)
