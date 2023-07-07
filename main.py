from fastapi import FastAPI, Depends
from routers import user, note, label
from utils import jwt_authorization


user_app = FastAPI(debug=True, title='User APIs')
note_app = FastAPI(debug=True, title='Note APIs')
label_app = FastAPI(debug=True, title='Label APIs')
user_app.include_router(user.user_router, prefix='/user', tags=['User'])
note_app.include_router(note.note_router, prefix='/note', dependencies=[Depends(jwt_authorization)], tags=['Note'])
label_app.include_router(label.label_router, prefix='/label', dependencies=[Depends(jwt_authorization)], tags=['Label'])
