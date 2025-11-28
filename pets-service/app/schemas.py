from pydantic import BaseModel

class PetBase(BaseModel):
    name: str
    species: str
    breed: str
    owner_name: str
    owner_id: int

class PetResponse(PetBase):
    id: int
    class Config:
        from_attributes = True
