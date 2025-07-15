from decimal import Decimal
from enum import Enum


# In reality we'd use a currency class with different currencies
# Here we're ensuring we don't pass naked numbers around
class Dollars(Decimal):
    pass


# TODO: We'd probably want to also validate percentages are in a range
class Percent(Decimal):
    pass


class Periods(Decimal):
    pass


# For this test we're only going to take deposits in integer years
class Years(Decimal):
    pass


class Schedule(Enum):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"
    AT_MATURITY = "AT_MATURITY"


def periods_per_year(schedule: Schedule) -> Periods:
    return {
        Schedule.MONTHLY: Periods(12),
        Schedule.QUARTERLY: Periods(4),
        Schedule.YEARLY: Periods(1),
        Schedule.AT_MATURITY: Periods(1),
    }[schedule]
