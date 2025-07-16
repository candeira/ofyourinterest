from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Type, Sequence


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


@dataclass(frozen=True, slots=True)
class TermDepositQuery:
    schedule: Schedule
    rate: Percent
    principal: Dollars
    matures_in_years: Years


# Validators/parsers would normally go in a different file, but for expediency...
# Parsers called `parse_` are validators that return a value or raise a ValidationResult as an error.
# Validators called `validate` return a ValidationResult and are used by the parsers
# This is an experimental style so the validate_*** results are values that can be accumulated by the parsers
# The parsers however would need to return the parsed value, so we want to raise the result as an exception

# ABSOLUTELY NOT FOR PRODUCTION: I wanted to experiment and I used the code sample to do it.

# However, about the coding style:
# This is the kind of thing that could be in a style guide so everybody writes the same style...
# The most important thing is not the style itself; rather, the composability afforded by everyone
# writing code in the same style.


@dataclass(frozen=True, slots=True)
class ValidationResult(Exception):
    """
    From my personal experiments, a dataclass that inherits from Exception.
    Not for production; don't try this at home!
    """

    is_valid: bool
    error_messages: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.is_valid ^ (not bool(self.error_messages)):
            raise ValueError(
                "The 'error_messages' field is mandatory when the result is valid, and forbidden when it's invalid"
            )

    def __bool__(self) -> bool:
        return self.is_valid

    @classmethod
    def valid(cls: Type["ValidationResult"]) -> "ValidationResult":
        return cls(is_valid=True)

    @classmethod
    def failed_with(cls: Type["ValidationResult"], messages: str | Sequence[str]) -> "ValidationResult":
        error_messages: tuple[str, ...]
        if isinstance(messages, str):
            error_messages = (messages,)
        else:
            error_messages = tuple(messages)
        return cls(is_valid=False, error_messages=error_messages)


# Validators


def _validate_n_or_less_decimal_places(max_n_places: int, value: Decimal, fieldname: str = "") -> ValidationResult:
    """
    When writing this validator I realised that finance probably works in cents and basis points,
    but it was too late to refactor. I just wanted to write a validator as well as a parser.
    """
    decimal_tuple = value.as_tuple()
    exponent = decimal_tuple.exponent
    if isinstance(exponent, int):
        n_decimal_places = exponent * -1
        if n_decimal_places <= max_n_places:
            return ValidationResult.valid()
        else:
            return ValidationResult.failed_with(f"{fieldname}: The value has too many decimal places: '{value}'")
    return ValidationResult.failed_with(f"{fieldname}: The value is NaN or infinite: '{value}'")


def validate_two_or_less_decimaal_places(value: Decimal, fieldname: str = "") -> ValidationResult:
    return _validate_n_or_less_decimal_places(max_n_places=2, value=value, fieldname=fieldname)


def validate_zero_decimal_places(value: Decimal, fieldname: str = "") -> ValidationResult:
    return _validate_n_or_less_decimal_places(max_n_places=0, value=value, fieldname=fieldname)


# Parsers


def parse_term_deposit_query(
    *,
    schedule: str,
    rate: str,
    principal: str,
    matures_in_years: str,
) -> TermDepositQuery | ValidationResult:
    """
    Accept a bunch of strings and parse them into a valid query for the term deposit, or raise the result as an error.

    I've arbitrarily decided that we need to have integer number of years, and that the rate has only two decimals.
    """
    _schedule: Schedule
    _rate: Percent
    _principal: Dollars
    _maturity: Years

    error_messages: list[str] = []

    # Not for production. This code reminds us why Pydantic et al end up having
    # field validators, whole model validators, etc. Still, experimental...
    try:
        _schedule = Schedule[schedule]
    except KeyError:
        error_messages.append(f"Not a valid schedule: '{schedule}'")
    try:
        _rate = Percent(rate)
    except InvalidOperation:
        error_messages.extend(f"Not a valid interest rate: '{rate}'")
    else:
        rate_validation = validate_two_or_less_decimaal_places(_rate, "Rate")
        if not rate_validation:
            error_messages.extend(rate_validation.error_messages)
    try:
        _principal = Dollars(principal)
    except InvalidOperation:
        error_messages.extend(f"Not a valid principal: '{principal}'")
    else:
        principal_validation = validate_two_or_less_decimaal_places(_principal, "Principal")
        if not principal_validation:
            error_messages.extend(principal_validation.error_messages)
    try:
        _maturity = Years(matures_in_years)
    except InvalidOperation:
        error_messages.extend(f"Not a valid number of years: '{matures_in_years}'")
    else:
        maturity_validation = validate_zero_decimal_places(_maturity, "Maturity")
        if not maturity_validation:
            error_messages.extend(maturity_validation.error_messages)

    if error_messages:
        raise ValidationResult.failed_with(error_messages)

    # The tooling will tell us that these could be unbound
    # Maybe the experiment is not that
    return TermDepositQuery(_schedule, _rate, _principal, _maturity)
