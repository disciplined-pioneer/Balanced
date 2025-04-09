from pydantic_settings import BaseSettings


class Bot(BaseSettings):
    
    TOKEN: str
    GROUP_NAME: str
    SHEETS_NAME: str

    class Config:
        env_prefix = 'BOT_'
        env_file = '.env'
        extra = 'ignore'

class Settings:

    bot = Bot()

settings = Settings()
