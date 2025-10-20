from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_streaming"]

watch_history_collection = db["watch_history"]
movies_collection = db["movies"]

def get_top_watched_movies(limit: int = 5, days: int = 30):
    one_month_ago = datetime.utcnow() - timedelta(days=days)
    
    pipeline = [
        {"$match": {"watched_at": {"$gte": one_month_ago}}},
        {"$group": {"_id": "$movie_id", "watch_count": {"$sum": 1}}},
        {"$sort": {"watch_count": -1}},
        {"$limit": limit},
        {
            "$lookup": {
                "from": "movies",
                "localField": "_id",
                "foreignField": "_id",
                "as": "movie_info"
            }
        },
        {"$unwind": "$movie_info"},
        {
            "$project": {
                "_id": 0,
                "movie_id": {"$toString":"$_id"},
                "title": "$movie_info.title",
                "watch_count": 1
            }
        }
    ]
    
    return list(db.watch_history.aggregate(pipeline))
