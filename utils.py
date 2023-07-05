from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import APIKeyHeader
from fastapi import Security, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from config import get_db
from model import User


class JWT:
    @staticmethod
    def jwt_encode(payload: dict):
        if 'exp' not in payload:
            payload.update(exp=datetime.utcnow() + timedelta(hours=1), iat=datetime.utcnow())
        return jwt.encode(payload, 'key', algorithm="HS256")

    @staticmethod
    def jwt_decode(token):
        try:
            return jwt.decode(token, 'key', algorithms=['HS256'])
        except jwt.JWTError as e:
            raise e


api_key = APIKeyHeader(name='Authorization')


def jwt_authorization(request: Request, token: str = Security(api_key), db: Session = Depends(get_db)):
    decode_token = JWT.jwt_decode(token)
    user_id = decode_token.get('user')
    user = db.query(User).filter_by(id=user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail='User not authorized')
    request.state.user = user


