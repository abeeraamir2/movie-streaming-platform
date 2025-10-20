from fastapi import FastAPI,HTTPException
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI(title="Movie Streaming Platform API")

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_streaming"]

movies_col = db["movies"]
reviews_col = db["reviews"]
users_col = db["users"]

def convert_objectid(obj):
    if isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

def get_movie_reviews(movie_id: str):
    try:
        movie = movies_col.find_one({"_id": ObjectId(movie_id)})
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        reviews = list(reviews_col.aggregate([
            {"$match": {"movie_id": ObjectId(movie_id)}},
            {"$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user_details"
            }},
            {"$unwind": {"path": "$user_details", "preserveNullAndEmptyArrays": True}},
            {"$project": {
                "_id": 1,
                "user_id": 1,
                "movie_id": 1,
                "rating": 1,
                "comment": 1,
                "created_at": 1,
                "user_details.username": 1,
                "user_details.email": 1
            }}
        ]))

        response = {
            "movie_id": str(movie["_id"]),
            "title": movie.get("title"),
            "total_reviews": len(reviews),
            "reviews": reviews
        }

        response = convert_objectid(response)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
