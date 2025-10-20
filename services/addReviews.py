from fastapi import Body, HTTPException
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient, errors

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_streaming"]

users_collection = db["users"]
movies_collection = db["movies"]
reviews_collection = db["reviews"]

def add_review(
    user_id: str,
    movie_id: str = Body(...),
    rating: float = Body(...),
    text_review: str = Body(...)
):
    try:
        user_obj = ObjectId(user_id)
        movie_obj = ObjectId(movie_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id or movie_id format")

    if not users_collection.find_one({"_id": user_obj}):
        raise HTTPException(status_code=404, detail="User not found")

    movie = movies_collection.find_one({"_id": movie_obj})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    review_entry = {
        "user_id": user_obj,
        "movie_id": movie_obj,
        "rating": rating,
        "text_review": text_review,
        "created_at": datetime.utcnow()
    }

    try:
        reviews_collection.insert_one(review_entry)
    except errors.DuplicateKeyError:
        reviews_collection.update_one(
            {"user_id": user_obj, "movie_id": movie_obj},
            {"$set": {
                "rating": rating,
                "text_review": text_review,
                "updated_at": datetime.utcnow()
            }}
        )
    
    all_reviews = list(reviews_collection.find({"movie_id": movie_obj}, {"rating": 1}))
    total_reviews = len(all_reviews)
    total_rating = sum(r["rating"] for r in all_reviews)
    avg_rating = round(total_rating / total_reviews, 2) if total_reviews > 0 else 0.0
    
    movies_collection.update_one(
        {"_id": movie_obj},
        {"$set": {
            "rating.average": avg_rating,
            "rating.review_count": total_reviews
        }}
    )

    return {
        "message": "Review added or updated successfully",
        "new_average": avg_rating,
        "total_reviews": total_reviews
    }
