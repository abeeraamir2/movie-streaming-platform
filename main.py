from fastapi import FastAPI,Query,Body
from pymongo import MongoClient
from pydantic import BaseModel
from services.movieReviews import get_movie_reviews
from services.userHistory import get_user_history
from services.searches import fuzzy_search_movies,hybrid_search_movies,semantic_search_title
from services.top_movies import get_top_watched_movies
from services.addUser import create_user
from services.addWatchHistory import add_watch_history
from services.addReviews import add_review

app = FastAPI(title="Movie Streaming Platform API")

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_streaming"]

class UserCreate(BaseModel):
    name: str
    email: str
    subscription_type: str

class WatchHistoryCreate(BaseModel):
    movie_id: str
    duration: int

class ReviewCreate(BaseModel):
    movie_id: str
    rating: float
    text_review: str

@app.get("/movies/{movie_id}/reviews")
def movie_reviews(movie_id:str):
    return get_movie_reviews(movie_id)

@app.get("/users/{user_id}/history")
def user_history(user_id:str):
    return get_user_history(user_id)

@app.get("/movies/search")
def search_movies(
    title: str = Query(None, min_length=1),
    director: str = Query(None, min_length=1),
    cast: str = Query(None, min_length=1),
    limit: int = Query(5, ge=1)
):
    return fuzzy_search_movies(title, director, cast, limit)

@app.get("/movies/semantic_search")
def api_semantic_search(query: str = Query(...), top_n: int = 10):
    return {"query": query, "top_n": top_n, "results": semantic_search_title(query, top_n)}

@app.get("/movies/hybrid_search")
def api_hybrid_search(query: str = Query(...), top_n: int = 10):
    return {"query": query, "top_n": top_n, "results": hybrid_search_movies(query, top_n)}

@app.get("/movies/top_watched")
def top_watched_movies(limit: int = 5, days: int = 30):
    movies = get_top_watched_movies(limit=limit, days=days)
    return {"Top watched movies": movies}

@app.post("/users")
def add_user(user: UserCreate):
    user = create_user(
        user.name,
        user.email,
        user.subscription_type
    )
    return user

@app.post("/{user_id}/history")
def add_history(user_id: str, body: WatchHistoryCreate):
    return add_watch_history(user_id, body.movie_id, body.duration)

@app.post("/{user_id}/reviews")
def add_reviews(user_id: str, body: ReviewCreate):
    return add_review(user_id, body.movie_id, body.rating, body.text_review)