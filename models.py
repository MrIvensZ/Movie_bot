"""
Модели данных для базы данных фильмов.
Содержит определения всех таблиц.
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# класс для данных всех таблиц
class Base(DeclarativeBase):
    pass


# описываем таблицу с фильмами
class MoviesORM(Base):
    __tablename__ = 'movies_orm'
    title: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True
        )
    search_date: Mapped[str]
