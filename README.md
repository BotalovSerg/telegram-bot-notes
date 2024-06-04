# telegram-bot-notes

```
docker compose up -d 
```
or only db
```commandline
docker compose up -d db
```
```commandline
alembic init --template async bot/db/migrations
```
```commandline
alembic revision --autogenerate -m "init"
```
```commandline
alembic upgrade head
```
run container db postgres without docker compose 
```commandline
docker run --rm -e POSTGRES_DB=bot_db -e POSTGRES_PASSWORD=botalov -e POSTGRES_USER=botalov -p 5433:5432 --name postgres_bot -d postgres
```