from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

films = [
    {
        "id": 1,
        "title": "Liberty City",
        "director": "Niko Bellic",
        "year": 2009
    },
    {
        "id": 2,
        "title": "Captains Sea",
        "director": "Oliver M.",
        "year": 2011
    },
    {
        "id": 3,
        "title": "Show and rob",
        "director": "John Jackson",
        "year": 2001
    }
]


class Movie(BaseModel):
    id: int
    title: str
    director: str
    year: int

class CreateMovie(BaseModel):
    title: str = Field(min_length=2, max_length=50)
    director: str = Field(min_length=2, max_length=50)
    year: int = Field(ge=1900, le=2030)



@app.get("/movies", response_model=list[Movie])
def return_movies():
    return films

@app.get("/movies/{movie_id}", response_model=Movie, status_code=200)
def return_movie_by_id(movie_id: int):
    for movie in films:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(
        status_code=404,
        detail=f"Movie with id `{movie_id}` not found! "
    )

@app.post("/movies", response_model=Movie, status_code=201)
def create_movie(movie_name: CreateMovie):
    for saved_movie in films:
        if saved_movie["title"].lower() == movie_name.title.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Film with title `{saved_movie["title"]} already exists. `"
            )   
            
    new_movie = {
        "id": len(films) + 1,
        "title": movie_name.title,
        "director": movie_name.director,
        "year": movie_name.year
    }
    films.append(new_movie)
    return new_movie


