from pydantic import BaseModel

class PetBase(BaseModel):
    name: str
    species: str
    breed: str
    owner_name: str

class PetResponse(PetBase):
    id: int
    class Config:
        orm_mode = True
