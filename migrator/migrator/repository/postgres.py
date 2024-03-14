import logging
import typing
import sqlalchemy as sa
from datetime import date, datetime
from migrator.adapters import orm as o
from migrator.domain import models as m

from core.protocols import DbConnection


LOGGER = logging.getLogger(__name__)


class SqlRepo:
    def __init__(self, conn: DbConnection):
        self.conn = conn

    def get_sensors(self) -> typing.List[m.Sensor]:
        query = sa.select(
            [
                o.sensor_table.c.id,
                o.sensor_table.c.sensor_id,
            ]
        )
        resp = self.conn.execute(query).fetchall()
        LOGGER.info(f"Collected {len(resp)} sensors.")
        return [
            m.Sensor(
                id=item["id"],
                sensor=item["sensor_id"],
            )
            for item in resp
        ]

    def get_user_plants(self) -> typing.List[m.UserPlant]:
        query = sa.select(
            [
                o.user_plants_table.c.id,
                o.user_plants_table.c.personal_name,
            ]
        )
        resp = self.conn.execute(query).fetchall()
        LOGGER.info(f"Collected {len(resp)} user plants.")
        return [
            m.UserPlant(
                id=item["id"],
                personal_name=item["personal_name"],
            )
            for item in resp
        ]

    def get_sensor_data(
        self, sensor: m.Sensor, timestamp_upto: datetime
    ) -> typing.List[m.SensorData]:
        query = sa.select(
            [
                o.sensor_readings_table.c.id,
                o.sensor_readings_table.c.sensor_id,
                o.sensor_readings_table.c.user_plant_id,
                o.sensor_readings_table.c.timestamp,
                o.sensor_readings_table.c.temperature,
                o.sensor_readings_table.c.humidity,
                o.sensor_readings_table.c.moisture,
                o.sensor_readings_table.c.light,
                o.sensor_readings_table.c.moisture_voltage,
                o.sensor_readings_table.c.location,
            ]
        ).where(
            sa.and_(
                o.sensor_readings_table.c.sensor_id == sensor.id,
                o.sensor_readings_table.c.timestamp <= timestamp_upto,
            )
        )
        resp = self.conn.execute(query).fetchall()
        LOGGER.info(f"Collected {len(resp)} sensor data")
        return [
            m.SensorData(
                id=item["id"],
                sensor=sensor.sensor,
                sensor_id=sensor.id,
                user_plant_id=item["user_plant_id"],
                timestamp=item["timestamp"],
                temperature=item["temperature"],
                humidity=item["humidity"],
                moisture=item["moisture"],
                light=item["light"],
                moisture_voltage=item["moisture_voltage"],
                location=item["location"],
            )
            for item in resp
        ]

    def delete_sensor_data(self, sensor: m.Sensor, timestamp_upto: datetime):
        query = sa.delete(o.sensor_readings_table).where(
            sa.and_(
                o.sensor_readings_table.c.sensor_id == sensor.id,
                o.sensor_readings_table.c.timestamp <= timestamp_upto,
            )
        )
        res = self.conn.execute(query)
        LOGGER.info(
            f"Deleted {getattr(res, 'rowcount')} sensor data rows for sensor: {sensor}. Upto {timestamp_upto}"
        )

    def get_daily_data_summary(
        self, sensor: m.Sensor, date_upto: date
    ) -> typing.List[m.DailyDataSummary]:
        query = sa.select(
            [
                o.daily_data_summary_table.c.id,
                o.daily_data_summary_table.c.sensor_id,
                o.daily_data_summary_table.c.user_plant_id,
                o.daily_data_summary_table.c.date,
                o.daily_data_summary_table.c.temperature,
                o.daily_data_summary_table.c.humidity,
                o.daily_data_summary_table.c.moisture,
                o.daily_data_summary_table.c.light,
                o.daily_data_summary_table.c.moisture_voltage,
                o.daily_data_summary_table.c.location,
            ]
        ).where(
            sa.and_(
                o.daily_data_summary_table.c.sensor_id == sensor.id,
                o.daily_data_summary_table.c.date <= date_upto,
            )
        )
        resp = self.conn.execute(query).fetchall()
        LOGGER.info(f"Collected {len(resp)} daily sensor data")
        return [
            m.DailyDataSummary(
                id=item["id"],
                sensor=sensor.sensor,
                sensor_id=sensor.id,
                user_plant_id=item["user_plant_id"],
                date=item["date"],
                temperature=item["temperature"],
                humidity=item["humidity"],
                moisture=item["moisture"],
                light=item["light"],
                location=item["location"],
            )
            for item in resp
        ]

    def delete_daily_data_summary(self, sensor: m.Sensor, date_upto: date):
        query = sa.delete(o.daily_data_summary_table).where(
            sa.and_(
                o.daily_data_summary_table.c.sensor_id == sensor.id,
                o.daily_data_summary_table.c.timestamp <= date_upto,
            )
        )
        res = self.conn.execute(query)
        LOGGER.info(
            f"Deleted {getattr(res, 'rowcount')} daily data summary rows for sensor: {sensor}. Upto: {date_upto}"
        )

    def get_user_plant_temperature_score(
        self, user_plant: m.UserPlant, timestamp_upto: datetime
    ) -> typing.List[m.UserPlantTemperatureScore]:
        query = sa.select(
            [
                o.user_plant_temperature_score_table.c.id,
                o.user_plant_temperature_score_table.c.timestamp,
                o.user_plant_temperature_score_table.c.temperature_score,
                o.user_plant_temperature_score_table.c.temperature_rolled_score,
                o.user_plant_temperature_score_table.c.temperature_score_usable,
            ]
        ).where(
            sa.and_(
                o.user_plant_temperature_score_table.c.user_plant_id == user_plant.id,
                o.user_plant_temperature_score_table.c.timestamp <= timestamp_upto,
            )
        )
        resp = self.conn.execute(query).fetchall()
        LOGGER.info(f"Collected {len(resp)} temperature score.")
        return [
            m.UserPlantTemperatureScore(
                id=item["id"],
                user_plant=user_plant.personal_name,
                user_plant_id=user_plant.id,
                timestamp=item["timestamp"],
                temperature_score=item["temperature_score"],
                temperature_rolled_score=item["temperature_rolled_score"],
                temperature_score_usable=item["temperature_rolled_usable"],
            )
            for item in resp
        ]

    def delete_user_plant_temperature_score(
        self, user_plant: m.UserPlant, timestamp_upto: datetime
    ):
        query = sa.delete(o.user_plant_temperature_score_table).where(
            sa.and_(
                o.user_plant_temperature_score_table.c.user_plant_id == user_plant.id,
                o.user_plant_temperature_score_table.c.timestamp <= timestamp_upto,
            )
        )
        res = self.conn.execute(query)
        LOGGER.info(
            f"Deleted {getattr(res, 'rowcount')} temperature score rows for user plant: {user_plant}. Upto {timestamp_upto}"
        )

    def get_user_plant_humidity_score(
        self, user_plant: m.UserPlant, timestamp_upto: datetime
    ) -> typing.List[m.UserPlantHumidityScore]:
        query = sa.select(
            [
                o.user_plant_humidity_score_table.c.id,
                o.user_plant_humidity_score_table.c.timestamp,
                o.user_plant_humidity_score_table.c.humidity_score,
                o.user_plant_humidity_score_table.c.humidity_rolled_score,
                o.user_plant_humidity_score_table.c.humidity_score_usable,
            ]
        ).where(
            sa.and_(
                o.user_plant_humidity_score_table.c.user_plant_id == user_plant.id,
                o.user_plant_humidity_score_table.c.timestamp <= timestamp_upto,
            )
        )
        resp = self.conn.execute(query).fetchall()
        LOGGER.info(f"Collected {len(resp)} humidity score.")
        return [
            m.UserPlantHumidityScore(
                id=item["id"],
                user_plant=user_plant.personal_name,
                user_plant_id=user_plant.id,
                timestamp=item["timestamp"],
                humidity_score=item["humidity_score"],
                humidity_rolled_score=item["humidity_rolled_score"],
                humidity_score_usable=item["humidity_rolled_usable"],
            )
            for item in resp
        ]

    def delete_user_plant_humidity_score(
        self, user_plant: m.UserPlant, timestamp_upto: datetime
    ):
        query = sa.delete(o.user_plant_humidity_score_table).where(
            sa.and_(
                o.user_plant_humidity_score_table.c.user_plant_id == user_plant.id,
                o.user_plant_humidity_score_table.c.timestamp <= timestamp_upto,
            )
        )
        res = self.conn.execute(query)
        LOGGER.info(
            f"Deleted {getattr(res, 'rowcount')} humidity score rows for user plant: {user_plant}. Upto {timestamp_upto}"
        )

    def get_user_plant_light_score(
        self, user_plant: m.UserPlant, timestamp_upto: datetime
    ) -> typing.List[m.UserPlantLightScore]:
        query = sa.select(
            [
                o.user_plant_light_score_table.c.id,
                o.user_plant_light_score_table.c.timestamp,
                o.user_plant_light_score_table.c.light_score,
                o.user_plant_light_score_table.c.light_rolled_score,
                o.user_plant_light_score_table.c.light_score_usable,
            ]
        ).where(
            sa.and_(
                o.user_plant_light_score_table.c.user_plant_id == user_plant.id,
                o.user_plant_light_score_table.c.timestamp <= timestamp_upto,
            )
        )
        resp = self.conn.execute(query).fetchall()
        LOGGER.info(f"Collected {len(resp)} light score.")
        return [
            m.UserPlantLightScore(
                id=item["id"],
                user_plant=user_plant.personal_name,
                user_plant_id=user_plant.id,
                timestamp=item["timestamp"],
                light_score=item["light_score"],
                light_rolled_score=item["light_rolled_score"],
                light_score_usable=item["light_rolled_usable"],
            )
            for item in resp
        ]

    def delete_user_plant_light_score(
        self, user_plant: m.UserPlant, timestamp_upto: datetime
    ):
        query = sa.delete(o.user_plant_light_score_table).where(
            sa.and_(
                o.user_plant_light_score_table.c.user_plant_id == user_plant.id,
                o.user_plant_light_score_table.c.timestamp <= timestamp_upto,
            )
        )
        res = self.conn.execute(query)
        LOGGER.info(
            f"Deleted {getattr(res, 'rowcount')} light score rows for user plant: {user_plant}. Upto {timestamp_upto}"
        )

    def get_user_plant_moisture_score(
        self, user_plant: m.UserPlant, timestamp_upto: datetime
    ) -> typing.List[m.UserPlantMoistureScore]:
        query = sa.select(
            [
                o.user_plant_moisture_score_table.c.id,
                o.user_plant_moisture_score_table.c.timestamp,
                o.user_plant_moisture_score_table.c.moisture_score,
                o.user_plant_moisture_score_table.c.moisture_rolled_score,
                o.user_plant_moisture_score_table.c.moisture_score_usable,
            ]
        ).where(
            sa.and_(
                o.user_plant_moisture_score_table.c.user_plant_id == user_plant.id,
                o.user_plant_moisture_score_table.c.timestamp <= timestamp_upto,
            )
        )
        resp = self.conn.execute(query).fetchall()
        LOGGER.info(f"Collected {len(resp)} moisture score.")
        return [
            m.UserPlantMoistureScore(
                id=item["id"],
                user_plant=user_plant.personal_name,
                user_plant_id=user_plant.id,
                timestamp=item["timestamp"],
                moisture_score=item["moisture_score"],
                moisture_rolled_score=item["moisture_rolled_score"],
                moisture_score_usable=item["moisture_rolled_usable"],
            )
            for item in resp
        ]

    def delete_user_plant_moisture_score(
        self, user_plant: m.UserPlant, timestamp_upto: datetime
    ):
        query = sa.delete(o.user_plant_moisture_score_table).where(
            sa.and_(
                o.user_plant_moisture_score_table.c.user_plant_id == user_plant.id,
                o.user_plant_moisture_score_table.c.timestamp <= timestamp_upto,
            )
        )
        res = self.conn.execute(query)
        LOGGER.info(
            f"Deleted {getattr(res, 'rowcount')} moisture score rows for user plant: {user_plant}. Upto {timestamp_upto}"
        )

    def get_user_plant_score(
        self, user_plant: m.UserPlant, timestamp_upto: datetime
    ) -> typing.List[m.UserPlantScore]:
        query = sa.select(
            [
                o.user_plant_score_table.c.id,
                o.user_plant_score_table.c.timestamp,
                o.user_plant_score_table.c.score,
                o.user_plant_score_table.c.rolled_score,
                o.user_plant_score_table.c.score_usable,
            ]
        ).where(
            sa.and_(
                o.user_plant_score_table.c.user_plant_id == user_plant.id,
                o.user_plant_score_table.c.timestamp <= timestamp_upto,
            )
        )
        resp = self.conn.execute(query).fetchall()
        LOGGER.info(f"Collected {len(resp)} score.")
        return [
            m.UserPlantScore(
                id=item["id"],
                user_plant=user_plant.personal_name,
                user_plant_id=user_plant.id,
                timestamp=item["timestamp"],
                score=item["score"],
                rolled_score=item["rolled_score"],
                score_usable=item["rolled_usable"],
            )
            for item in resp
        ]

    def delete_user_plant_score(
        self, user_plant: m.UserPlant, timestamp_upto: datetime
    ):
        query = sa.delete(o.user_plant_score_table).where(
            sa.and_(
                o.user_plant_score_table.c.user_plant_id == user_plant.id,
                o.user_plant_score_table.c.timestamp <= timestamp_upto,
            )
        )
        res = self.conn.execute(query)
        LOGGER.info(
            f"Deleted {getattr(res, 'rowcount')} plant score rows for user plant: {user_plant}. Upto {timestamp_upto}"
        )
