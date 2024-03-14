from datetime import datetime, timedelta
from migrator.services import archive_data


def lambda_handler(event, context):
    timestamp_upto = datetime.utcnow() - timedelta(days=60)
    ts = event.get("timestamp_upto")
    if ts:
        timestamp_upto = datetime.fromisoformat(ts)
    archive_data(
        timestamp_upto=timestamp_upto,
        selected_sensors=event.get("selected_sensors"),
        selected_user_plants=event.get("selected_user_plants"),
    )
