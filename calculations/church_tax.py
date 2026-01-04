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

    Church tax is calculated as a percentage of the Einfache Staatssteuer,
    similar to how cantonal and municipal taxes are calculated.

    Args:
        einfache_staatssteuer: Base simple state tax
        gemeinde_steuerfuss: Municipal tax multiplier (not used for church tax)
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

    # Church tax is based on Einfache Staatssteuer (just like cantonal and municipal taxes)
    # The multiplier represents the Steuerfuss as a decimal (e.g., 0.11 = 11%)
    multiplier = CHURCH_TAX_MULTIPLIERS.get(religious_affiliation, 0)
    church_tax = einfache_staatssteuer * multiplier
    effective_rate = (church_tax / income * 100) if income > 0 else 0

    return {
        'church_tax': church_tax,
        'effective_rate': effective_rate,
        'denomination': religious_affiliation,
        'applied': True
    }
