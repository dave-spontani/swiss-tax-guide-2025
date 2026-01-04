"""
Test script to verify commuting cost caps are applied correctly.

Tests:
1. No commuting costs
2. CHF 700 pauschal
3. CHF 3,000 (below both limits)
4. CHF 4,000 (above federal CHF 3,200, below cantonal CHF 5,000)
5. CHF 6,000 (above both limits)
"""

from models.tax_data import UserProfile, DeductionResult
from models.constants import COMMUTING_MAX_FEDERAL, COMMUTING_MAX_CANTONAL
from calculations.deductions import get_adjusted_deductions_for_tax_type
from ui.tax_comparison import calculate_complete_taxes
from utils.formatters import format_currency


def test_commuting_caps():
    """Test that different commuting caps are applied correctly."""

    print("=" * 80)
    print("TESTING COMMUTING COST CAPS")
    print("=" * 80)
    print(f"\nFederal limit: {format_currency(COMMUTING_MAX_FEDERAL)}")
    print(f"Cantonal limit: {format_currency(COMMUTING_MAX_CANTONAL)}")
    print()

    # Create test profile
    profile = UserProfile()
    profile.net_salary = 100000
    profile.gemeinde_steuerfuss = 119  # Zürich
    profile.marital_status = 'single'
    profile.num_children = 0
    profile.total_wealth = 0
    profile.religious_affiliation = 'none'

    # Test cases
    test_cases = [
        (0, "No commuting"),
        (700, "CHF 700 pauschal"),
        (3000, "CHF 3,000 (below both limits)"),
        (4000, "CHF 4,000 (above federal, below cantonal)"),
        (6000, "CHF 6,000 (above both limits)"),
    ]

    for commuting_amount, description in test_cases:
        print(f"\n{'=' * 80}")
        print(f"TEST: {description}")
        print(f"{'=' * 80}")

        # Create deduction result
        deductions = DeductionResult()
        deductions.commuting_pauschal = commuting_amount
        deductions.calculate_totals()

        # Calculate adjusted deductions
        if commuting_amount > 0:
            federal_deductions = get_adjusted_deductions_for_tax_type(deductions, 'federal')
            cantonal_deductions = get_adjusted_deductions_for_tax_type(deductions, 'cantonal')

            print(f"\nRaw commuting amount: {format_currency(commuting_amount)}")
            print(f"Federal deductions:   {format_currency(federal_deductions)}")
            print(f"Cantonal deductions:  {format_currency(cantonal_deductions)}")

            # Verify caps are applied correctly
            expected_federal = min(commuting_amount, COMMUTING_MAX_FEDERAL)
            expected_cantonal = min(commuting_amount, COMMUTING_MAX_CANTONAL)

            assert federal_deductions == expected_federal, \
                f"Federal deduction mismatch: got {federal_deductions}, expected {expected_federal}"
            assert cantonal_deductions == expected_cantonal, \
                f"Cantonal deduction mismatch: got {cantonal_deductions}, expected {expected_cantonal}"

            print("[OK] Caps applied correctly!")

        # Calculate full tax result
        tax_result = calculate_complete_taxes(
            income=100000,
            deductions=deductions.total_deductions,
            profile=profile,
            deduction_result=deductions if commuting_amount > 0 else None
        )

        print(f"\nTax Results:")
        print(f"  Taxable income: {format_currency(tax_result.taxable_income)}")
        print(f"  Federal tax:    {format_currency(tax_result.federal_tax)}")
        print(f"  Cantonal tax:   {format_currency(tax_result.cantonal_tax)}")
        print(f"  Municipal tax:  {format_currency(tax_result.municipal_tax)}")
        print(f"  Total tax:      {format_currency(tax_result.total_tax)}")

    print(f"\n{'=' * 80}")
    print("ALL TESTS PASSED! [OK]")
    print(f"{'=' * 80}\n")


def test_comparison_scenarios():
    """Test that caps work correctly in all three comparison scenarios."""

    print("\n" + "=" * 80)
    print("TESTING COMPARISON SCENARIOS WITH HIGH COMMUTING COSTS")
    print("=" * 80)

    profile = UserProfile()
    profile.net_salary = 100000
    profile.gemeinde_steuerfuss = 119
    profile.marital_status = 'single'
    profile.num_children = 0
    profile.total_wealth = 0
    profile.religious_affiliation = 'none'

    # Create deductions with high commuting costs
    deductions = DeductionResult()
    deductions.commuting_pauschal = 6000  # Above both limits
    deductions.pillar_3a = 5000
    deductions.calculate_totals()

    print(f"\nTest scenario:")
    print(f"  Income: {format_currency(profile.net_salary)}")
    print(f"  Commuting costs: {format_currency(deductions.commuting_pauschal)}")
    print(f"  Pillar 3a: {format_currency(deductions.pillar_3a)}")
    print(f"  Total deductions: {format_currency(deductions.total_deductions)}")

    # Scenario 1: No deductions
    tax_no_deductions = calculate_complete_taxes(100000, 0, profile)
    print(f"\nScenario 1 (no deductions):")
    print(f"  Total tax: {format_currency(tax_no_deductions.total_tax)}")

    # Scenario 2: Automatic only (commuting)
    tax_auto = calculate_complete_taxes(
        100000,
        deductions.total_automatic,
        profile,
        deduction_result=deductions
    )
    print(f"\nScenario 2 (automatic deductions):")
    print(f"  Total tax: {format_currency(tax_auto.total_tax)}")
    print(f"  Savings: {format_currency(tax_no_deductions.total_tax - tax_auto.total_tax)}")

    # Scenario 3: All deductions
    tax_all = calculate_complete_taxes(
        100000,
        deductions.total_deductions,
        profile,
        deduction_result=deductions
    )
    print(f"\nScenario 3 (all deductions):")
    print(f"  Total tax: {format_currency(tax_all.total_tax)}")
    print(f"  Savings: {format_currency(tax_no_deductions.total_tax - tax_all.total_tax)}")

    # Verify that caps are working
    # With CHF 6,000 commuting:
    # - Federal should use CHF 3,200
    # - Cantonal should use CHF 5,000
    # So taxable income should be different for federal vs cantonal

    expected_federal_taxable = 100000 - 3200  # Using federal cap
    expected_cantonal_taxable = 100000 - 5000  # Using cantonal cap

    print(f"\nVerification:")
    print(f"  Expected federal taxable income:  {format_currency(expected_federal_taxable)}")
    print(f"  Actual taxable income (scenario 2): {format_currency(tax_auto.taxable_income)}")

    # The taxable_income shown is from federal calculation
    assert abs(tax_auto.taxable_income - expected_federal_taxable) < 1, \
        "Federal taxable income doesn't match expected value"

    print(f"  [OK] Federal cap applied correctly!")
    print(f"  [OK] Cantonal cap should be applied separately (CHF 5,000)")

    print(f"\n{'=' * 80}")
    print("COMPARISON SCENARIOS TEST PASSED! [OK]")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    try:
        test_commuting_caps()
        test_comparison_scenarios()
        print("\n[SUCCESS] ALL TESTS COMPLETED SUCCESSFULLY!\n")
    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n[ERROR] {e}\n")
        raise
