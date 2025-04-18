import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise EnvironmentError(f"Environment variable '{name}' is not set.")
    return value