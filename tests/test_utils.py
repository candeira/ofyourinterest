import pytest

from ofyourinterest import utils
from ofyourinterest.data import Schedule, Percent, Periods, Years, Dollars

cases = [
    (
        Schedule.MONTHLY,
        Years(3),
        Percent(1.10),
        Dollars(10335.35),
    ),
    (
        Schedule.QUARTERLY,
        Years(3),
        Percent(1.10),
        Dollars(10335.04),
    ),
    (
        Schedule.YEARLY,
        Years(3),
        Percent(1.10),
        Dollars(10333.64),
    ),
    (
        Schedule.AT_MATURITY,
        Years(3),
        Percent(1.10),
        Dollars(10330.00),
    ),
    (
        Schedule.MONTHLY,
        Years(3),
        Percent(6.00),
        Dollars(11966.81),
    ),
    (
        Schedule.QUARTERLY,
        Years(3),
        Percent(6.00),
        Dollars(11956.18),
    ),
    (
        Schedule.YEARLY,
        Years(3),
        Percent(6.00),
        Dollars(11910.16),
    ),
    (
        Schedule.AT_MATURITY,
        Years(3),
        Percent(6.00),
        Dollars(11800.00),
    ),
    (
        Schedule.MONTHLY,
        Years(5),
        Percent(1.10),
        Dollars(10565.14),
    ),
    (
        Schedule.QUARTERLY,
        Years(5),
        Percent(1.10),
        Dollars(10564.61),
    ),
    (
        Schedule.YEARLY,
        Years(5),
        Percent(1.10),
        Dollars(10562.23),
    ),
    (
        Schedule.AT_MATURITY,
        Years(5),
        Percent(1.10),
        Dollars(10550.00),
    ),
    (
        Schedule.MONTHLY,
        Years(5),
        Percent(6.00),
        Dollars(13488.50),
    ),
    (
        Schedule.QUARTERLY,
        Years(5),
        Percent(6.00),
        Dollars(13468.55),
    ),
    (
        Schedule.YEARLY,
        Years(5),
        Percent(6.00),
        Dollars(13382.26),
    ),
    (
        Schedule.AT_MATURITY,
        Years(5),
        Percent(6.00),
        Dollars(13000.00),
    ),
]


@pytest.mark.parametrize("schedule, matures_in_years, rate, expected", cases)
def test_calculate_term_deposit_value(schedule, matures_in_years, rate, expected):
    # Interest and therefore final value is linear with the principal when there are no later deposits
    # So we can get away testing with a single principal except for edge case
    principal = Dollars(10_000)

    value = utils.calculate_term_deposit_value(
        principal=principal, rate=rate, matures_in_years=matures_in_years, schedule=schedule
    )
    # Let's round down the hard way for this first approach
    assert int(value) == int(expected)
