import typing
from datetime import datetime, date as _date
from dataclasses import dataclass


# Note: slots in dataclass are available in python 3.10


@dataclass(slots=True)
class SensorData:
    sensor: typing.Optional[str]
    user_plant: typing.Optional[str]
    timestamp: datetime
    temperature: float
    humidity: float
    moisture: float
    light: float
    moisture_voltage: float
    location: typing.Optional[str]


@dataclass(slots=True)
class DailyDataSummary:
    sensor: typing.Optional[str]
    user_plant: typing.Optional[str]
    date: _date
    temperature: typing.Optional[float]
    humidity: typing.Optional[float]
    moisture: typing.Optional[float]
    light: typing.Optional[float]
    location: typing.Optional[str]


@dataclass(slots=True)
class UserPlantTemperatureScore:
    user_plant: str
    timestamp: datetime
    temperature_score: float
    temperature_rolled_score: typing.Optional[float]
    temperature_score_usable: bool


@dataclass(slots=True)
class UserPlantHumidityScore:
    user_plant: str
    timestamp: datetime
    humidity_score: float
    humidity_rolled_score: typing.Optional[float]
    humidity_score_usable: bool


@dataclass(slots=True)
class UserPlantLightScore:
    user_plant: str
    timestamp: datetime
    light_score: float
    light_rolled_score: typing.Optional[float]
    light_score_usable: bool


@dataclass(slots=True)
class UserPlantMoistureScore:
    user_plant: str
    timestamp: datetime
    moisture_score: float
    moisture_rolled_score: typing.Optional[float]
    moisture_score_usable: bool


@dataclass(slots=True)
class UserPlantScore:
    user_plant: str
    timestamp: datetime
    score: float
    rolled_score: typing.Optional[float]
    score_usable: bool
