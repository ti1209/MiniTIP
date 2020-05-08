from datetime import datetime, timezone
import pytz
from MiniTIP.settings import TIME_ZONE


def iso_to_datetime(date):
    tz = pytz.timezone(TIME_ZONE)
    index = date.find('.')
    if index != -1:
        date = date[:index]
    datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    datetime_aware = datetime_object.replace(tzinfo=timezone.utc).astimezone(tz)
    return datetime_aware
