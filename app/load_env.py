import os
from typing import Optional
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()


def get_env_var(
    name: str, default: str | None = None, required: bool = True
) -> Optional[str]:
    value = os.getenv(name, default)
    if required and (value is None or value.strip() == ""):
        raise EnvironmentError(
            f"Required environment variable '{name}' was not defined."
        )
    return value


# Função para gerar o DSN do banco de dados
def get_database_dsn() -> str:
    user = get_env_var("DB_USER", default="postgres")
    password = get_env_var("DB_PASSWORD", default="postgres")
    name = get_env_var("DB_NAME", default="mugen")
    host = get_env_var("DB_HOST", default="localhost")
    port = get_env_var("DB_PORT", default="5432")

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"
