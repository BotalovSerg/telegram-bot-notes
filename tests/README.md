
Создание конфигурации alembic в директории для тестов
```commandline
cd tests/
alembic init --template async migrations
```
Настройка tests/migrations/env.py
```
import os
from dotenv import load_dotenv
from pathlib import Path

from bot.db.models import Base

target_metadata = Base.metadata

project_dir = Path(__file__).parent.parent
path_conf = Path.joinpath(project_dir.absolute(), ".env.test").as_posix()
load_dotenv(dotenv_path=path_conf)

config.set_main_option(
    'sqlalchemy.url',
    str(os.getenv('APP_DB_URL_TEST')),
)

```
Тестовая база данных в докере
```commandline
docker run --rm -e POSTGRES_DB=bot_db -e POSTGRES_PASSWORD=botalov -e POSTGRES_USER=botalov -p 5433:5432 --name postgres_bot -d postgres
```
