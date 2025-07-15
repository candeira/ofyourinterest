from decimal import Decimal
from enum import Enum


class Schedule(Enum):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"
    AT_MATURITY = "AT_MATURITY"


def periods_per_year(schedule: Schedule) -> Decimal:
    return {
        Schedule.MONTHLY: Decimal(12),
        Schedule.QUARTERLY: Decimal(4),
        Schedule.YEARLY: Decimal(1),
        Schedule.AT_MATURITY: Decimal(1),
    }[schedule]
