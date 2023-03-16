swagger URL:
http://localhost:8004/docs#/


commands:
    docker compose exec web alembic revision --autogenerate -m "init"
    docker compose exec web alembic upgrade head
