from decimal import Decimal

import pytest
from ofyourinterest import utils
from ofyourinterest.data import Schedule

cases = [
    (
        Schedule.MONTHLY,
        Decimal(3),
        Decimal(1.10),
        Decimal(10335.35),
    ),
    (
        Schedule.QUARTERLY,
        Decimal(3),
        Decimal(1.10),
        Decimal(10335.04),
    ),
    (
        Schedule.YEARLY,
        Decimal(3),
        Decimal(1.10),
        Decimal(10333.64),
    ),
    (
        Schedule.AT_MATURITY,
        Decimal(3),
        Decimal(1.10),
        Decimal(10330.00),
    ),
    (
        Schedule.MONTHLY,
        Decimal(3),
        Decimal(6.00),
        Decimal(11966.81),
    ),
    (
        Schedule.QUARTERLY,
        Decimal(3),
        Decimal(6.00),
        Decimal(11956.18),
    ),
    (
        Schedule.YEARLY,
        Decimal(3),
        Decimal(6.00),
        Decimal(11910.16),
    ),
    (
        Schedule.AT_MATURITY,
        Decimal(3),
        Decimal(6.00),
        Decimal(11800.00),
    ),
    (
        Schedule.MONTHLY,
        Decimal(5),
        Decimal(1.10),
        Decimal(10565.14),
    ),
    (
        Schedule.QUARTERLY,
        Decimal(5),
        Decimal(1.10),
        Decimal(10564.61),
    ),
    (
        Schedule.YEARLY,
        Decimal(5),
        Decimal(1.10),
        Decimal(10562.23),
    ),
    (
        Schedule.AT_MATURITY,
        Decimal(5),
        Decimal(1.10),
        Decimal(10550.00),
    ),
    (
        Schedule.MONTHLY,
        Decimal(5),
        Decimal(6.00),
        Decimal(13488.50),
    ),
    (
        Schedule.QUARTERLY,
        Decimal(5),
        Decimal(6.00),
        Decimal(13468.55),
    ),
    (
        Schedule.YEARLY,
        Decimal(5),
        Decimal(6.00),
        Decimal(13382.26),
    ),
    (
        Schedule.AT_MATURITY,
        Decimal(5),
        Decimal(6.00),
        Decimal(13000.00),
    ),
]


@pytest.mark.parametrize("schedule, matures_in_years, rate, expected", cases)
def test_calculate_term_deposit_value(schedule, matures_in_years, rate, expected):
    # Interest and therefore final value is linear with the principal when there are no later deposits
    # So we can get away testing with a single principal except for edge case
    principal = Decimal(10_000)

    value = utils.calculate_term_deposit_value(
        principal=principal, rate=rate, matures_in_years=matures_in_years, schedule=schedule
    )
    # Let's round down the hard way for this first approach
    assert int(value) == int(expected)
