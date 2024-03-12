import logging
from readline import insert_text
import typing
import sqlalchemy as sa
from datetime import date
import pandas as pd
from sqlalchemy.dialects import postgresql
from migrator.adapters import orm as o

from core.protocols import DbConnection


LOGGER = logging.getLogger(__name__)
