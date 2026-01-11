"""
Swiss Federal Income Tax Calculation (DBG - Direct Federal Tax)
Based on Art. 36 DBG
"""
from typing import Dict, List
from models.constants import FEDERAL_TAX_BRACKETS, FEDERAL_TAX_BRACKETS_MARRIED
from models.tax_data import TaxResult


def calculate_federal_tax(income: float, deductions: float = 0.0, marital_status: str = 'single') -> TaxResult:
    """
    Calculate Swiss federal income tax (DBG).

    Formula: total_tax = base_tax + (excess_income / 100) × rate_per_hundred

    For married couples, uses married tax brackets (Art. 36 Abs. 2).
    Income should be the combined income of both spouses.

    Args:
        income: Gross annual income (combined for married couples)
        deductions: Total deductions
        marital_status: 'single' or 'married'

    Returns:
        TaxResult with federal tax details
    """
    result = TaxResult()
    result.gross_income = income
    result.total_deductions = deductions

    # Select appropriate brackets based on marital status
    if marital_status == 'married':
        brackets = FEDERAL_TAX_BRACKETS_MARRIED
    else:
        brackets = FEDERAL_TAX_BRACKETS

    # Calculate taxable income
    taxable_income = max(0, income - deductions)
    result.taxable_income = taxable_income

    if taxable_income <= 0:
        return result

    # Find current bracket
    current_bracket_index = 0
    for i in range(len(brackets) - 1, -1, -1):
        if taxable_income >= brackets[i]['threshold']:
            current_bracket_index = i
            break

    current_bracket = brackets[current_bracket_index]
    result.federal_bracket_index = current_bracket_index

    # Calculate total tax using Swiss federal formula
    excess_income = taxable_income - current_bracket['threshold']
    tax_on_excess = (excess_income / 100) * current_bracket['rate_per_hundred']
    federal_tax = current_bracket['base_tax'] + tax_on_excess

    result.federal_tax = federal_tax

    # Calculate effective rate (based on ORIGINAL income, not taxable income)
    if income > 0:
        result.federal_effective_rate = (federal_tax / income) * 100

    # Marginal rate is the rate per hundred at current bracket
    result.federal_marginal_rate = current_bracket['rate_per_hundred']

    # Calculate progress within current bracket
    if current_bracket_index + 1 < len(brackets):
        next_bracket = brackets[current_bracket_index + 1]
        bracket_range = next_bracket['threshold'] - current_bracket['threshold']
        position_in_bracket = taxable_income - current_bracket['threshold']
        result.progress_in_bracket = (position_in_bracket / bracket_range) * 100 if bracket_range > 0 else 0
        result.amount_to_next_bracket = next_bracket['threshold'] - taxable_income
    else:
        result.progress_in_bracket = 100  # At top bracket
        result.amount_to_next_bracket = 0

    # Calculate breakdown for each bracket
    result.federal_breakdown = get_federal_bracket_breakdown(taxable_income, current_bracket_index, brackets)

    return result


def get_federal_bracket_breakdown(income: float, current_bracket_index: int, brackets: List[Dict]) -> List[Dict]:
    """
    Calculate how much tax is paid in each bracket.

    Args:
        income: Taxable income
        current_bracket_index: Index of current tax bracket
        brackets: Tax bracket list (single or married)

    Returns:
        List of dictionaries with bracket breakdown
    """
    breakdown = []

    for i, bracket in enumerate(brackets):
        next_bracket = brackets[i + 1] if i + 1 < len(brackets) else None

        # Skip first bracket if it has 0 rate (tax-free threshold)
        if bracket['rate_per_hundred'] == 0 and i == 0:
            continue

        range_start = bracket['threshold']
        range_end = next_bracket['threshold'] if next_bracket else float('inf')

        # Calculate taxable amount in this bracket
        taxable_amount = 0
        if income > range_start:
            if income >= range_end:
                taxable_amount = range_end - range_start
            else:
                taxable_amount = income - range_start

        # Calculate tax paid in this bracket
        tax_paid = (taxable_amount / 100) * bracket['rate_per_hundred']

        if taxable_amount > 0 or i <= current_bracket_index:
            breakdown.append({
                'bracket_index': i,
                'range_start': range_start,
                'range_end': range_end,
                'rate': bracket['rate_per_hundred'],
                'taxable_amount': taxable_amount,
                'tax_paid': tax_paid,
                'is_active': i == current_bracket_index
            })

    return breakdown
