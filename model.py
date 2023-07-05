from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from config import Base, engine


Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    password = Column(String)
    note = relationship('Note', back_populates='user')
    label = relationship('Label', back_populates='user')


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(200))
    color = Column(String(30))
    user_id = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='note')


class Label(Base):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    user_id = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='label')

