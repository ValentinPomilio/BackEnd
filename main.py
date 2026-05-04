from fastapi import FastAPI
from typing import Optional

app = FastAPI()
app.title = "Práctico 1 - BackEnd"

juegos = [
    {"id": 1, "titulo": "Counter Strike 2", "genero": "FPS"},
    {"id": 2, "titulo": "Rocket League", "genero": "Deportes"},
    {"id": 3, "titulo": "WRC", "genero": "Carreras"}
]

@app.get("/juegos", tags=["juegos"])
def mostrar_juegos():
    return juegos

@app.get("/juego/{id}", tags=["juegos"])
def filtrar_juego(id : int):
    for juego in juegos:
        if juego["id"] == id:
            return juego
    return {"msg": "Algo no salio pibe"}

@app.post("/agregar-juego", tags=["juegos"])
def agregar_juego(id: int, titulo: str, genero: str):
    juegos.append({"id": id, "titulo": titulo, "genero": genero})
    return juegos

@app.put("/editar-juego", tags=["juegos"])
def aditar_juego(id: int, titulo:Optional[str] = None, genero: Optional[str] = None):
    for juego in juegos:
        if juego["id"] == id:
            juego["titulo"] = titulo if titulo else juego["titulo"]
            juego["genero"] = genero if genero else juego["genero"]
            return juego
    return "Algo no salio bien pibe"

@app.delete("/borrar-juego/{id}", tags=["juegos"])
def borrar_juego(id:int):
    for juego in juegos:
        if juego["id"] == id:
            juegos.remove(juego)
            return juego
    return "Algo no salio bien pibe"