"""
Formatting utilities for Swiss Tax Analyzer

Provides consistent formatting for currency, percentages, and numbers.
"""


def format_chf(amount: float, decimals: int = 2, show_symbol: bool = True) -> str:
    """
    Format amount as Swiss Francs

    Args:
        amount: Amount in CHF
        decimals: Number of decimal places
        show_symbol: Whether to show "CHF" symbol

    Returns:
        Formatted string (e.g., "CHF 1,234.56")
    """
    if show_symbol:
        return f"CHF {amount:,.{decimals}f}"
    else:
        return f"{amount:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format value as percentage

    Args:
        value: Value as decimal (e.g., 0.15 for 15%)
        decimals: Number of decimal places

    Returns:
        Formatted string (e.g., "15.00%")
    """
    return f"{value:.{decimals}f}%"


def format_number(value: float, decimals: int = 0) -> str:
    """
    Format number with thousands separator

    Args:
        value: Numeric value
        decimals: Number of decimal places

    Returns:
        Formatted string (e.g., "1,234")
    """
    return f"{value:,.{decimals}f}"


def format_chf_compact(amount: float) -> str:
    """
    Format CHF in compact form for large numbers

    Args:
        amount: Amount in CHF

    Returns:
        Formatted string (e.g., "1.2M", "150K")
    """
    if abs(amount) >= 1_000_000:
        return f"CHF {amount / 1_000_000:.1f}M"
    elif abs(amount) >= 1_000:
        return f"CHF {amount / 1_000:.0f}K"
    else:
        return format_chf(amount, decimals=0)


def format_tax_rate_badge(rate: float) -> str:
    """
    Format tax rate for badge display

    Args:
        rate: Tax rate as percentage

    Returns:
        Formatted string
    """
    if rate < 15:
        return f"⬇️ {rate:.1f}%"
    elif rate < 25:
        return f"➡️ {rate:.1f}%"
    else:
        return f"⬆️ {rate:.1f}%"


def format_savings(amount: float) -> str:
    """
    Format savings amount with positive indicator

    Args:
        amount: Savings amount

    Returns:
        Formatted string with indicator
    """
    if amount > 0:
        return f"💰 {format_chf(amount)}"
    else:
        return f"{format_chf(amount)}"
