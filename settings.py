from pydantic_settings import BaseSettings


class Bot(BaseSettings):
    API_ID: str
    API_HASH: str
    GROUP_NAME: str
    TOKEN: str

    class Config:
        env_prefix = 'BOT_'
        env_file = '.env'
        extra = 'ignore'

class Settings:

    bot = Bot()

settings = Settings()
