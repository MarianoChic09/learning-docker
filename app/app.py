from fastapi import FastAPI,Body,Path,Query
from fastapi.responses import HTMLResponse 
from pydantic import BaseModel,Field
from typing import Optional

app = FastAPI() # Create an instance of FastAPI
app.title = "My First FastAPI Application"
app.version = "0.0.1"

@app.get("/",tags = ["hello_world"]) # Decorator to tell FastAPI which path to handle
def message():
    return "Hello World!"

# Metodo get

@app.get("/hello_json",tags = ["hello_world"])
def message2():
    return {"message": "Hello World!"}

@app.get("/hello_html",tags = ["hello_world"])
def message3():
    return HTMLResponse('<h1>Hello World!</h1>')

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get("/movies",tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}',tags=['movies'])
def get_movie(id: int):
    for item in movies:
        if item['id'] == id:
            return item
    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str,year: int):
    return [item for item in movies if item['category'] == category and item['year'] == year]

@app.post('/movies',tags=['movies'])
def create_movie(id:int = Body(),title:str= Body(),overview:str= Body(),year:int= Body(),rating:float= Body(),category:str= Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return title
    
@app.put('/movies/{id}',tags=['movies'])
def update_movie(id:int,title:str= Body(),overview:str= Body(),year:int= Body(),rating:float= Body(),category:str= Body()):
    for item in movies:
        if item['id'] == id:
            item['title'] = title
            item['overview'] = overview
            item['year'] = year
            item['rating'] = rating
            item['category'] = category
            return movies
    return []

@app.delete('/movies/{id}',tags=['movies'])
def delete_movie(id:int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies
    return []


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15) # Field is used to add validation to the model fields. Max length is used to limit the length of the string
    overview: str = Field(min_length=15,max_length=100)
    year: int = Field(ge=2000,le=2022) # ge and le are used to set the range of the integer
    rating: float = Field(ge=1,le=10)
    category: str = Field(min_length=3,max_length=15)
    
    class Config:
        schema_extra = {
            "example":{
                "id": 1,
                "title": "Mi Pelicula",
                "overview": " Descripcion de la pelicula",
                "year": "2022",
                "rating": 9.8,
                "category": "Acción"
            }
        }
 
@app.post('/movies2',tags=['movies'])
def create_movie2(movie: Movie):
    movies.append(movie)
    return movies

@app.put('/movies2',tags=['movies'])
def update_movie2(id:int, movie: Movie):
   for item in movies:
       if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies
# uvicorn app:app --reload --port 5000 --host 0.0.0.0 
# to run the application on port 5000 and to use the host (if i point to the IP of the code I can access this)

