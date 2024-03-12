import sqlalchemy as sa
from core.sql import SQL_METADATA


sensor_table = sa.Table(
    "device_sensor",
    SQL_METADATA,
    sa.Column("id", sa.BigInteger()),
    sa.Column("sensor_id", sa.String(length=255)),
)


user_plants_table = sa.Table(
    "user_plants_userplant",
    SQL_METADATA,
    sa.Column("id", sa.BigInteger(), primary_key=True),
    sa.Column("personal_name", sa.String()),
)


sensor_readings_table = sa.Table(
    "sensor_readings",
    SQL_METADATA,
    sa.Column("id", sa.BigInteger(), primary_key=True),
    sa.Column("sensor_id", sa.BigInteger()),
    sa.Column("user_plant_id", sa.BigInteger()),
    sa.Column("timestamp", sa.DateTime()),
    sa.Column("temperature", sa.Float()),
    sa.Column("humidity", sa.Float()),
    sa.Column("moisture", sa.Float()),
    sa.Column("light", sa.Float()),
    sa.Column("moisture_voltage", sa.Float()),
    sa.Column("location", sa.String()),
    sa.ForeignKeyConstraint(["sensor_id"], ["device_sensor.id"]),
    sa.ForeignKeyConstraint(["user_plant_id"], ["user_plants_userplant.id"]),
    sa.UniqueConstraint("sensor_id", "timestamp", name="unique-sensor-timestamp-data"),
    schema="depot",
)


daily_data_summary_table = sa.Table(
    "daily_data_summary",
    SQL_METADATA,
    sa.Column("id", sa.BigInteger(), primary_key=True),
    sa.Column("sensor_id", sa.BigInteger(), nullable=False),
    sa.Column("user_plant_id", sa.BigInteger(), nullable=True),
    sa.Column("date", sa.Date(), nullable=False),
    sa.Column("temperature", sa.Float()),
    sa.Column("humidity", sa.Float()),
    sa.Column("moisture", sa.Float()),
    sa.Column("light", sa.Float()),
    sa.Column("location", sa.String()),
    sa.ForeignKeyConstraint(["sensor_id"], ["device.sensor_id"]),
    sa.ForeignKeyConstraint(["user_plant_id"], ["user_plants_userplant.id"]),
    sa.UniqueConstraint(
        "sensor_id",
        "date",
        name="single-daily-data-summary-per-sensor",
    ),
    schema="depot",
)


user_plant_temperature_score_table = sa.Table(
    "score_user_plant_temperature_score",
    SQL_METADATA,
    sa.Column("id", sa.BigInteger(), primary_key=True),
    sa.Column("user_plant_id", sa.BigInteger()),
    sa.Column("timestamp", sa.DateTime()),
    sa.Column("temperature_score", sa.Float()),
    sa.Column("temperature_rolled_score", sa.Float()),
    sa.Column("temperature_score_usable", sa.Boolean()),
    sa.ForeignKeyConstraint(["user_plant_id"], ["user_plants_userplant.id"]),
)


user_plant_humidity_score_table = sa.Table(
    "score_user_plant_humidity_score",
    SQL_METADATA,
    sa.Column("id", sa.BigInteger(), primary_key=True),
    sa.Column("user_plant_id", sa.BigInteger()),
    sa.Column("timestamp", sa.DateTime()),
    sa.Column("humidity_score", sa.Float()),
    sa.Column("humidity_rolled_score", sa.Float()),
    sa.Column("humidity_score_usable", sa.Boolean()),
    sa.ForeignKeyConstraint(["user_plant_id"], ["user_plants_userplant.id"]),
)


user_plant_light_score_table = sa.Table(
    "score_user_plant_light_score",
    SQL_METADATA,
    sa.Column("id", sa.BigInteger(), primary_key=True),
    sa.Column("user_plant_id", sa.BigInteger()),
    sa.Column("timestamp", sa.DateTime()),
    sa.Column("light_score", sa.Float()),
    sa.Column("light_rolled_score", sa.Float()),
    sa.Column("light_score_usable", sa.Boolean()),
    sa.ForeignKeyConstraint(["user_plant_id"], ["user_plants_userplant.id"]),
)


user_plant_moisture_score_table = sa.Table(
    "score_user_plant_moisture_score",
    SQL_METADATA,
    sa.Column("id", sa.BigInteger(), primary_key=True),
    sa.Column("user_plant_id", sa.BigInteger()),
    sa.Column("timestamp", sa.DateTime()),
    sa.Column("moisture_score", sa.Float()),
    sa.Column("moisture_rolled_score", sa.Float()),
    sa.Column("moisture_score_usable", sa.Boolean()),
    sa.ForeignKeyConstraint(["user_plant_id"], ["user_plants_userplant.id"]),
)


user_plant_score_table = sa.Table(
    "score_user_plant_score",
    SQL_METADATA,
    sa.Column("id", sa.BigInteger(), primary_key=True),
    sa.Column("user_plant_id", sa.BigInteger()),
    sa.Column("timestamp", sa.DateTime()),
    sa.Column("score", sa.Float()),
    sa.Column("rolled_score", sa.Float()),
    sa.Column("score_usable", sa.Boolean()),
    sa.ForeignKeyConstraint(["user_plant_id"], ["user_plants_userplant.id"]),
)
