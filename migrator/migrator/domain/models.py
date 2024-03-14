import typing
from datetime import datetime, date as _date
from decimal import Decimal
from dataclasses import dataclass, fields


# Note: slots in dataclass are available in python 3.10


@dataclass(slots=True)
class Sensor:
    id: int
    sensor: str


@dataclass(slots=True)
class UserPlant:
    id: int
    personal_name: str


@dataclass(slots=True)
class Base:

    @staticmethod
    def _clean_for_dynamodb(item: typing.Any):
        if isinstance(item, datetime):
            return item.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(item, _date):
            return item.isoformat()
        elif isinstance(item, float):
            return Decimal(str(item))
        return item

    def to_dict(self):
        return {
            field.name: self._clean_for_dynamodb(getattr(self, field.name))
            for field in fields(self)
        }


@dataclass(slots=True)
class SensorData(Base):
    id: int
    sensor: typing.Optional[str]
    sensor_id: int
    user_plant_id: typing.Optional[int]
    timestamp: datetime
    temperature: float
    humidity: float
    moisture: float
    light: float
    moisture_voltage: float
    location: typing.Optional[str]


@dataclass(slots=True)
class DailyDataSummary(Base):
    id: int
    sensor: typing.Optional[str]
    sensor_id: int
    user_plant_id: typing.Optional[int]
    date: _date
    temperature: typing.Optional[float]
    humidity: typing.Optional[float]
    moisture: typing.Optional[float]
    light: typing.Optional[float]
    location: typing.Optional[str]


@dataclass(slots=True)
class UserPlantTemperatureScore(Base):
    id: int
    user_plant: str
    user_plant_id: int
    timestamp: datetime
    temperature_score: float
    temperature_rolled_score: typing.Optional[float]
    temperature_score_usable: bool


@dataclass(slots=True)
class UserPlantHumidityScore(Base):
    id: int
    user_plant: str
    user_plant_id: int
    timestamp: datetime
    humidity_score: float
    humidity_rolled_score: typing.Optional[float]
    humidity_score_usable: bool


@dataclass(slots=True)
class UserPlantLightScore(Base):
    id: int
    user_plant: str
    user_plant_id: int
    timestamp: datetime
    light_score: float
    light_rolled_score: typing.Optional[float]
    light_score_usable: bool


@dataclass(slots=True)
class UserPlantMoistureScore(Base):
    id: int
    user_plant: str
    user_plant_id: int
    timestamp: datetime
    moisture_score: float
    moisture_rolled_score: typing.Optional[float]
    moisture_score_usable: bool


@dataclass(slots=True)
class UserPlantScore(Base):
    id: int
    user_plant: str
    user_plant_id: int
    timestamp: datetime
    score: float
    rolled_score: typing.Optional[float]
    score_usable: bool
