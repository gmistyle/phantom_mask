import sqlalchemy
from sqlalchemy import create_engine
from config import database as db_config


# engine instance
engine_url = sqlalchemy.engine.url.URL(
    drivername=db_config.DB_DRIVER,
    host=db_config.HOST,
    port=db_config.PORT,
    database=db_config.DATABASE,
    username=db_config.USER_NAME,
    password=db_config.PASSWORD
)

ENGINE = create_engine(engine_url)
