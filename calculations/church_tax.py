"""
Church Tax Calculation for Zurich Canton
"""
from models.constants import CHURCH_TAX_MULTIPLIERS, CANTONAL_STEUERFUSS


def calculate_church_tax(
    einfache_staatssteuer: float,
    gemeinde_steuerfuss: int,
    religious_affiliation: str,
    income: float
) -> dict:
    """
    Calculate church tax for Zurich canton.

    Church tax is calculated as a percentage of the total cantonal + municipal tax.

    Args:
        einfache_staatssteuer: Base simple state tax
        gemeinde_steuerfuss: Municipal tax multiplier
        religious_affiliation: 'none', 'reformed', 'catholic', 'christian-catholic'
        income: Gross income (for effective rate calculation)

    Returns:
        Dictionary with church tax details
    """
    if religious_affiliation == 'none' or income <= 0:
        return {
            'church_tax': 0.0,
            'effective_rate': 0.0,
            'denomination': religious_affiliation,
            'applied': False
        }

    # Church tax is based on total cantonal + municipal tax
    total_cantonal_municipal_tax = (
        (einfache_staatssteuer * CANTONAL_STEUERFUSS / 100) +
        (einfache_staatssteuer * gemeinde_steuerfuss / 100)
    )

    multiplier = CHURCH_TAX_MULTIPLIERS.get(religious_affiliation, 0)
    church_tax = total_cantonal_municipal_tax * multiplier
    effective_rate = (church_tax / income * 100) if income > 0 else 0

    return {
        'church_tax': church_tax,
        'effective_rate': effective_rate,
        'denomination': religious_affiliation,
        'applied': True
    }
