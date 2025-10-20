# Movie Streaming Platform — Backend (FastAPI + MongoDB)

## Overview
This project implements the backend system for a Movie Streaming Platform using *FastAPI* and *MongoDB*.
It provides features such as movie storage, user management, reviews, watch history, and a hybrid search mechanism that integrates keyword-based, fuzzy, and popularity-based ranking.


## Tech Stack

| Component         | Technology                                                                 |
| ----------------- | -------------------------------------------------------------------------- |
| Backend Framework | FastAPI                                                                    |
| Database          | MongoDB                                                                    |
| ORM / Driver      | PyMongo                                                                    |
| Libraries         | fuzzywuzzy, python-Levenshtein, NumPy, scikit-learn, sentence-transformers |
| Server            | Uvicorn                                                                    |
| Language          | Python                                                                     |
| API Documentation | Swagger UI (FastAPI Docs)                                                  |

## Database Schema Design

### Collections

* *movies* — Stores movie details such as title,director,genres, cast,popularity and ratings
* *users* — Stores user information
* *watch_history* — Logs user watch activity
* *reviews* — Stores user reviews and ratings for movies

### Relationships

* *One-to-Many*
  * One movie → many reviews
  * One user → many watch history entries
   
* *Referenced Fields*
  * user_id and movie_id are used as references in both reviews and watch_history
    
* *Nested Documents*
  * Movie genres and cast are stored as nested arrays within the movies collection


## Features
* *Movie Storage:* Add, update, and delete movie records
* *Reviews:* Submit and fetch user reviews for each movie
* *Watch History:* Track movies watched by users
* *Search:* Full-text search with typo tolerance
* *Hybrid Search System:* Hybrid search base on similarity,popularity and rating
* *User Management:* Create user profiles
* *Top Watched movies:* Fetch top 5 most-watched movies


## Setup Instructions

1. *Clone the Repository*
   git clone https://github.com/abeeraamir2/movie-streaming-platform.git
   cd movie-streaming-platform
   

2. *Install Dependencies*
   pip install fastapi uvicorn pymongo fuzzywuzzy python-Levenshtein numpy scikit-learn sentence-transformers
   
3. *Run MongoDB Locally*
   mongodb://localhost:27017/
   

4. *Start the FastAPI Server*
   uvicorn main:app --reload
   

5. *Access the API Documentation*

   http://127.0.0.1:8000/docs
   


