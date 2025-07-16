import pytest

from ofyourinterest.data import ValidationResult, TermDepositQuery, parse_term_deposit_query


class TestValidationResult:
    def test_cant_be_valid_with_errors(self) -> None:
        with pytest.raises(ValueError):
            # Ensure the incorrect initialisation doesn't trip mypy
            error_messages: tuple[str, ...] = ("lalala",)
            ValidationResult(is_valid=True, error_messages=error_messages)

    def test_cant_be_not_valid_without_errors(self) -> None:
        with pytest.raises(ValueError):
            ValidationResult(is_valid=False)

    def test_can_be_raised(self) -> None:
        with pytest.raises(ValidationResult):
            try:
                raise ValidationResult.failed_with("lala")
            except ValidationResult as r:
                raise r

    def test_invalid_can_be_given_error_or_errors(self) -> None:
        r = ValidationResult.failed_with("Error message")
        s = ValidationResult.failed_with(["Error message"])
        assert r == s


class TestParseDepositQuery:
    def test_parses_valid_without_errors(self) -> None:
        data = {"schedule": "MONTHLY", "rate": "4.35", "principal": "10000", "matures_in_years": "3"}
        query = parse_term_deposit_query(**data)

    def test_parses_invalid_and_raises_with_all_the_errors(self) -> None:
        data = {"schedule": "ANNUAL", "rate": "4.354", "principal": "10000.235", "matures_in_years": "3.5"}
        try:
            parse_term_deposit_query(**data)
        except ValidationResult as result:
            print("HAAHAHAHAHA")
            print(result.error_messages)
            assert result.error_messages == (
                "Not a valid schedule: 'ANNUAL'",
                "Rate: The value has too many decimal places: '4.354'",
                "Principal: The value has too many decimal places: '10000.235'",
                "Maturity: The value has too many decimal places: '3.5'",
            )
