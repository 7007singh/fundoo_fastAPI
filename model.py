from sqlalchemy import Column, String, Integer
from config import Base, engine
from passlib.hash import pbkdf2_sha256

Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    password = Column(String)

    def verify_password(self, password: str):
        return pbkdf2_sha256.verify(password, self.password_hash)


