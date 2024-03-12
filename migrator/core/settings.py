import typing
import logging.config
import sqlalchemy as sa
import os
# import boto3
from core.connections import PostgresConnection
from functools import partial
from dotenv import load_dotenv
# from plantscore.queue import SQSJobQueue

# try:
#     from mypy_boto3_sqs import SQSClient
# except ImportError:
#     SQSClient = typing.NewType("SQSClient", typing.Any)

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


# sqs_client = boto3.resource("sqs", **(dict(region_name=region) if region else dict()))

# def get_sqs_client() -> SQSClient:
#     if not sqs_client:
#         raise Exception("SQS client not defined")
#     return sqs_client


# SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", None)


# SELECT SOURCE AND DESTINATION DATABASE
PostgresDatabase = partial(PostgresConnection, get_database_engine=get_sql_engine)
# JobQueue = SQSJobQueue(get_sqs_client, queue_name=SQS_QUEUE_NAME)
