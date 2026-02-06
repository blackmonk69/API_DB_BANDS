from enum import Enum
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, field_validator, validator
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
class Album(BaseModel):
    title: str
    release_date: date

# 3. TERCERO: El modelo Padre (BandBase)
class BandBase(BaseModel):
    name: str
    genre: GenreURLChoices
    albums: List[Album] = [] # Aquí ya conoce qué es Album

#
class BandCreate(BandBase):
    @field_validator('genre', mode='before')
    def title_case_genre(cls, value):
        return value.title()

class BandWithID(BandBase):
    id: int

# 4. CUARTO: Forzar la reconstrucción de modelos
# Esto resuelve el error "not fully defined"
BandBase.model_rebuild()
BandWithID.model_rebuild()