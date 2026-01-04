"""
Test against user's provided example
CHF 97,500 income, Dübendorf, Roman Catholic
With 98% Cantonal Steuerfuss (user's data)
"""
from models.tax_data import UserProfile
from calculations.federal_tax import calculate_federal_tax
from calculations.cantonal_tax import calculate_zurich_tax
from calculations.church_tax import calculate_church_tax
from utils.formatters import format_currency

print("=" * 80)
print("TEST AGAINST USER'S EXAMPLE")
print("=" * 80)
print("\nTest Case: CHF 97,500 income, Dübendorf, Roman Catholic")
print()

# Setup profile
profile = UserProfile()
profile.marital_status = 'single'
profile.num_children = 0
profile.employment_type = 'employed'
profile.net_salary = 97500
profile.municipality = 'Dübendorf'
profile.gemeinde_steuerfuss = 96  # Dübendorf
profile.religious_affiliation = 'catholic'

# No deductions (gross income test)
deductions = 0

# Calculate taxes with 98% cantonal (override constant)
from models import constants
original_steuerfuss = constants.CANTONAL_STEUERFUSS
constants.CANTONAL_STEUERFUSS = 98  # User's expected value

cant_tax = calculate_zurich_tax(profile.net_salary, profile.gemeinde_steuerfuss, deductions)
church_result = calculate_church_tax(
    cant_tax.einfache_staatssteuer,
    profile.gemeinde_steuerfuss,
    profile.religious_affiliation,
    profile.net_salary
)

# Restore original
constants.CANTONAL_STEUERFUSS = original_steuerfuss

print("USER'S EXPECTED RESULTS:")
print("-" * 80)
print(f"  Einfache Staatssteuer:       CHF 5,981.00")
print(f"  Cantonal (98%):              CHF 5,861.40")
print(f"  Municipal Dübendorf (96%):   CHF 5,741.75")
print(f"  Church Catholic (11%):       CHF 657.90")
print(f"  Personalsteuer:              CHF 24.00")
print(f"  Total Cantonal/Municipal:    CHF 12,285.05")
print()

print("OUR CALCULATED RESULTS:")
print("-" * 80)
print(f"  Einfache Staatssteuer:       {format_currency(cant_tax.einfache_staatssteuer)}")
print(f"  Cantonal (98%):              {format_currency(cant_tax.cantonal_tax)}")
print(f"  Municipal Dübendorf (96%):   {format_currency(cant_tax.municipal_tax)}")
print(f"  Church Catholic (11%):       {format_currency(church_result['church_tax'])}")
print(f"  Personalsteuer:              {format_currency(cant_tax.personalsteuer)}")
total_cantonal_municipal = cant_tax.cantonal_tax + cant_tax.municipal_tax + church_result['church_tax'] + cant_tax.personalsteuer
print(f"  Total Cantonal/Municipal:    {format_currency(total_cantonal_municipal)}")
print()

print("DIFFERENCES:")
print("-" * 80)
einfache_diff = cant_tax.einfache_staatssteuer - 5981.00
cantonal_diff = cant_tax.cantonal_tax - 5861.40
municipal_diff = cant_tax.municipal_tax - 5741.75
church_diff = church_result['church_tax'] - 657.90
personal_diff = cant_tax.personalsteuer - 24.00
total_diff = total_cantonal_municipal - 12285.05

print(f"  Einfache Staatssteuer:       {einfache_diff:+.2f} CHF  {'[OK]' if abs(einfache_diff) < 5 else '[ERROR]'}")
print(f"  Cantonal (98%):              {cantonal_diff:+.2f} CHF  {'[OK]' if abs(cantonal_diff) < 5 else '[ERROR]'}")
print(f"  Municipal (96%):             {municipal_diff:+.2f} CHF  {'[OK]' if abs(municipal_diff) < 5 else '[ERROR]'}")
print(f"  Church (11%):                {church_diff:+.2f} CHF  {'[OK]' if abs(church_diff) < 5 else '[ERROR]'}")
print(f"  Personalsteuer:              {personal_diff:+.2f} CHF  {'[OK]' if abs(personal_diff) < 1 else '[ERROR]'}")
print(f"  Total:                       {total_diff:+.2f} CHF  {'[OK]' if abs(total_diff) < 10 else '[ERROR]'}")
print()

print("DETAILED BRACKET BREAKDOWN:")
print("-" * 80)
# Manual calculation
from models.constants import ZURICH_TAX_BRACKETS

income = 97500
einfache_manual = 0
print(f"Income: CHF {income:,}")
print()

for i, bracket in enumerate(ZURICH_TAX_BRACKETS):
    next_bracket = ZURICH_TAX_BRACKETS[i + 1] if i + 1 < len(ZURICH_TAX_BRACKETS) else None

    if bracket['rate'] == 0:
        continue

    range_start = bracket['threshold']
    range_end = next_bracket['threshold'] if next_bracket else float('inf')

    taxable_amount = 0
    if income > range_start:
        if next_bracket and income >= range_end:
            taxable_amount = range_end - range_start
        elif income > range_start:
            taxable_amount = income - range_start

    tax_paid = (taxable_amount * bracket['rate']) / 100
    einfache_manual += tax_paid

    if taxable_amount > 0:
        print(f"  {format_currency(range_start)} - {format_currency(range_end) if range_end != float('inf') else '∞'}")
        print(f"    Rate: {bracket['rate']:>2}%  |  Taxable: {format_currency(taxable_amount)}  |  Tax: {format_currency(tax_paid)}")

print()
print(f"Total Einfache Staatssteuer (manual): {format_currency(einfache_manual)}")
print()
print("=" * 80)
