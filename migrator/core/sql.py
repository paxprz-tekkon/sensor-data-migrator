import sqlalchemy as sa
from core.protocols import DbConnection


SQL_METADATA = sa.MetaData()


def get_metadata(schema=None):
    if schema is not None:
        return sa.MetaData(schema=schema)
    return SQL_METADATA


def reflect_table(
    table_name: str,
    conn: DbConnection,
    schema: str = "public",
    metadata: sa.MetaData = sa.MetaData(),
) -> sa.Table:
    engine = sa.create_engine(str(conn.url))
    return sa.Table(
        table_name,
        metadata,
        autoload=True,
        schema=schema,
        autoload_with=engine,
    )
