# user.py
from sqlalchemy import Column, String, Boolean, DateTime, ARRAY, Enum as SAEnum,INTEGER,Float
from sqlalchemy.orm import declarative_base
from typing import Dict, Any
from constants.roles import Roles

Base = declarative_base()

class MovieDBModel(Base):
    __tablename__ = "movies"
    id = Column(INTEGER, primary_key=True, autoincrement=True)  # text в БД
    name = Column(String)
    price = Column(INTEGER)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    rating = Column(Float)
    genre_id = Column(INTEGER)
    created_at = Column(DateTime)

    def to_dict(self) -> Dict[str, Any]:
        return{
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image_url": self.image_url,
            "location": self.location,
            "published": self.published,
            "rating": self.rating,
            "genre_id": self.genre_id,
            "created_at": self.created_at
        }

    def __repr__(self) -> str:
        return f"<Movie id={self.id} name={self.name}>"