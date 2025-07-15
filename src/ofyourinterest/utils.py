from decimal import Decimal
from .data import Schedule, periods_per_year


def do_something_useful() -> None:
    print("Replace this with a utility function")


def _calculate_payment_periods(matures_in_years: Decimal, schedule: Schedule) -> Decimal:
    return matures_in_years * periods_per_year(schedule)


def _calculate_period_rate(rate: Decimal, schedule: Schedule) -> Decimal:
    if schedule == Schedule.AT_MATURITY:
        return rate / Decimal(100)
    return (rate / 100) / periods_per_year(schedule)


def calculate_term_deposit_value(
    *, principal: Decimal, rate: Decimal, matures_in_years: Decimal, schedule: Schedule
) -> Decimal:
    if schedule == Schedule.AT_MATURITY:
        return principal * Decimal(1 + (rate / 100) * matures_in_years)
    periods = _calculate_payment_periods(matures_in_years, schedule)
    period_rate = _calculate_period_rate(rate, schedule)
    return principal * Decimal((1 + period_rate) ** periods)
