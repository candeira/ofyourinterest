from decimal import Decimal
from .data import Schedule, periods_per_year, Periods, Years, Percent, Dollars


def do_something_useful() -> None:
    print("Replace this with a utility function")


def _calculate_payment_periods(matures_in_years: Years, schedule: Schedule) -> Periods:
    return Periods(matures_in_years * periods_per_year(schedule))


def _calculate_period_rate(rate: Percent, schedule: Schedule) -> Percent:
    if schedule == Schedule.AT_MATURITY:
        return Percent(rate / Decimal(100))
    return Percent((rate / 100) / periods_per_year(schedule))


def calculate_term_deposit_value(
    *, principal: Dollars, rate: Percent, matures_in_years: Years, schedule: Schedule
) -> Dollars:
    if schedule == Schedule.AT_MATURITY:
        return Dollars(principal * Decimal(1 + (rate / 100) * matures_in_years))
    periods = _calculate_payment_periods(matures_in_years, schedule)
    period_rate = _calculate_period_rate(rate, schedule)
    return Dollars(principal * Decimal((1 + period_rate) ** periods))
