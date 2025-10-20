from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI(title="Movie Streaming Platform API")

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_streaming"]

movies_collection = db["movies"]
users_collection = db["users"]
watch_history_collection = db["watch_history"]

def get_user_history(user_id:str):
    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400,detail="Invalid User ID")

    user_details = users_collection.find_one(
        {"_id":user_object_id},
        {"_id":1,"name":1,"email":1,"subscription_type":1}
    )
    if not user_details:
        raise HTTPException(status_code = 400,detail="This user doesn't exist")

    pipeline = [
        {"$match":{"user_id":user_object_id}},
        {"$lookup":{
            "from":"movies",
            "localField":"movie_id",
            "foreignField":"_id",
            "as":"movie_details"
        }},
        {"$unwind":"$movie_details"},
        {"$project":{
            "_id":0,
            "title":"$movie_details.title",
            "watched_at":1,
            "watch_duration":1,
            "popularity":"$movie_details.popularity"
        }}
    ]

    history = list(watch_history_collection.aggregate(pipeline))

    response = {
        "user_id":str(user_details['_id']),
        "name":user_details["name"],
        "email":user_details["email"],
        "subscription_type":user_details["subscription_type"],
        "watched_movies":history
    }

    return response
