from logger import logger
from fastapi import APIRouter, Depends, status, Request, FastAPI
from sqlalchemy.orm import Session
import schema
from model import Note, User
from config import get_db

note_router = APIRouter()


@note_router.post('/create_note/', status_code=status.HTTP_201_CREATED)
def create_note(request: Request, note: schema.NoteSchema, db: Session = Depends(get_db)):
    try:
        data = note.dict()
        data.update({'user_id': request.state.user.id})
        note = Note(**data)
        db.add(note)
        db.commit()
        db.refresh(note)
        return {'message': 'note created', 'status': 201, 'data': note}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@note_router.put('/update_note/{note_id}', status_code=status.HTTP_200_OK)
def update_note(request: Request, note_id: int, data: schema.NoteSchema, db: Session = Depends(get_db)):
    try:
        data = data.dict()
        data.update({'user_id': request.state.user.id})
        note = db.query(Note).filter_by(id=note_id, user_id=request.state.user.id).one_or_none()
        if not note:
            raise Exception('note not found')
        [setattr(note, k, v) for k, v in data.items()]
        db.commit()
        db.refresh(note)
        return {'message': 'Note updated', 'status': 200, 'data': note}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@note_router.get('/get_user_notes/', status_code=status.HTTP_200_OK)
def get_user_notes(request: Request, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(id=request.state.user.id).first()
        if not user:
            return {'message': 'User not found', 'status': 400, 'data': {}}
        user.note.extend(user.note_m2m)
        print(user.note)
        data = [x.__dict__ for x in user.note]
        # return {'message': 'Notes retrieved', 'status': 200, 'data': data}
        return user.note
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@note_router.delete('/delete_note/{note_id}', status_code=status.HTTP_200_OK)
def delete_note(request: Request, note_id: int, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(id=note_id, user_id=request.state.user.id).one_or_none()
        if not note:
            return {'message': 'Note not found', 'status': 400, 'data': {}}
        db.delete(note)
        db.commit()
        return {'message': 'Note deleted', 'status': 200, 'data': {}}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@note_router.post('/collaborate/', status_code=status.HTTP_201_CREATED)
def add_collaborator(request: Request, data: schema.Collaborator, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter_by(id=data.note_id, user_id=request.state.user.id).one_or_none()
        if not note:
            raise Exception('note not found')
        collaborator = []
        for i in data.user_id:
            user = db.query(User).filter_by(id=i).one_or_none()
            if not user:
                raise Exception(f"user {i} not found")
            collaborator.append(user)
        note.user_m2m.extend(collaborator)
        print(note.user_m2m)
        db.commit()
        return {'message': 'Note collaborated', 'status': 201, 'data': {}}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@note_router.delete('/delete_collaborator/', status_code=status.HTTP_200_OK)
def delete_collaborator(request: Request, data: schema.DeleteCollaborator, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(id=data.user_id).first()
        if not user:
            raise Exception('user not found')
        note = db.query(Note).filter_by(id=data.note_id, user_id=request.state.user.id).one_or_none()
        if not note:
            raise Exception('note not found')
        if user in note.user_m2m:
            note.user_m2m.remove(user)
        db.commit()
        return {'message': 'Collaborator deleted', 'status': 200, 'data': {}}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}
