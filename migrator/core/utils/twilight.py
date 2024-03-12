import logging
import requests
import typing
from datetime import time, date
from urllib.parse import urlencode
from core import exceptions as exc


LOGGER = logging.getLogger(__name__)
API_URL = "https://api.sunrise-sunset.org/json"


def convert24(timestr: str):
    """
    Convert 12 hour representation to 24 hour
    e.g: 1:12:00 PM to 13:12:00
    """
    if timestr[-2:] == "AM" and timestr[:2] == "12":
        v = "00" + timestr[2:-2]
    elif timestr[-2:] == "AM":
        v = timestr[:-2]
    elif timestr[-2:] == "PM" and timestr[:2] == "12":
        v = timestr[:-2]
    else:
        v = (
            str(int(timestr.split(":")[0]) + 12)
            + ":"
            + timestr.split(":", maxsplit=2)[1]
        )
    return [int(x) for x in v.strip().split(":")]


def parse_to_time(timestamp: typing.List[int]):
    """Convert timestamp instance to time"""
    return time(*timestamp)


def get_sunrise_sunset_time(
    latitude: float,
    longitude: float,
    date_: typing.Optional[date] = None,
) -> typing.Dict[str, time]:
    """Using latitude and longitude, returns sunrise and sunset time"""
    params = {
        "lat": latitude,
        "lng": longitude,
    }
    if date_ is not None:
        params.update({"date": date_.isoformat()})
    url = f"{API_URL}?{urlencode(params)}"
    LOGGER.debug(f"Calling SunriseSunset api for {str(params)}")
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            raise exc.SunriseSunsetAPIError(str(resp.text))
        data = resp.json()
        sunrise_time = data["results"]["sunrise"]
        sunset_time = data["results"]["sunset"]
        sunrise = parse_to_time(convert24(sunrise_time))
        sunset = parse_to_time(convert24(sunset_time))
    except requests.RequestException as e:
        LOGGER.error(f"Error while fetching sunset-sunrise: {str(e)}")
        raise exc.HTTPException(str(e))
    except KeyError:
        e = "Sunrise and sunset api changed their output format"
        LOGGER.error(e)
        raise exc.SunriseSunsetAPIError(e)
    except Exception as e:
        LOGGER.error(f"Error sunrise-sunset api: {str(e)}")
        raise
    return {
        "sunrise": sunrise,
        "sunset": sunset,
    }


def check_is_day(
    now: time,
    sunrise: time,
    sunset: time,
) -> bool:
    if sunrise < sunset:
        return (now >= sunrise) and (now <= sunset)
    return (now >= sunrise) or (now <= sunset)
