import pytest

from ofyourinterest.data import ValidationResult


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
