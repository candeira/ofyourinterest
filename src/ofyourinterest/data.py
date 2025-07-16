from decimal import Decimal
from dataclasses import dataclass
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


# Validators/parsers would normally go in a different file, but for expediency...
# Parsers called `parse_` are validators that return a value or a ValidationError.
# Validators called `validate` return a ValidationResult alse and are used by the parsers
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
