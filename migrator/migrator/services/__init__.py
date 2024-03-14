import logging
import typing
from datetime import datetime
from core.settings import PostgresDatabase, dynamodb_resource
from migrator.repository.postgres import SqlRepo
from migrator.repository.dynamodb import DynamoRepo


LOGGER = logging.getLogger(__name__)


def archive_data(
    timestamp_upto: datetime,
    selected_sensors: typing.Optional[typing.List[int]] = None,
    selected_user_plants: typing.Optional[typing.List[int]] = None,
):
    LOGGER.info("Starting migrating data")
    date_upto = timestamp_upto.date()
    dynamo_repo = DynamoRepo(dynamodb_resource)
    with PostgresDatabase() as conn:
        postgres_repo = SqlRepo(conn)
        sensors = postgres_repo.get_sensors()
    for sensor in sensors:
        if selected_sensors and sensor.id not in selected_sensors:
            LOGGER.info(f"Skipping sensor: {sensor}")
            continue
        try:
            with PostgresDatabase() as conn:
                postgres_repo = SqlRepo(conn)
                LOGGER.info(f"Working on {sensor.sensor} for sensor data")
                data = postgres_repo.get_sensor_data(sensor, timestamp_upto)
                dynamo_repo.save_sensor_data(data)
                postgres_repo.delete_sensor_data(sensor, timestamp_upto)
                LOGGER.info(f"Working on {sensor.sensor} for daily sensor data")
                daily_data = postgres_repo.get_daily_data_summary(sensor, date_upto)
                dynamo_repo.save_daily_sensor_data(daily_data)
                postgres_repo.delete_daily_data_summary(sensor, date_upto)
        except Exception as e:
            LOGGER.error(f"Error Archiving sensor: {sensor}: {str(e)}")
    with PostgresDatabase() as conn:
        postgres_repo = SqlRepo(conn)
        user_plants = postgres_repo.get_user_plants()
    for user_plant in user_plants:
        if selected_user_plants and user_plant.id not in selected_user_plants:
            continue
        try:
            with PostgresDatabase() as conn:
                postgres_repo = SqlRepo(conn)
                LOGGER.info(f"Working on {user_plant.personal_name} for score")
                score = postgres_repo.get_user_plant_score(user_plant, timestamp_upto)
                dynamo_repo.save_user_plant_score(score)
                postgres_repo.delete_user_plant_score(user_plant, timestamp_upto)
                LOGGER.info(
                    f"Working on {user_plant.personal_name} for temperature score"
                )
                temperature_score = postgres_repo.get_user_plant_temperature_score(
                    user_plant, timestamp_upto
                )
                dynamo_repo.save_temperature_user_plant_score(temperature_score)
                postgres_repo.delete_user_plant_temperature_score(
                    user_plant, timestamp_upto
                )
                LOGGER.info(f"Working on {user_plant.personal_name} for humidity score")
                humidity_score = postgres_repo.get_user_plant_humidity_score(
                    user_plant, timestamp_upto
                )
                dynamo_repo.save_humidity_user_plant_score(humidity_score)
                postgres_repo.delete_user_plant_humidity_score(
                    user_plant, timestamp_upto
                )
                LOGGER.info(f"Working on {user_plant.personal_name} for light score")
                light_score = postgres_repo.get_user_plant_light_score(
                    user_plant, timestamp_upto
                )
                dynamo_repo.save_light_user_plant_score(light_score)
                postgres_repo.delete_user_plant_light_score(user_plant, timestamp_upto)
                LOGGER.info(f"Working on {user_plant.personal_name} for moisture score")
                moisture_score = postgres_repo.get_user_plant_moisture_score(
                    user_plant, timestamp_upto
                )
                dynamo_repo.save_moisture_user_plant_score(moisture_score)
                postgres_repo.delete_user_plant_moisture_score(
                    user_plant, timestamp_upto
                )
        except Exception as e:
            LOGGER.error(f"Error Archiving user plant: {user_plant}: {str(e)}")
