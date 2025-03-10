# MovieBot
## Описание проекта
Telegram бот, который запоминает просмотренные фильмы. В его базу данных заносятся название фильма и дата просмотра. Имеется возможность удаления и обновления записей в базе данных.
## Локальный запуск проекта
#### Клонируйте репозиторий
```
git@github.com:NikitaProkhvatilov/Movie_bot.git
```
#### Перейдите в директорию Movie_bot
```
cd Movie_bot
```
#### Cоздайте и активируйте виртуальное окружение:
```
python -m venv venv
```
```
source venv/bin/activate
```
#### Установите зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

В той же директории создайте .env файл и наполните его своими данными:
```
TOKEN               - токен вашего бота
```
### Начало работы
1. Запустите файл __movie_bot.py__
2. В Telegram чате для активации бота напишите команду `/start`
3. На появившейся клавиатуре выберите нужное вам действие и следуйте дальнейшим инструкциям бота
##### Перечень действий
```
/добавить        - добавить новый фильм в БД
/удалить         - удалить фильм из БД
/обновить        - обновить запись о фильме (название или дату просмотра)
/поиск           - поиск названия фильма по дате просмотра или даты по названию
```


### Технологии
_Используемые технологии_: __Python 3__, __pyTelegramBotAPI__, __SQLite__

### Автор
_Никита Прохватилов_