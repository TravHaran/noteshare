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

    class Config:
        env_file = "/Users/travisratnaharan/Documents/Work/noteshare/backend/.env"

settings = Settings()