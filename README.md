Movie Streaming Platform — Backend (FastAPI + MongoDB)
Project Overview
This project implements the backend for a Movie Streaming Platform, designed and developed using FastAPI and MongoDB.
It supports movie storage, user management, reviews, watch history, and a hybrid search system that combines keyword, fuzzy, and popularity-based ranking.

MongoDB Schema Design
Collections:
movies,users,watch_history,reviews

MongoDB Relationships

One-to-many:
One movie → many reviews
One user → many watch history entries

Referenced relationships:
user_id and movie_id used in both reviews and watch_history.

Nested documents:
Genres and cast are nested inside movies.

Setup Instructions

Clone the repository

git clone https://github.com/abeeraamir2/movie-streaming-platform.git
cd movie-streaming-platform


Install dependencies
fastapi
uvicorn
pymongo
fuzzywuzzy
python-Levenshtein
numpy
scikit-learn
sentence-transformers


Run MongoDB locally
mongodb://localhost:27017/


Start FastAPI server
uvicorn main:app --reload


Access API Docs
http://127.0.0.1:8000/docs
