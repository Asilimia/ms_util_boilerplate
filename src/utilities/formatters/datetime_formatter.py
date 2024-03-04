import datetime


def format_datetime_into_isoformat(date_time: datetime.datetime) -> str:
    """
    The function `format_datetime_into_isoformat` converts a given datetime object
    into an ISO 8601 formatted string.

    :param date_time: datetime.datetime object representing a specific date and time
    :type date_time: datetime.datetime
    :return: a string representation of the input datetime object in ISO 8601
    format.
    """
    return (
        date_time.replace(tzinfo=datetime.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )
