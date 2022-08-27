from pydantic import BaseSettings

class Settings(BaseSettings):
    database_name: str
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    file_dir: str
    waiting_room_file_dir: str
    thumbnail_dir: str
    banner_dir: str
    default_banner: str

    class Config:
        env_file = "/Users/trav/Desktop/noteshare/backend/.env"

settings = Settings()