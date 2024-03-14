import traceback
import typing
import logging
from core import exceptions as exc
from mypy_boto3_dynamodb.service_resource import Table, DynamoDBServiceResource
from core.settings import (
    DYNAMODB_SENSOR_DATA_TABLE,
    DYNAMODB_DAILY_SENSOR_DATA_TABLE,
    DYNAMODB_PLANT_SCORE_TABLE,
    DYNAMODB_PLANT_TEMPERATURE_SCORE_TABLE,
    DYNAMODB_PLANT_HUMIDITY_SCORE_TABLE,
    DYNAMODB_PLANT_LIGHT_SCORE_TABLE,
    DYNAMODB_PLANT_MOISTURE_SCORE_TABLE,
)
from migrator.domain import models as m


LOGGER = logging.getLogger(__name__)


class DynamoRepo:
    def __init__(self, dynamo_resource: DynamoDBServiceResource) -> None:
        self.sensor_data_table: Table = dynamo_resource.Table(
            DYNAMODB_SENSOR_DATA_TABLE
        )
        self.daily_sensor_data_table: Table = dynamo_resource.Table(
            DYNAMODB_DAILY_SENSOR_DATA_TABLE
        )
        self.score_table: Table = dynamo_resource.Table(DYNAMODB_PLANT_SCORE_TABLE)
        self.temperature_score_table: Table = dynamo_resource.Table(
            DYNAMODB_PLANT_TEMPERATURE_SCORE_TABLE
        )
        self.humidity_score_table: Table = dynamo_resource.Table(
            DYNAMODB_PLANT_HUMIDITY_SCORE_TABLE
        )
        self.light_score_table: Table = dynamo_resource.Table(
            DYNAMODB_PLANT_LIGHT_SCORE_TABLE
        )
        self.moisture_score_table: Table = dynamo_resource.Table(
            DYNAMODB_PLANT_MOISTURE_SCORE_TABLE
        )

    def save_sensor_data(self, data: typing.List[m.SensorData]):
        try:
            for item in data:
                self.sensor_data_table.put_item(
                    Item=item.to_dict(),
                )
        except Exception as e:
            traceback.print_exc()
            raise exc.DbException(str(e)) from e

    def save_daily_sensor_data(self, data: typing.List[m.DailyDataSummary]):
        try:
            for item in data:
                self.daily_sensor_data_table.put_item(Item=item.to_dict())
        except Exception as e:
            traceback.print_exc()
            raise exc.DbException(str(e)) from e

    def save_user_plant_score(self, data: typing.List[m.UserPlantScore]):
        try:
            for item in data:
                self.score_table.put_item(Item=item.to_dict())
        except Exception as e:
            traceback.print_exc()
            raise exc.DbException(str(e)) from e

    def save_temperature_user_plant_score(
        self, data: typing.List[m.UserPlantTemperatureScore]
    ):
        try:
            for item in data:
                self.temperature_score_table.put_item(Item=item.to_dict())
        except Exception as e:
            traceback.print_exc()
            raise exc.DbException(str(e)) from e

    def save_moisture_user_plant_score(
        self, data: typing.List[m.UserPlantMoistureScore]
    ):
        try:
            for item in data:
                self.moisture_score_table.put_item(Item=item.to_dict())
        except Exception as e:
            traceback.print_exc()
            raise exc.DbException(str(e)) from e

    def save_light_user_plant_score(self, data: typing.List[m.UserPlantLightScore]):
        try:
            for item in data:
                self.light_score_table.put_item(Item=item.to_dict())
        except Exception as e:
            traceback.print_exc()
            raise exc.DbException(str(e)) from e

    def save_humidity_user_plant_score(
        self, data: typing.List[m.UserPlantHumidityScore]
    ):
        try:
            for item in data:
                self.humidity_score_table.put_item(Item=item.to_dict())
        except Exception as e:
            traceback.print_exc()
            raise exc.DbException(str(e)) from e
