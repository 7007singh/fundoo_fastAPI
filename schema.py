from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class NoteSchema(BaseModel):
    title: str
    description: str
    color: str

    class Config:
        orm_mode = True


class LabelSchema(BaseModel):
    name: str


class LabelAssociation(BaseModel):
    note_id: int
    label_id: Optional[List[int]]
