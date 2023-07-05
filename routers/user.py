from logger import logger
from fastapi import APIRouter, status, Depends, Response
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session
import schema
from config import get_db
from model import User
from utils import JWT

user_router = APIRouter()


@user_router.post('/register/', status_code=status.HTTP_201_CREATED)
def create_user(user: schema.User, db: Session = Depends(get_db)):
    try:
        data = user.dict()
        data['password'] = pbkdf2_sha256.hash(data['password'])
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        logger.exception(e.args[0])
        return {"message": 'User registered successfully', 'Status': 201, 'data': user}


@user_router.post('/login/', status_code=status.HTTP_200_OK)
def login_user(user_login: schema.UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(username=user_login.username).first()
        if user and pbkdf2_sha256.verify(user_login.password, user.password):
            token = JWT.jwt_encode({'user': user.id})
            return {"message": 'Logged in successfully', 'status': 200, 'access_token': token}
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": 'Invalid username or password', 'status': 400, 'data': {}}
    except Exception as e:
        logger.exception(e.args[0])
        response.status_code = 400
        return {"message": e.args[0], 'status': 400, 'data': {}}

