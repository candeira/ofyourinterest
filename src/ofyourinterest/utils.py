from decimal import Decimal

from .data import Dollars, Percent, Periods, Schedule, Years, periods_per_year, TermDepositQuery


def do_something_useful() -> None:
    print("Replace this with a utility function")


def _calculate_payment_periods(matures_in_years: Years, schedule: Schedule) -> Periods:
    return Periods(matures_in_years * periods_per_year(schedule))


def _calculate_period_rate(rate: Percent, schedule: Schedule) -> Percent:
    if schedule == Schedule.AT_MATURITY:
        return Percent(rate / Decimal(100))
    return Percent((rate / 100) / periods_per_year(schedule))


def calculate_term_deposit_value(q: TermDepositQuery) -> Dollars:
    if q.schedule == Schedule.AT_MATURITY:
        return Dollars(q.principal * Decimal(1 + (q.rate / 100) * q.matures_in_years))
    periods = _calculate_payment_periods(q.matures_in_years, q.schedule)
    period_rate = _calculate_period_rate(q.rate, q.schedule)
    return Dollars(q.principal * Decimal((1 + period_rate) ** periods))
