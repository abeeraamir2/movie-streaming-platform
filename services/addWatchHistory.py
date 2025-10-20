from fastapi import Body, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_streaming"]

users_collection = db["users"]
movies_collection = db["movies"]
watch_history_collection = db["watch_history"]

def add_watch_history(
    user_id: str,
    movie_id: str = Body(...),
    duration: int = Body(...)
):
    if not users_collection.find_one({"_id": ObjectId(user_id)}):
        raise HTTPException(status_code=404, detail="User not found")

    
    movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")


    previous_watches = watch_history_collection.count_documents({
        "user_id": ObjectId(user_id),
        "movie_id": ObjectId(movie_id)
    })

    increment = previous_watches + 1

    watch_entry = {
        "user_id": ObjectId(user_id),
        "movie_id": ObjectId(movie_id),
        "watched_at": datetime.utcnow(),
        "duration": duration
    }
    watch_history_collection.insert_one(watch_entry)

    movies_collection.update_one(
        {"_id": ObjectId(movie_id)},
        {"$inc": {"popularity": increment}}
    )

    return {
        "message": "Watch history added & movie popularity updated",
        "popularity_increment": increment
    }
