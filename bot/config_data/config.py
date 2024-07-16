from pydantic import BaseModel
from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    url: PostgresDsn


class BotConfig(BaseModel):
    token: str

class RedisConfig(BaseModel):
    dsn: RedisDsn

class AdminConfig(BaseModel):
    ids_list: list = [454793877]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="_",
        env_prefix="APP_",
    )
    bot: BotConfig
    db: DatabaseConfig
    redis: RedisConfig
    admins: AdminConfig = AdminConfig()

settings = Settings()
