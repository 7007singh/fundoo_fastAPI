from fastapi import FastAPI, Depends
from routers import user, note, label
from utils import jwt_authorization


app = FastAPI(debug=True)
app.include_router(user.user_router, prefix='/user', tags=['user'])
app.include_router(note.note_router, prefix='/note', dependencies=[Depends(jwt_authorization)], tags=['note'])
app.include_router(label.label_router, prefix='/label', dependencies=[Depends(jwt_authorization)], tags=['label'])
