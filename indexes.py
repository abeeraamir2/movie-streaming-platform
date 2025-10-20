from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.errors import OperationFailure

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "movie_streaming"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

#Indexes on movies 
db.movies.create_index(
    [
        ("title", TEXT),
        ("director", TEXT),
        ("cast.name", TEXT),
    ],
    name="movie_text_search",
    default_language="english"
)
print("Created text index: movie_text_search")

db.movies.create_index(
    [("title", ASCENDING)],
    name="movie_title_index"
)
print("Created ascending index: movie_title_index")

db.movies.create_index(
    [("rating.average", DESCENDING), ("popularity", DESCENDING)],
    name="movie_hybrid_rank_index"
)
print("Created compound index: movie_hybrid_rank_index")


#Indexes on watch_history
db.watch_history.create_index(
    [("user_id", ASCENDING), ("watch_date", DESCENDING)],
    name="watch_user_recent_index"
)
print("Created index: watch_user_recent_index (user_id, watch_date)")

db.watch_history.create_index(
    [("movie_id", ASCENDING), ("watch_date", DESCENDING)],
    name="watch_movie_recent_index"
)
print("Created index: watch_movie_recent_index (movie_id, watch_date)")

db.watch_history.create_index(
    [("user_id", ASCENDING), ("movie_id", ASCENDING)],
    name="watch_user_movie_index"
)
print("Created index: watch_user_movie_index (user_id, movie_id)")


#Index on reviews
db.reviews.create_index(
    [("movie_id", ASCENDING), ("created_at", DESCENDING)],
    name="reviews_movie_recent_index"
)
print("Created index: reviews_movie_recent_index (movie_id, created_at)")

try:
    db.reviews.create_index(
        [("user_id", ASCENDING), ("movie_id", ASCENDING)],
        unique=True,
        name="unique_user_movie_review"
    )
    print("Created unique index: unique_user_movie_review")
except OperationFailure as e:
    print("Could not create unique index 'unique_user_movie_review':", e)

print("All updated indexes created.")
