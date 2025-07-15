from decimal import Decimal

from ofyourinterest import utils
from ofyourinterest import data


def test_calculate_term_deposit_value():
    expected = Decimal(10_330)
    # Harcoded the hard way for this first approach
    value = utils.calculate_term_deposit_value(
        principal=Decimal(10_000), rate=Decimal(1.1), matures_in_years=Decimal(3), schedule=data.Schedule.AT_MATURITY
    )
    # Let's round down the hard way for this first approach
    assert int(value) == int(expected)
