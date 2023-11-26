from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, ValidationError


class Settings(BaseSettings):
    TOKEN: SecretStr
    TOKEN_KOSTYA: SecretStr
    DB_HOST: str
    DB_USER: str
    DB_PORT: int
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        # DSN
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


try:
    settings = Settings()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))
