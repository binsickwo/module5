from enum import Enum

from pydantic import BaseModel, Field, field_validator
from typing import Optional
import datetime
import re
from typing import List
from pydantic import BaseModel, Field, field_validator

from constants.roles import Roles


class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен вполностью совпадать с полем password")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        # Проверяем, совпадение паролей
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    # Добавляем кастомный JSON-сериализатор для Enum
    class Config:
        json_encoders = {
            Roles: lambda v: v.value  # Преобразуем Enum в строку
        }

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: Optional[bool] = None
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value
##################################################

class LocationEnum(str, Enum):
    MSK = "MSK"
    SPB = "SPB"


class GenreResponse(BaseModel):
    id: Optional[int] = None
    name: str


class MovieReviewResponse(BaseModel):
    userId: str
    rating: float = Field(ge=0, le=10)
    text: str
    createdAt: str
    user: dict  # {"fullName": "..."}


class MovieResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str
    imageUrl: Optional[str] = None
    location: LocationEnum
    published: bool
    genreId: int
    genre: GenreResponse
    createdAt: str
    rating: float = Field(ge=0, le=10)

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        datetime.datetime.fromisoformat(value)
        return value


class FindOneMovieResponse(MovieResponse):
    
    reviews: List[MovieReviewResponse]


class FindAllMoviesResponse(BaseModel):
    movies: List[MovieResponse]
    count: int
    page: int
    pageSize: int
    pageCount: int