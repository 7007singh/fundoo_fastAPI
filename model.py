from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped
from config import Base, engine


Base.metadata.create_all(engine)


collaborator = Table(
    'collaborator',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('note_id', ForeignKey('notes.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    password = Column(String)
    note = relationship('Note', back_populates='user')
    label = relationship('Label', back_populates='user')
    note_m2m = relationship('Note', secondary=collaborator, back_populates='user_m2m')


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(200))
    color = Column(String(30))
    user_id = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='note')
    user_m2m = relationship('User', secondary=collaborator, back_populates='note_m2m')


class Label(Base):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    user_id = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='label')
