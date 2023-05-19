# tic tat toe

[swagger URL](http://localhost:8004/docs/)

## articles

* [Securing FastAPI with JWT Token-based Authentication on testdriven.io](https://testdriven.io/blog/fastapi-jwt-auth/)

## on deploy

* rename `.env_example` to `.env`
* in `.env` file edit `secret` field

## commands

    docker compose exec api alembic revision --autogenerate -m "init"

    docker compose exec api alembic upgrade head

## secret key generation example

    >>> import os
    >>> import binascii
    >>> binascii.hexlify(os.urandom(24))
    b'deff1952d59f883ece260e8683fed21ab0ad9a53323eca4f'
