import argparse
from decimal import Decimal

from ofyourinterest import data, utils

parser = argparse.ArgumentParser(
    description="Calculate interest at maturity for a term deposit",
    epilog="Made with love and curiosity by Javier Candeira.",
)

MATURITY_CHOICES = [c.name for c in data.Schedule]

# All arguments optional with a sane default for ease of manual testing
# All arguments are parsed as strings: this makes sure we can produce the correct error message on parsing
parser.add_argument("-m", "--maturity", default="3", help="The deposit maturity time in integer years")
parser.add_argument("-r", "--rate", default="1.1", help="Interest rate with a maximum two decimal digits")
parser.add_argument(
    "-p",
    "--principal",
    default="10000",
    help="The amount invested at the start of the deposit. Dollars and cents, no fractional cents.",
)
# But this one is easy to validate upfront, so let's do it
parser.add_argument(
    "-s",
    "--schedule",
    choices=MATURITY_CHOICES,
    default="AT_MATURITY",
    help=f"How often the interest is calculated. Options are: {MATURITY_CHOICES} ",
)


def app() -> None:
    args = parser.parse_args()

    try:
        query = data.parse_term_deposit_query(
            schedule=args.schedule,
            rate=args.rate,
            principal=args.principal,
            matures_in_years=args.maturity,
        )
    except data.ValidationResult as result:
        print("Value cannot be calculated with the following inputs:")
        for message in result.error_messages:
            print(f"- {message}")
    else:
        value = utils.calculate_term_deposit_value(query)

        print("Calculating value at maturity for term deposit with conditions:")
        print(f"Maturity:     {args.maturity} years")
        print(f"Principal:    ${args.principal}")
        print(f"Rate:         {args.rate}%")
        print(f"Schedule:     {args.schedule}")
        print()
        # The web calculator doesn't show cents, it rounds dollars upwards, so...
        print(f"The value at maturity will be ${value.quantize(Decimal('0'))}")


if __name__ == "__main__":
    app()
