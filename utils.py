import re
from datetime import datetime, timedelta, date
import pytz
from dateutil.relativedelta import relativedelta

tz = pytz.timezone("Asia/Shanghai")


def get_now() -> datetime:
    return datetime.now(tz=tz)


def get_today():
    return date.today()


def format_date(d: str) -> date:
    try:
        return datetime.strptime(d, "%Y/%m/%d").date()
    except ValueError:
        return datetime.min.date()


def convert_to_date(time_ago: str) -> date:
    match = re.match(r'(\d+)\s*(天|年|个月|月)', time_ago)
    if not match:
        raise ValueError(f"Invalid time ago '{time_ago}'")

    num, unit = match.groups()
    num = int(num)
    now = get_now()

    if unit == '天':
        time_difference = timedelta(days=num)
    elif unit == '月' or unit == '个月':
        time_difference = relativedelta(months=num)
    elif unit == '年':
        time_difference = relativedelta(years=num)
    else:
        raise ValueError(f"Invalid time delta '{time_ago}'")

    return (now - time_difference).date()
