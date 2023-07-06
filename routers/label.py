from fastapi import APIRouter, Depends, status, Request
from logger import logger
from sqlalchemy.orm import Session
import schema
from config import get_db
from model import Label, User, Note

label_router = APIRouter()


@label_router.post('/add_label/', status_code=status.HTTP_201_CREATED)
def create_label(request: Request, label: schema.LabelSchema, db: Session = Depends(get_db)):
    try:
        data = label.dict()
        data.update({'user_id': request.state.user.id})
        label = Label(**data)
        db.add(label)
        db.commit()
        db.refresh(label)
        return {'message': 'label added', 'status': 201, 'data': label}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@label_router.get('get_label', status_code=status.HTTP_200_OK)
def get_label(request: Request):
    try:
        return {'message': 'labeled notes', 'status': 200, 'data': request.state.user.label}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@label_router.put('update_label', status_code=status.HTTP_200_OK)
def update_label(request: Request, label_id: int, data: schema.LabelSchema, db: Session = Depends(get_db)):
    try:
        data = data.dict()
        data.update({'user_id': request.state.user.id})
        label = db.query(Label).filter_by(id=label_id, user_id=request.state.user.id).one_or_none()
        if not label:
            raise Exception('user not found')
        [setattr(label, k, v) for k, v in data.items()]
        db.commit()
        db.refresh(label)
        return {'message': 'label updated', 'status': 200, 'data': label}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


@label_router.delete('delete_label', status_code=status.HTTP_200_OK)
def delete_label(request: Request, label_id: int, db: Session = Depends(get_db)):
    try:
        label = db.query(Label).filter_by(id=label_id, user_id=request.state.user.id).one_or_none()
        if not label:
            return {'message': 'label not found', 'status': 400, 'data': {}}
        db.delete(label)
        db.commit()
        return {'message': 'label deleted successfully', 'status': 200, 'data': {}}
    except Exception as e:
        logger.exception(e.args[0])
        return {'message': e.args[0], 'status': 400, 'data': {}}


# @label_router.post('/add_label/{note_id}', status_code=status.HTTP_201_CREATED)
# def add_label(request: Request, note_id: int, label: schema.LabelSchema, db: Session = Depends(get_db)):
#     try:
#         note = db.query(Note).filter_by(id=note_id).one_or_none()
#         if not note:
#             return {'message': 'Note not found', 'status': 400, 'data': {}}
#         label_obj = db.query(Label).filter_by(user_id=request.state.user.id)
#         # if not label_obj:
#         #     label_obj = Label(name=label.name, user_id=request.state.user.id)
#         #     db.add(label_obj)
#         #     db.commit()
#         note.label.append(label_obj)
#         db.commit()
#         return {'message': 'Label added to note', 'status': 201, 'data': {}}
#     except Exception as e:
#         logger.exception(e.args[0])
#         return {'message': e.args[0], 'status': 400, 'data': {}}
