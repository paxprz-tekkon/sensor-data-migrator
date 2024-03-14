import typing
import boto3
import logging.config
import sqlalchemy as sa
import os

# import boto3
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
from core.connections import PostgresConnection
from functools import partial
from dotenv import load_dotenv

load_dotenv()

# LOG CONFIG
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            # 'level': 'WARNING',
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOG_CONFIG)

# SQL DATABASE
DATABASE_URI = os.environ.get(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
engine = None
if DATABASE_URI:
    engine = sa.create_engine(DATABASE_URI, pool_size=4)


def get_sql_engine():
    if not engine:
        raise Exception("Database engine not defined")
    return engine


DYNAMODB_SENSOR_DATA_TABLE = "Sensor-Data-Archive"
DYNAMODB_DAILY_SENSOR_DATA_TABLE = "Daily-Sensor-Data-Archive"
DYNAMODB_PLANT_SCORE_TABLE = "Plant-Score-Archive"
DYNAMODB_PLANT_TEMPERATURE_SCORE_TABLE = "Plant-Temperature-Score-Archive"
DYNAMODB_PLANT_HUMIDITY_SCORE_TABLE = "Plant-Humidity-Score-Archive"
DYNAMODB_PLANT_MOISTURE_SCORE_TABLE = "Plant-Moisture-Score-Archive"
DYNAMODB_PLANT_LIGHT_SCORE_TABLE = "Plant-Light-Score-Archive"


config = {}

if region := os.getenv("X_AWS_REGION"):
    config["region_name"] = region

if access_key := os.getenv("X_AWS_ACCESS_KEY_ID"):
    config["aws_access_key_id"] = access_key

if secret_key := os.getenv("X_AWS_SECRET_ACCESS_KEY"):
    config["aws_secret_access_key"] = secret_key


dynamodb_resource: DynamoDBServiceResource = boto3.resource("dynamodb", **config)

# SELECT SOURCE AND DESTINATION DATABASE
PostgresDatabase = partial(PostgresConnection, get_database_engine=get_sql_engine)
