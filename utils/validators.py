"""
Input validation utilities for Swiss Tax Analyzer
"""


def validate_positive_number(value: float, field_name: str = "Value") -> tuple[bool, str]:
    """
    Validate that a number is positive

    Args:
        value: Value to validate
        field_name: Name of the field for error message

    Returns:
        Tuple of (is_valid, error_message)
    """
    if value < 0:
        return False, f"{field_name} must be non-negative"
    return True, ""


def validate_percentage(value: float, field_name: str = "Percentage") -> tuple[bool, str]:
    """
    Validate that a percentage is between 0 and 100

    Args:
        value: Percentage value to validate
        field_name: Name of the field for error message

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not 0 <= value <= 100:
        return False, f"{field_name} must be between 0 and 100"
    return True, ""


def validate_salary(salary: float) -> tuple[bool, str]:
    """
    Validate salary input

    Args:
        salary: Annual salary

    Returns:
        Tuple of (is_valid, error_message)
    """
    if salary < 0:
        return False, "Salary cannot be negative"

    if salary > 10_000_000:
        return False, "Salary seems unreasonably high (> CHF 10M)"

    if 0 < salary < 10_000:
        return False, "Salary seems too low for annual amount (< CHF 10,000)"

    return True, ""


def validate_deduction_amount(amount: float, max_amount: float, deduction_name: str) -> tuple[bool, str]:
    """
    Validate deduction amount against maximum

    Args:
        amount: Deduction amount
        max_amount: Maximum allowed deduction
        deduction_name: Name of the deduction

    Returns:
        Tuple of (is_valid, error_message)
    """
    if amount < 0:
        return False, f"{deduction_name} cannot be negative"

    if amount > max_amount:
        return False, f"{deduction_name} exceeds maximum of CHF {max_amount:,.2f}"

    return True, ""
