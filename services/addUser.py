from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_streaming"]

users_collection = db["users"]

def create_user(name: str, email: str, subscription_type: str):
    user = {
        "name": name,
        "email": email,
        "subscription_type": subscription_type,
        "created_at": datetime.utcnow()
    }
    result = users_collection.insert_one(user)
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}