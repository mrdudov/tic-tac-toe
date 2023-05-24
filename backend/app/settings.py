from pydantic import BaseSettings


class Settings(BaseSettings):
    authjwt_secret_key: str
    authjwt_access_token_expires: int
    max_online_users: int

    class Config:
        env_file = ".env"


SETTINGS = Settings()
