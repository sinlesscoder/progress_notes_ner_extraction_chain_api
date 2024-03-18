from json import load
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# Load env vars
def load_env_vars(file_path: str):
    with open(file_path, "r") as buffer:
        vars = load(buffer)
    
    environ.update(vars)

    vars.clear()

def postgres_engine(file_path: str) -> Engine:
    # Load env vars
    load_env_vars(file_path=file_path)

    # Get credentials
    host = environ['POSTGRES_HOST']
    user = environ['POSTGRES_USER']
    password = environ['POSTGRES_PASSWORD']
    port = environ['POSTGRES_PORT']
    database = environ['POSTGRES_DATABASE']

    uri = f'postgresql://{user}:{password}@{host}:{port}/{database}'

    engine = create_engine(uri)

    return engine
