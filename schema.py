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


class Collaborator(BaseModel):
    note_id: int
    user_id: Optional[List[int]]


class DeleteCollaborator(BaseModel):
    note_id: int
    user_id: int
