from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

import pandas as pd


def load_from_csv(
    file_path: str
) -> pd.DataFrame:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    return pd.read_csv(path)


def get_postgres_engine():

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    #connection_string = (
    #    f"postgresql+psycopg2://"
    #    f"{username}:{password}"
    #    f"@{host}:{port}/{database}"
    #)
    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=username,
        password=password,
        host=host,
        port=int(port),
        database=database,
    )
    #print('Connection string: ',connection_string)

    return create_engine(
        connection_url
    )


def load_from_postgres(
    query: str
) -> pd.DataFrame:

    engine = get_postgres_engine()

    with engine.connect() as connection:

        df = pd.read_sql(
            query,
            connection
        )

    return df
    
def load_data(
    source: str,
    csv_path: str | None = None,
    query: str | None = None
) -> pd.DataFrame:

    if source == "csv":

        if csv_path is None:
            raise ValueError(
                "csv_path is required "
                "when source='csv'"
            )

        return load_from_csv(
            csv_path
        )

    if source == "postgres":

        if query is None:
            raise ValueError(
                "query is required "
                "when source='postgres'"
            )

        return load_from_postgres(
            query
        )

    raise ValueError(
        f"Unsupported data source: {source}"
    )

