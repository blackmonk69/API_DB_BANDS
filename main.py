from typing import Annotated, Optional, List
from fastapi import FastAPI, HTTPException,Path,Query,Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
import os

from enum import Enum
from fastapi import FastAPI
from models import GenreURLChoices,BandCreate,Band,Album
from db import init_db,get_session



app = FastAPI()

# # --- ENDPOINTS ---

# Listar bandas con filtros de Género y Álbumes (Imagen 7, 11)
@app.get('/bands')
async def bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str|None,Query (max_length=10)]=None,session: Session = Depends(get_session)) -> list[Band]: #the annotation agrega metadata que se puede usar
    band_list=session.exec(select(Band)).all()
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
async def band(band_id: Annotated [int, Path (title="The Band ID")],session: Session = Depends(get_session)) -> Band:
     band=session.get(Band,band_id)  #trae de la entidad banda con ese primary key  
     if band is None:
         # Manejo de error 404
         raise HTTPException(status_code=404, detail='Band not found')
     return band

# @app.get('/bands/genre/{genre}')
# async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
#     print("entra")
#     return [
#         b for b in BANDS if b['genre'].lower() == genre.value
#     ]
    
    
@app.post("/bands")
async def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session)
) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)
    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(
            title=album.title, release_date=album.release_date, band=band
        )
        session.add(album_obj)
    session.commit()
    session.refresh(band)
    return band

