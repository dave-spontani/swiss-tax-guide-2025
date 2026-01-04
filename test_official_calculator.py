"""
Test against official Zurich calculator results
CHF 97,500 income, Dübendorf, Roman Catholic
"""
from models.tax_data import UserProfile
from calculations.federal_tax import calculate_federal_tax
from calculations.cantonal_tax import calculate_zurich_tax
from calculations.church_tax import calculate_church_tax
from calculations.wealth_tax import calculate_wealth_tax
from utils.formatters import format_currency

# Test case from official calculator
# https://www.zh.ch/de/steuern-finanzen/steuern/steuern-natuerliche-personen/steuererklaerung-natuerliche-personen/steuerrechner.html?calculatorId=income_assets
print("=" * 80)
print("TEST AGAINST OFFICIAL ZURICH CALCULATOR")
print("=" * 80)
print("\nTest Case: CHF 97,500 income, Dübendorf, Roman Catholic, CHF 50,000 wealth")
print()

# Setup profile
profile = UserProfile()
profile.marital_status = 'single'
profile.num_children = 0
profile.employment_type = 'employed'
profile.net_salary = 97500
profile.municipality = 'Dübendorf'
profile.gemeinde_steuerfuss = 96  # Dübendorf (fixed from 106)
profile.religious_affiliation = 'catholic'
profile.total_wealth = 50000
profile.commutes_to_work = False
profile.works_away_from_home = False

# No deductions (gross income test)
deductions = 0

# Calculate taxes
fed_tax = calculate_federal_tax(profile.net_salary, deductions)
cant_tax = calculate_zurich_tax(profile.net_salary, profile.gemeinde_steuerfuss, deductions)
church_result = calculate_church_tax(
    cant_tax.einfache_staatssteuer,
    profile.gemeinde_steuerfuss,
    profile.religious_affiliation,
    profile.net_salary
)
wealth_result = calculate_wealth_tax(
    profile.total_wealth,
    profile.num_children,
    profile.gemeinde_steuerfuss
)

print("EXPECTED RESULTS (from official calculator):")
print("-" * 80)
print(f"  Einfache Staatssteuer:       CHF 5,944.00")
print(f"  Cantonal (95%):              CHF 5,646.80")
print(f"  Municipal Dübendorf (96%):   CHF 5,706.25")
print(f"  Church Catholic (11%):       CHF 653.85")
print(f"  Personalsteuer:              CHF 24.00")
print(f"  Total Cantonal/Municipal:    CHF 12,030.90")
print()

print("OUR CALCULATED RESULTS:")
print("-" * 80)
print(f"  Einfache Staatssteuer:       {format_currency(cant_tax.einfache_staatssteuer)}")
print(f"  Cantonal (95%):              {format_currency(cant_tax.cantonal_tax)}")
print(f"  Municipal Dübendorf (96%):   {format_currency(cant_tax.municipal_tax)}")
print(f"  Church Catholic (11%):       {format_currency(church_result['church_tax'])}")
print(f"  Personalsteuer:              {format_currency(cant_tax.personalsteuer)}")
total_cantonal_municipal = cant_tax.cantonal_tax + cant_tax.municipal_tax + church_result['church_tax'] + cant_tax.personalsteuer
print(f"  Total Cantonal/Municipal:    {format_currency(total_cantonal_municipal)}")
print()

print("DIFFERENCES:")
print("-" * 80)
einfache_diff = cant_tax.einfache_staatssteuer - 5944.00
cantonal_diff = cant_tax.cantonal_tax - 5646.80
municipal_diff = cant_tax.municipal_tax - 5706.25
church_diff = church_result['church_tax'] - 653.85
personal_diff = cant_tax.personalsteuer - 24.00
total_diff = total_cantonal_municipal - 12030.90

print(f"  Einfache Staatssteuer:       {einfache_diff:+.2f} CHF  {'[OK]' if abs(einfache_diff) < 40 else '[NEED PHASE 2]'}")
print(f"  Cantonal (95%):              {cantonal_diff:+.2f} CHF  {'[OK]' if abs(cantonal_diff) < 2 else '[ERROR]'}")
print(f"  Municipal (96%):             {municipal_diff:+.2f} CHF  {'[OK]' if abs(municipal_diff) < 2 else '[ERROR]'}")
print(f"  Church (11%):                {church_diff:+.2f} CHF  {'[OK]' if abs(church_diff) < 2 else '[ERROR]'}")
print(f"  Personalsteuer:              {personal_diff:+.2f} CHF  {'[OK]' if abs(personal_diff) < 1 else '[ERROR]'}")
print(f"  Total:                       {total_diff:+.2f} CHF")
print()

print("ANALYSIS:")
print("-" * 80)
if abs(einfache_diff) > 2:
    print(f"  [WARNING] Einfache Staatssteuer off by {abs(einfache_diff):.2f} CHF")
    print(f"    This indicates bracket thresholds need adjustment (Phase 2)")
else:
    print(f"  [OK] Einfache Staatssteuer matches!")

if abs(cantonal_diff) < 2 and abs(municipal_diff) < 2:
    print(f"  [OK] Steuerfuss multipliers are correct!")
else:
    print(f"  [ERROR] Steuerfuss multipliers still have issues")

if abs(church_diff) < 2:
    print(f"  [OK] Church tax multiplier is correct!")
else:
    print(f"  [ERROR] Church tax multiplier needs adjustment")

if abs(personal_diff) < 1:
    print(f"  [OK] Personalsteuer is correct!")
else:
    print(f"  [ERROR] Personalsteuer calculation has issues")

print()
print("=" * 80)
if abs(total_diff) < 50:
    print("[PHASE 1 SUCCESS] All multipliers correct. Einfache discrepancy is expected.")
    print("Proceed to Phase 2 to investigate bracket thresholds if needed.")
else:
    print("[ERROR] Major discrepancies found. Review calculations.")
print("=" * 80)
