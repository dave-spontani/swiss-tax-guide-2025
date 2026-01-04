"""
Swiss number and currency formatting utilities
"""

def format_currency(amount: float) -> str:
    """
    Format amount as Swiss currency.

    Args:
        amount: The amount to format

    Returns:
        Formatted string like "CHF 100'000.00"

    Examples:
        >>> format_currency(100000)
        "CHF 100'000.00"
        >>> format_currency(1234.56)
        "CHF 1'234.56"
    """
    return f"CHF {amount:,.2f}".replace(',', "'")


def format_number(amount: float) -> str:
    """
    Format number with Swiss thousands separator.

    Args:
        amount: The number to format

    Returns:
        Formatted string like "100'000"

    Examples:
        >>> format_number(100000)
        "100'000"
        >>> format_number(1234.56)
        "1'235"
    """
    return f"{int(amount):,}".replace(',', "'")


def format_percent(rate: float, decimals: int = 2) -> str:
    """
    Format percentage with specified decimal places.

    Args:
        rate: The percentage rate (e.g., 12.345)
        decimals: Number of decimal places (default: 2)

    Returns:
        Formatted string like "12.35%"

    Examples:
        >>> format_percent(12.345)
        "12.35%"
        >>> format_percent(12.345, 1)
        "12.3%"
    """
    return f"{rate:.{decimals}f}%"


def format_rate_per_thousand(rate: float) -> str:
    """
    Format rate per thousand (‰).

    Args:
        rate: The rate per thousand

    Returns:
        Formatted string like "0.5‰"

    Examples:
        >>> format_rate_per_thousand(0.5)
        "0.5‰"
    """
    return f"{rate:.1f}‰"
