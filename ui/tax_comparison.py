"""
3-Level Tax Comparison Display
Shows taxes before any deductions, after automatic, and after all deductions
"""
import streamlit as st
import pandas as pd
from models.tax_data import TaxResult, ComparisonResult, DeductionResult, UserProfile
from calculations.federal_tax import calculate_federal_tax
from calculations.cantonal_tax import calculate_zurich_tax
from calculations.church_tax import calculate_church_tax
from calculations.wealth_tax import calculate_wealth_tax
from calculations.deductions import get_adjusted_deductions_for_tax_type
from utils.formatters import format_currency, format_percent


def calculate_complete_taxes(income: float, deductions: float, profile: UserProfile,
                            deduction_result: DeductionResult = None) -> TaxResult:
    """
    Calculate all taxes for a given income and deductions.

    Args:
        income: Gross income
        deductions: Total deductions (used for display purposes)
        profile: User profile
        deduction_result: Optional DeductionResult object for applying different caps
                         for federal vs cantonal commuting costs

    Returns:
        TaxResult with all taxes calculated
    """
    result = TaxResult()
    result.gross_income = income
    result.total_deductions = deductions

    # Calculate adjusted deductions for federal vs cantonal if deduction_result provided
    if deduction_result is not None:
        federal_deductions = get_adjusted_deductions_for_tax_type(
            deduction_result, 'federal', total_to_adjust=deductions
        )
        cantonal_deductions = get_adjusted_deductions_for_tax_type(
            deduction_result, 'cantonal', total_to_adjust=deductions
        )
    else:
        # Use same deductions for both (e.g., when deductions=0)
        federal_deductions = deductions
        cantonal_deductions = deductions

    # Federal tax (with federal commuting cap: CHF 3,200)
    fed_result = calculate_federal_tax(income, federal_deductions, profile.marital_status)
    result.federal_tax = fed_result.federal_tax
    result.federal_effective_rate = fed_result.federal_effective_rate
    result.federal_marginal_rate = fed_result.federal_marginal_rate
    result.federal_bracket_index = fed_result.federal_bracket_index
    result.federal_breakdown = fed_result.federal_breakdown
    result.taxable_income = fed_result.taxable_income

    # Cantonal tax (with cantonal commuting cap: CHF 5,000)
    cant_result = calculate_zurich_tax(income, profile.gemeinde_steuerfuss, cantonal_deductions, profile.marital_status)
    result.einfache_staatssteuer = cant_result.einfache_staatssteuer
    result.cantonal_tax = cant_result.cantonal_tax
    result.municipal_tax = cant_result.municipal_tax
    result.personalsteuer = cant_result.personalsteuer
    result.total_cantonal_municipal = cant_result.total_cantonal_municipal
    result.cantonal_effective_rate = cant_result.cantonal_effective_rate
    result.cantonal_marginal_rate = cant_result.cantonal_marginal_rate
    result.cantonal_bracket_index = cant_result.cantonal_bracket_index
    result.cantonal_breakdown = cant_result.cantonal_breakdown
    result.progress_in_bracket = cant_result.progress_in_bracket
    result.amount_to_next_bracket = cant_result.amount_to_next_bracket

    # Church tax
    church_result = calculate_church_tax(
        result.einfache_staatssteuer,
        profile.gemeinde_steuerfuss,
        profile.religious_affiliation,
        income
    )
    result.church_tax = church_result['church_tax']
    result.church_effective_rate = church_result['effective_rate']

    # Wealth tax
    if profile.total_wealth > 0:
        wealth_result = calculate_wealth_tax(
            profile.total_wealth,
            profile.num_children,
            profile.gemeinde_steuerfuss,
            profile.marital_status
        )
        result.wealth_tax = wealth_result['wealth_tax']
        result.wealth_effective_rate = wealth_result['effective_rate']

    # Calculate totals
    result.calculate_totals()

    return result


def render_tax_comparison(profile: UserProfile, deductions: DeductionResult):
    """Render 3-level tax comparison."""
    st.header("Your Tax Calculation Results")

    # Calculate combined income for married couples
    if profile.marital_status == 'married':
        income = profile.spouse1_net_salary + profile.spouse2_net_salary
        st.caption(f"Combined income (Person 1: {format_currency(profile.spouse1_net_salary)} + Person 2: {format_currency(profile.spouse2_net_salary)})")
    else:
        income = profile.net_salary

    # Calculate three scenarios
    # Scenario 1: No deductions (no need to pass deduction_result)
    tax_no_deductions = calculate_complete_taxes(income, 0, profile)

    # Scenario 2: Automatic deductions only (pass deduction_result for commuting caps)
    tax_auto_deductions = calculate_complete_taxes(
        income,
        deductions.total_automatic,
        profile,
        deduction_result=deductions
    )

    # Scenario 3: All deductions (pass deduction_result for commuting caps)
    tax_all_deductions = calculate_complete_taxes(
        income,
        deductions.total_deductions,
        profile,
        deduction_result=deductions
    )

    # Create comparison
    comparison = ComparisonResult()
    comparison.gross_income = income
    comparison.tax_before_deductions = tax_no_deductions
    comparison.automatic_deductions = deductions.total_automatic
    comparison.tax_after_automatic = tax_auto_deductions
    comparison.total_deductions = deductions.total_deductions
    comparison.tax_after_all_deductions = tax_all_deductions
    comparison.calculate_savings()

    # Display 3-level comparison
    st.subheader("Tax Comparison")

    col1, col2, col3 = st.columns(3)

    # Scenario 1: Before ANY deductions
    with col1:
        with st.container(border=True):
            st.markdown("### 1️⃣ Before Deductions")
            st.metric("Gross Income", format_currency(income))
            st.metric("Federal Tax", format_currency(tax_no_deductions.federal_tax))
            st.metric("Cantonal Tax", format_currency(tax_no_deductions.cantonal_tax))
            st.metric("Municipal Tax", format_currency(tax_no_deductions.municipal_tax))
            if tax_no_deductions.personalsteuer > 0:
                st.metric("Personal Tax", format_currency(tax_no_deductions.personalsteuer))
            if tax_no_deductions.church_tax > 0:
                st.metric("Church Tax", format_currency(tax_no_deductions.church_tax))
            if tax_no_deductions.wealth_tax > 0:
                st.metric("Wealth Tax", format_currency(tax_no_deductions.wealth_tax))
            st.divider()
            st.metric("TOTAL ZH TAX", format_currency(tax_no_deductions.total_tax))
            st.caption(f"Effective Rate: {format_percent(tax_no_deductions.total_effective_rate)}")
            st.caption("(Federal tax paid separately)")

    # Scenario 2: After AUTOMATIC deductions
    with col2:
        with st.container(border=True):
            st.markdown("### 2️⃣ After Automatic")
            st.info(f"Deductions: {format_currency(deductions.total_automatic)}")
            st.metric("Taxable Income", format_currency(tax_auto_deductions.taxable_income))
            st.metric("Federal Tax", format_currency(tax_auto_deductions.federal_tax),
                     delta=f"-{format_percent((tax_no_deductions.federal_tax - tax_auto_deductions.federal_tax) / tax_no_deductions.federal_tax * 100)}")
            st.metric("Cantonal Tax", format_currency(tax_auto_deductions.cantonal_tax))
            st.metric("Municipal Tax", format_currency(tax_auto_deductions.municipal_tax))
            if tax_auto_deductions.personalsteuer > 0:
                st.metric("Personal Tax", format_currency(tax_auto_deductions.personalsteuer))
            if tax_auto_deductions.church_tax > 0:
                st.metric("Church Tax", format_currency(tax_auto_deductions.church_tax))
            if tax_auto_deductions.wealth_tax > 0:
                st.metric("Wealth Tax", format_currency(tax_auto_deductions.wealth_tax))
            st.divider()
            st.metric("TOTAL ZH TAX", format_currency(tax_auto_deductions.total_tax))
            st.success(f"💰 Save: {format_currency(comparison.savings_from_automatic)}")

    # Scenario 3: After ALL deductions
    with col3:
        with st.container(border=True):
            st.markdown("### 3️⃣ After All")
            st.info(f"Deductions: {format_currency(deductions.total_deductions)}")
            st.metric("Taxable Income", format_currency(tax_all_deductions.taxable_income))
            st.metric("Federal Tax", format_currency(tax_all_deductions.federal_tax))
            st.metric("Cantonal Tax", format_currency(tax_all_deductions.cantonal_tax))
            st.metric("Municipal Tax", format_currency(tax_all_deductions.municipal_tax))
            if tax_all_deductions.personalsteuer > 0:
                st.metric("Personal Tax", format_currency(tax_all_deductions.personalsteuer))
            if tax_all_deductions.church_tax > 0:
                st.metric("Church Tax", format_currency(tax_all_deductions.church_tax))
            if tax_all_deductions.wealth_tax > 0:
                st.metric("Wealth Tax", format_currency(tax_all_deductions.wealth_tax))
            st.divider()
            st.metric("TOTAL ZH TAX", format_currency(tax_all_deductions.total_tax))
            st.success(f"🎯 Total savings: {format_currency(comparison.total_savings)} ({format_percent(comparison.total_savings_percent)})")

    # Interactive Optimization Section
    st.divider()
    st.subheader("🎯 Optimize Your Deductions (Interactive)")
    st.caption("Use the sliders below to see how changing your Pillar 3a and Pillar 2 contributions affects your taxes in real-time")

    # Import constants
    from models.constants import PILLAR_3A_MAX_EMPLOYED, PILLAR_3A_MAX_SELF_EMPLOYED

    # Determine max Pillar 3a
    max_3a = PILLAR_3A_MAX_EMPLOYED if profile.employment_type != 'self_employed' else PILLAR_3A_MAX_SELF_EMPLOYED

    col1, col2 = st.columns(2)

    with col1:
        optimized_3a = st.slider(
            "💰 Pillar 3a Contribution (CHF/year)",
            min_value=0,
            max_value=int(max_3a),
            value=int(deductions.pillar_3a),
            step=100,
            help=f"Maximum: {format_currency(max_3a)}"
        )

    with col2:
        optimized_2_buyins = st.slider(
            "🏦 Pillar 2 Buy-ins (CHF/year)",
            min_value=0,
            max_value=100000,
            value=int(deductions.pillar_2_buyins),
            step=1000,
            help="Additional contributions to your pension fund"
        )

    # Calculate optimized scenario
    optimized_deductions = deductions.total_deductions - deductions.pillar_3a - deductions.pillar_2_buyins + optimized_3a + optimized_2_buyins

    # Create temporary deduction result for optimized scenario
    temp_deductions = DeductionResult()
    temp_deductions.commuting_pauschal = deductions.commuting_pauschal
    temp_deductions.meal_costs_pauschal = deductions.meal_costs_pauschal
    temp_deductions.professional_expenses = deductions.professional_expenses
    temp_deductions.side_income_deduction = deductions.side_income_deduction
    temp_deductions.child_deductions = deductions.child_deductions
    temp_deductions.property_maintenance = deductions.property_maintenance
    temp_deductions.asset_management = deductions.asset_management
    temp_deductions.insurance_premiums = deductions.insurance_premiums
    temp_deductions.dual_income_deduction = deductions.dual_income_deduction
    temp_deductions.pillar_3a = optimized_3a
    temp_deductions.pillar_2_buyins = optimized_2_buyins
    temp_deductions.ahv_contributions = deductions.ahv_contributions
    temp_deductions.mortgage_interest = deductions.mortgage_interest
    temp_deductions.other_debt_interest = deductions.other_debt_interest
    temp_deductions.medical_costs = deductions.medical_costs
    temp_deductions.medical_costs_deductible = deductions.medical_costs_deductible
    temp_deductions.childcare_costs = deductions.childcare_costs
    temp_deductions.donations = deductions.donations
    temp_deductions.political_contributions = deductions.political_contributions
    temp_deductions.alimony_payments = deductions.alimony_payments
    temp_deductions.support_payments = deductions.support_payments
    temp_deductions.calculate_totals()

    tax_optimized = calculate_complete_taxes(
        income,
        temp_deductions.total_deductions,
        profile,
        deduction_result=temp_deductions
    )

    # Side-by-side comparison
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 📊 Current Scenario")
            st.metric("Total Deductions", format_currency(deductions.total_deductions))
            st.metric("Pillar 3a", format_currency(deductions.pillar_3a))
            st.metric("Pillar 2 Buy-ins", format_currency(deductions.pillar_2_buyins))
            st.divider()
            st.metric("Total Tax", format_currency(tax_all_deductions.total_tax))

    with col2:
        with st.container(border=True):
            st.markdown("### 🎯 Optimized Scenario")
            st.metric("Total Deductions", format_currency(temp_deductions.total_deductions))
            st.metric("Pillar 3a", format_currency(optimized_3a))
            st.metric("Pillar 2 Buy-ins", format_currency(optimized_2_buyins))
            st.divider()
            st.metric("Total Tax", format_currency(tax_optimized.total_tax))

            savings = tax_all_deductions.total_tax - tax_optimized.total_tax
            if savings > 0:
                st.success(f"💰 Additional Savings: {format_currency(savings)}")
            elif savings < 0:
                st.warning(f"⚠️ Higher Tax: {format_currency(-savings)}")
            else:
                st.info("No change")

    return comparison, tax_all_deductions
