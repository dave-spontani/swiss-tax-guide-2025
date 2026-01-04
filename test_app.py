"""
Quick test to verify tax calculations
"""
from models.tax_data import UserProfile, DeductionResult
from calculations.federal_tax import calculate_federal_tax
from calculations.cantonal_tax import calculate_zurich_tax
from calculations.deductions import calculate_automatic_deductions
from utils.formatters import format_currency

# Test case: Single person, CHF 100,000 salary, 2 children
profile = UserProfile()
profile.marital_status = 'single'
profile.num_children = 2
profile.employment_type = 'employed'
profile.net_salary = 100000
profile.commutes_to_work = True
profile.works_away_from_home = True
profile.employer_meal_subsidy = False
profile.municipality = 'Zürich'
profile.gemeinde_steuerfuss = 119

# Calculate automatic deductions
deductions = calculate_automatic_deductions(profile)

print("=" * 60)
print("SWISS TAX CALCULATOR TEST")
print("=" * 60)
print(f"\nIncome: {format_currency(profile.net_salary)}")
print(f"Children: {profile.num_children}")
print("\nAUTOMATIC DEDUCTIONS:")
print(f"  Commuting: {format_currency(deductions.commuting_pauschal)}")
print(f"  Meals: {format_currency(deductions.meal_costs_pauschal)}")
print(f"  Professional: {format_currency(deductions.professional_expenses)}")
print(f"  Children: {format_currency(deductions.child_deductions)}")
print(f"  TOTAL AUTOMATIC: {format_currency(deductions.total_automatic)}")

# Calculate taxes
fed_tax = calculate_federal_tax(profile.net_salary, deductions.total_automatic)
cant_tax = calculate_zurich_tax(profile.net_salary, 119, deductions.total_automatic)

print(f"\nTAXES (after automatic deductions):")
print(f"  Federal Tax: {format_currency(fed_tax.federal_tax)}")
print(f"  Cantonal Tax: {format_currency(cant_tax.cantonal_tax)}")
print(f"  Municipal Tax: {format_currency(cant_tax.municipal_tax)}")
print(f"  Personal Tax: {format_currency(cant_tax.personalsteuer)}")
print(f"  TOTAL TAX: {format_currency(fed_tax.federal_tax + cant_tax.cantonal_tax + cant_tax.municipal_tax + cant_tax.personalsteuer)}")
print(f"\nTaxable Income: {format_currency(fed_tax.taxable_income)}")
print(f"Effective Tax Rate: {fed_tax.total_effective_rate + cant_tax.cantonal_effective_rate:.2f}%")
print("=" * 60)
print("[OK] Test completed successfully!")
print("=" * 60)
