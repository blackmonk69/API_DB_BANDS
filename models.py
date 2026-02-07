from enum import Enum
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, field_validator
from sqlmodel import SQLModel,Field, true,Relationship
from fastapi import FastAPI

app = FastAPI()

# 1. Primero los Enums
class GenreURLChoices(str, Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'

# 2. SEGUNDO: El modelo que va DENTRO de otros (Album)
# Debe estar definido antes de que BandBase lo mencione
class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id:int=Field(foreign_key="band.id")

class Album(AlbumBase, table=True):
    id:int=Field(default=None,primary_key=True)
    band:Band=Relationship(back_populates="albums")
    
# 3. TERCERO: El modelo Padre (BandBase)
class BandBase(SQLModel):
    name: str
    genre: GenreURLChoices
    

#
class BandCreate(BandBase):
    albums: List[AlbumBase]|None=None  # Aquí ya conoce qué es Album
    @field_validator('genre', mode='before')
    def title_case_genre(cls, value):
        return value.title()

class Band(BandBase,table=True):
    id: int=Field(default=None,primary_key=true)
    albums:list[Album]=Relationship(back_populates="band")
# 4. CUARTO: Forzar la reconstrucción de modelos
# Esto resuelve el error "not fully defined"
BandBase.model_rebuild()
Band.model_rebuild()