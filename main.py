from fastapi import FastAPI, Path, Query, HTTPException
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()


class JuegoBase(BaseModel):
    id: Annotated[int, Field(gt=0)]
    titulo: Annotated[str, Field(min_length=3, max_length=35, examples=["WOW"])]
    genero: Annotated[str, Field(min_length=3, max_length=35, examples=["MMORPG"])]
    score: Annotated[int, Field(gt=0, le=100)]


class JuegoFiltrado(BaseModel):
    titulo: Annotated[str, Field(min_length=3, max_length=35, examples=["WOW"])]
    genero: Annotated[str, Field(min_length=3, max_length=35, examples=["MMORPG"])]
    score: Annotated[int, Field(gt=0, le=100)]


list_games = [
    {"id": 1, "titulo": "Minecraft", "genero": "survival", "score": 1},
    {"id": 2, "titulo": "Need For Speed - Underground", "genero": "race", "score": 1},
    {"id": 3, "titulo": "Watch_dog", "genero": "open word", "score": 1},
]


# -------------------------------------------------------------------------------------
@app.get(
    "/juegos",
    tags=["Lista de juegos"],
    response_model=list[JuegoBase],
    responses={
        404: {
            "description": "juego no encontrado",
            "content": {
                "application/json": {"example": {"detail": "juego no encontrado"}}
            },
        }
    },
)
def obtener_juego() -> list[JuegoBase]:
    if list_games:
        return list_games

    raise HTTPException(status_code=404, detail="juego no encontrado")


# -------------------------------------------------------------------------------------
@app.get(
    "/juegos/{id}",
    tags=["Filtros por id"],
    response_model=JuegoFiltrado,
    responses={
        404: {
            "description": "juego no encontrado",
            "content": {
                "application/json": {"example": {"detail": "juego no encontrado"}}
            },
        }
    },
)
def filtrar_juego(
    id: Annotated[int, Path(gt=0, description="id del juego a filtrar")],
) -> JuegoFiltrado:
    print(id)
    for j in list_games:
        if j["id"] == id:
            return j

    raise HTTPException(status_code=404, detail="juego no encontrado")


# -------------------------------------------------------------------------------------
@app.post("/agregar-juego", tags=["Agregar juego"], response_model=list[JuegoBase])
def agregar_juego(juego: JuegoBase) -> list[JuegoBase]:
    list_games.append(juego.model_dump())
    return list_games


# -------------------------------------------------------------------------------------
@app.put(
    "/editar-juego/{id}",
    tags=["Editor de juegos"],
    responses={
        404: {
            "description": "Juego no encontrado",
            "content": {
                "aplication/json": {"example": {"detail": "juego no encontrado"}}
            },
        }
    },
)
def aditar_juego(
    id: Annotated[int, Path(gt=0, description="id del juego a eliminar")],
    juego: JuegoFiltrado,
) -> JuegoFiltrado:
    for j in list_games:
        if j["id"] == id:
            j["titulo"] = juego.titulo
            j["genero"] = juego.genero
            j["score"] = juego.score
            return juego
    raise HTTPException(status_code=404, detail="Juego no encontrado")


# -------------------------------------------------------------------------------------
@app.delete(
    "/borrar-juego/{id}",
    tags=["Eliminar juego"],
    response_model=list[JuegoBase],
    responses={
        404: {
            "description": "Juego no encontrado",
            "content": {
                "aplication/json": {"example": {"detail": "juego no encontrado"}}
            },
        }
    },
)
def borrar_juego(
    id: Annotated[int, Path(gt=0, description="id del juego a borrar")],
) -> list[JuegoBase]:
    for juego in list_games:
        if juego["id"] == id:
            list_games.remove(juego)
            return list_games
    raise HTTPException(status_code=404, detail="Juego no encontrado")
