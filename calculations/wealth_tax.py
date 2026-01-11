"""
Wealth Tax Calculation for Zurich Canton
"""
from models.constants import (
    WEALTH_TAX_BRACKETS_SINGLE,
    WEALTH_TAX_BRACKETS_MARRIED,
    WEALTH_DEDUCTION_PER_CHILD,
    CANTONAL_STEUERFUSS
)


def calculate_wealth_tax(
    total_wealth: float,
    number_of_children: int,
    gemeinde_steuerfuss: int,
    marital_status: str = 'single'
) -> dict:
    """
    Calculate wealth tax for Zurich canton.

    Note: In Zurich, there are NO per-adult deductions. Instead:
    - Singles use WEALTH_TAX_BRACKETS_SINGLE (threshold: CHF 80,000)
    - Married use WEALTH_TAX_BRACKETS_MARRIED (threshold: CHF 159,000)
    - Both can deduct CHF 41,100 per child

    Process:
    1. Select appropriate brackets based on marital status
    2. Calculate deductions (CHF 41,100 per child only)
    3. Calculate taxable wealth
    4. Calculate "einfache" wealth tax using progressive brackets (rates in ‰)
    5. Apply cantonal and municipal Steuerfüsse

    Args:
        total_wealth: Total assets minus liabilities
        number_of_children: Number of children
        gemeinde_steuerfuss: Municipal tax multiplier
        marital_status: 'single' or 'married'

    Returns:
        Dictionary with wealth tax details
    """
    if total_wealth <= 0:
        return {
            'taxable_wealth': 0.0,
            'wealth_tax': 0.0,
            'cantonal_wealth_tax': 0.0,
            'municipal_wealth_tax': 0.0,
            'effective_rate': 0.0,
            'deductions': 0.0
        }

    # Select appropriate brackets
    if marital_status == 'married':
        brackets = WEALTH_TAX_BRACKETS_MARRIED
    else:
        brackets = WEALTH_TAX_BRACKETS_SINGLE

    # Calculate deductions (ONLY for children, no per-adult deductions)
    deductions = number_of_children * WEALTH_DEDUCTION_PER_CHILD
    taxable_wealth = max(0, total_wealth - deductions)

    if taxable_wealth == 0:
        return {
            'taxable_wealth': 0.0,
            'wealth_tax': 0.0,
            'cantonal_wealth_tax': 0.0,
            'municipal_wealth_tax': 0.0,
            'effective_rate': 0.0,
            'deductions': deductions
        }

    # Calculate "einfache" wealth tax using progressive brackets
    einfache_wealth_tax = 0

    for i, bracket in enumerate(brackets):
        next_bracket = brackets[i + 1] if i + 1 < len(brackets) else None

        if taxable_wealth <= bracket['threshold']:
            break

        taxable_in_bracket = (
            min(taxable_wealth, next_bracket['threshold']) - bracket['threshold']
            if next_bracket
            else taxable_wealth - bracket['threshold']
        )

        einfache_wealth_tax += (taxable_in_bracket / 1000) * bracket['rate_per_thousand']

    # Apply Steuerfüsse
    cantonal_wealth_tax = (einfache_wealth_tax * CANTONAL_STEUERFUSS) / 100
    municipal_wealth_tax = (einfache_wealth_tax * gemeinde_steuerfuss) / 100
    wealth_tax = cantonal_wealth_tax + municipal_wealth_tax

    effective_rate = (wealth_tax / total_wealth * 100) if total_wealth > 0 else 0

    return {
        'taxable_wealth': taxable_wealth,
        'wealth_tax': wealth_tax,
        'cantonal_wealth_tax': cantonal_wealth_tax,
        'municipal_wealth_tax': municipal_wealth_tax,
        'effective_rate': effective_rate,
        'deductions': deductions,
        'einfache_wealth_tax': einfache_wealth_tax
    }
