from _decimal import Decimal


def round_percent_string_to_decimal(value):
    return round(Decimal(value[:-1].replace(',', '.')), 2)