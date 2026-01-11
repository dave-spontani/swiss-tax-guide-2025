"""
Zurich Cantonal Tax Calculation
Based on StG § 35 (adjusted for 2024)
"""
from typing import Dict, List
from models.constants import ZURICH_TAX_BRACKETS, ZURICH_TAX_BRACKETS_MARRIED, CANTONAL_STEUERFUSS, PERSONALSTEUER
from models.tax_data import TaxResult


def calculate_zurich_tax(income: float, gemeinde_steuerfuss: int = 119, deductions: float = 0.0, marital_status: str = 'single') -> TaxResult:
    """
    Calculate Zurich cantonal and municipal taxes.

    The system works in two steps:
    1. Calculate "Einfache Staatssteuer" (simple state tax) using progressive brackets
    2. Apply tax multipliers (Steuerfüsse) to get actual cantonal and municipal taxes

    For married couples, uses married tax brackets (StG § 35 Abs. 2).
    Income should be the combined income of both spouses.

    Args:
        income: Gross annual income (combined for married couples)
        gemeinde_steuerfuss: Municipal tax multiplier (e.g., 119 for Zürich)
        deductions: Total deductions
        marital_status: 'single' or 'married'

    Returns:
        TaxResult with cantonal tax details
    """
    result = TaxResult()
    result.gross_income = income
    result.total_deductions = deductions

    # Select appropriate brackets based on marital status
    if marital_status == 'married':
        brackets = ZURICH_TAX_BRACKETS_MARRIED
    else:
        brackets = ZURICH_TAX_BRACKETS

    # Calculate taxable income
    taxable_income = max(0, income - deductions)
    result.taxable_income = taxable_income

    if taxable_income <= 0:
        return result

    # Step 1: Calculate Einfache Staatssteuer (simple state tax)
    einfache_staatssteuer = 0
    current_bracket_index = 0
    breakdown = []

    for i, bracket in enumerate(brackets):
        next_bracket = brackets[i + 1] if i + 1 < len(brackets) else None

        if taxable_income > bracket['threshold']:
            current_bracket_index = i

        # Skip the first (0%) bracket for breakdown display
        if bracket['rate'] == 0:
            continue

        range_start = bracket['threshold']
        range_end = next_bracket['threshold'] if next_bracket else float('inf')

        # Calculate taxable amount in this bracket
        taxable_amount = 0
        if taxable_income > range_start:
            if next_bracket and taxable_income >= range_end:
                taxable_amount = range_end - range_start
            elif taxable_income > range_start:
                taxable_amount = taxable_income - range_start

        # Calculate tax for this bracket
        tax_paid = (taxable_amount * bracket['rate']) / 100
        einfache_staatssteuer += tax_paid

        if taxable_amount > 0:
            breakdown.append({
                'bracket_index': i,
                'range_start': range_start,
                'range_end': range_end,
                'rate': bracket['rate'],
                'taxable_amount': taxable_amount,
                'tax_paid': tax_paid,
                'is_active': i == current_bracket_index
            })

    result.einfache_staatssteuer = einfache_staatssteuer
    result.cantonal_breakdown = breakdown

    # Step 2: Apply Steuerfüsse (tax multipliers)
    result.cantonal_tax = (einfache_staatssteuer * CANTONAL_STEUERFUSS) / 100
    result.municipal_tax = (einfache_staatssteuer * gemeinde_steuerfuss) / 100

    # Step 3: Add Personalsteuer (flat CHF 24 personal tax)
    result.personalsteuer = PERSONALSTEUER if taxable_income > 0 else 0

    result.total_cantonal_municipal = result.cantonal_tax + result.municipal_tax

    # Calculate effective rate (based on ORIGINAL income, not taxable income)
    if income > 0:
        result.cantonal_effective_rate = (result.total_cantonal_municipal / income) * 100

    # Get current bracket info
    current_bracket = brackets[current_bracket_index]
    result.cantonal_bracket_index = current_bracket_index
    result.cantonal_marginal_rate = current_bracket['rate']

    # Calculate progress within current bracket
    if current_bracket_index + 1 < len(brackets):
        next_bracket = brackets[current_bracket_index + 1]
        bracket_range = next_bracket['threshold'] - current_bracket['threshold']
        position_in_bracket = taxable_income - current_bracket['threshold']
        result.progress_in_bracket = (position_in_bracket / bracket_range) * 100 if bracket_range > 0 else 0
        result.amount_to_next_bracket = next_bracket['threshold'] - taxable_income
    else:
        result.progress_in_bracket = 100
        result.amount_to_next_bracket = 0

    return result


def get_cantonal_bracket_breakdown(income: float, gemeinde_steuerfuss: int = 119) -> List[Dict]:
    """
    Get detailed breakdown of Zurich cantonal tax by bracket.

    Args:
        income: Taxable income
        gemeinde_steuerfuss: Municipal tax multiplier

    Returns:
        List of dictionaries with bracket breakdown
    """
    breakdown = []
    current_bracket_index = 0

    for i, bracket in enumerate(ZURICH_TAX_BRACKETS):
        next_bracket = ZURICH_TAX_BRACKETS[i + 1] if i + 1 < len(ZURICH_TAX_BRACKETS) else None

        if income > bracket['threshold']:
            current_bracket_index = i

        # Skip 0% bracket
        if bracket['rate'] == 0:
            continue

        range_start = bracket['threshold']
        range_end = next_bracket['threshold'] if next_bracket else float('inf')

        # Calculate taxable amount in this bracket
        taxable_amount = 0
        if income > range_start:
            if next_bracket and income >= range_end:
                taxable_amount = range_end - range_start
            elif income > range_start:
                taxable_amount = income - range_start

        # Calculate einfache tax for this bracket
        einfache_tax_paid = (taxable_amount * bracket['rate']) / 100

        # Calculate actual cantonal and municipal tax
        cantonal_tax = (einfache_tax_paid * CANTONAL_STEUERFUSS) / 100
        municipal_tax = (einfache_tax_paid * gemeinde_steuerfuss) / 100

        if taxable_amount > 0:
            breakdown.append({
                'bracket_index': i,
                'range_start': range_start,
                'range_end': range_end,
                'rate': bracket['rate'],
                'taxable_amount': taxable_amount,
                'einfache_tax_paid': einfache_tax_paid,
                'cantonal_tax': cantonal_tax,
                'municipal_tax': municipal_tax,
                'total_tax': cantonal_tax + municipal_tax,
                'is_active': i == current_bracket_index
            })

    return breakdown
