from typing import Annotated, Optional, List
from fastapi import FastAPI, HTTPException, Path, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
import os
from contextlib import asynccontextmanager
from enum import Enum
from fastapi import FastAPI
from schemas import GenreURLChoices,BandCreate,BandWithID

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'electronic'},
    {'id': 3, 'name': 'Slowdive', 'genre': 'metal'},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'hip-hop','albums':[{'title':'Titulo del album','release_date':'1971-07-21'}]},
]


# --- ENDPOINTS ---

# Listar bandas con filtros de Género y Álbumes (Imagen 7, 11)
@app.get('/bands')
async def bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str|None,Query (max_length=10)]=None) -> list[BandWithID]:
    #print("entra")
    band_list = [BandWithID(**b) for b in BANDS]

    if genre:
        band_list = [
            b for b in band_list if b.genre.lower() == genre.value
        ]
        #print ("entra2")
   #filtramos las bandas
    if q:
       band_list=[b for b in band_list if q.lower() in b.name.lower()]
    return band_list

@app.get('/bands/{band_id}')
async def band(band_id: Annotated [int, Path (title="The Band ID")]) -> BandWithID:
    band = next((BandWithID(**b) for b in BANDS if b['id'] == band_id), None)
    if band is None:
        # Manejo de error 404
        raise HTTPException(status_code=404, detail='Band not found')
    return band

@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
    print("entra")
    return [
        b for b in BANDS if b['genre'].lower() == genre.value
    ]
    
    
@app.post('/bands')
async def create_band(band_data: BandCreate) -> BandWithID:
    # Generamos un nuevo ID basado en el último elemento
    new_id = BANDS[-1]['id'] + 1 if BANDS else 1
    
    # Creamos el nuevo objeto combinando el ID y los datos validados
    # model_dump() convierte el modelo de Pydantic en un diccionario
    new_band = BandWithID(id=new_id, **band_data.model_dump())
    
    # Guardamos en nuestra "BD" (convertimos a dict para mantener consistencia)
    BANDS.append(new_band.model_dump())
    
    return new_band