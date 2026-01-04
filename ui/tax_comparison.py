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
from utils.formatters import format_currency, format_percent


def calculate_complete_taxes(income: float, deductions: float, profile: UserProfile) -> TaxResult:
    """Calculate all taxes for a given income and deductions."""
    result = TaxResult()
    result.gross_income = income
    result.total_deductions = deductions

    # Federal tax
    fed_result = calculate_federal_tax(income, deductions)
    result.federal_tax = fed_result.federal_tax
    result.federal_effective_rate = fed_result.federal_effective_rate
    result.federal_marginal_rate = fed_result.federal_marginal_rate
    result.federal_bracket_index = fed_result.federal_bracket_index
    result.federal_breakdown = fed_result.federal_breakdown
    result.taxable_income = fed_result.taxable_income

    # Cantonal tax
    cant_result = calculate_zurich_tax(income, profile.gemeinde_steuerfuss, deductions)
    result.einfache_staatssteuer = cant_result.einfache_staatssteuer
    result.cantonal_tax = cant_result.cantonal_tax
    result.municipal_tax = cant_result.municipal_tax
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
            profile.gemeinde_steuerfuss
        )
        result.wealth_tax = wealth_result['wealth_tax']
        result.wealth_effective_rate = wealth_result['effective_rate']

    # Calculate totals
    result.calculate_totals()

    return result


def render_tax_comparison(profile: UserProfile, deductions: DeductionResult):
    """Render 3-level tax comparison."""
    st.header("Your Tax Calculation Results")

    income = profile.net_salary

    # Calculate three scenarios
    tax_no_deductions = calculate_complete_taxes(income, 0, profile)
    tax_auto_deductions = calculate_complete_taxes(income, deductions.total_automatic, profile)
    tax_all_deductions = calculate_complete_taxes(income, deductions.total_deductions, profile)

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
            if tax_no_deductions.church_tax > 0:
                st.metric("Church Tax", format_currency(tax_no_deductions.church_tax))
            st.divider()
            st.metric("TOTAL TAX", format_currency(tax_no_deductions.total_tax))
            st.caption(f"Effective Rate: {format_percent(tax_no_deductions.total_effective_rate)}")

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
            st.divider()
            st.metric("TOTAL TAX", format_currency(tax_auto_deductions.total_tax))
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
            st.divider()
            st.metric("TOTAL TAX", format_currency(tax_all_deductions.total_tax))
            st.success(f"🎯 Total savings: {format_currency(comparison.total_savings)} ({format_percent(comparison.total_savings_percent)})")

    return comparison, tax_all_deductions
