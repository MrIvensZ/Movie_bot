"""
Модели данных для базы данных фильмов.
Содержит определения всех таблиц и metadata.
"""

from sqlalchemy import Table, Column, String, MetaData

# Метаданные для всех таблиц
metadata = MetaData()

# описываем таблицу с фильмами
movies = Table(
    'movies',
    metadata,
    # title - первичный ключ (уникальный идентификатор)
    Column('title', String, primary_key=True, nullable=False),
    # search_date - дата просмотра
    Column('search_date', String, nullable=False)
)
