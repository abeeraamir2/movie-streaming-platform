from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_streaming"]
movies_col = db["movies"]

movies = []
embeddings_list = []
ratings = []
popularities = []

embedder = SentenceTransformer('all-MiniLM-L6-v2')

for movie in movies_col.find():
    title = movie["title"]

    embedding = embedder.encode(title).tolist()

    movies_col.update_one(
        {"_id": movie["_id"]},
        {"$set": {"embedding": embedding}}
    )
    print(f"Added embedding for: {title}")