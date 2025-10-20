from pymongo import MongoClient
from fuzzywuzzy import fuzz
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_streaming"]
movies_col = db["movies"]

movies = []
embeddings_list = []
ratings = []
popularities = []

embedder = SentenceTransformer('all-MiniLM-L6-v2')

for doc in movies_col.find({}, {"title": 1, "embedding": 1, "rating": 1, "popularity": 1, "_id": 0}):
    if "embedding" in doc and doc["embedding"] is not None:
        movies.append({
            "title": doc["title"],
            "rating": doc.get("rating", 0.0),
            "popularity": doc.get("popularity", 0)
        })
        embeddings_list.append(doc["embedding"])
        ratings.append(doc.get("rating", 0.0))
        popularities.append(doc.get("popularity", 0))


if not embeddings_list:
    raise ValueError("No embeddings found in database. Generate title embeddings first.")

embeddings = np.array(embeddings_list, dtype=np.float32)
ratings = np.array([m["rating"]["average"] if isinstance(m["rating"], dict) else m["rating"] for m in movies], dtype=np.float32)
popularities = np.array(popularities, dtype=np.float32)

def normalize(arr):
    if np.max(arr) == np.min(arr):
        return np.zeros_like(arr)
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

normalized_ratings = normalize(ratings)
normalized_popularity = normalize(popularities)


def semantic_search_title(user_query: str, top_n: int = 10):
    query_embedding = embedder.encode([user_query])
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_n]
    results = []
    for idx in top_indices:
        movie = movies[idx].copy()
        movie["similarity_score"] = float(similarities[idx])
        results.append(movie)
    return results


def hybrid_search_movies(query: str, top_n=10, w_sim=0.5, w_rating=0.3, w_pop=0.2):
    query_embedding = embedder.encode([query])
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    normalized_sim = normalize(similarities)
    final_scores = w_sim * normalized_sim + w_rating * normalized_ratings + w_pop * normalized_popularity
    top_indices = np.argsort(final_scores)[::-1][:top_n]
    top_movies = []
    for idx in top_indices:
        movie = movies[idx].copy()
        movie["similarity_score"] = float(similarities[idx])
        movie["final_score"] = float(final_scores[idx])
        top_movies.append(movie)
    return top_movies


def fuzzy_search_movies(title: str = None, director: str = None, cast: str = None, limit: int = 5):
    movies_db = list(movies_col.find({}))
    results = []

    for movie in movies_db:
        score = 0


        if title:
            score += fuzz.WRatio(title, movie.get("title", ""))

        if director:
            score += fuzz.WRatio(director, movie.get("director", ""))

        if cast:
            cast_list = movie.get("cast", [])
            if cast_list:
                max_cast_score = 0
                for member in cast_list:
                    member_score = fuzz.WRatio(cast, member)
                    if member_score > max_cast_score:
                        max_cast_score = member_score
                score += max_cast_score

        if score > 0:
            movie["_id"] = str(movie["_id"])
            results.append((movie, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results[:limit]]

