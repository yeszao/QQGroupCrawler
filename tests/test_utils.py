from dateutil.relativedelta import relativedelta

from utils import convert_to_date, get_now


def test_convert_to_datetime():
    assert convert_to_date("1年") == get_now().date() - relativedelta(years=1)
    assert convert_to_date("1天") == get_now().date() - relativedelta(days=1)
    assert convert_to_date("10个月") == get_now().date() - relativedelta(months=10)
