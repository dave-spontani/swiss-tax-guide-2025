"""
Interactive Tax Optimization Tools
Real-time sliders for optimizing tax deductions
"""
import streamlit as st
from models.tax_data import UserProfile, DeductionResult
from ui.tax_comparison import calculate_complete_taxes
from utils.formatters import format_currency, format_percent
from models.constants import PILLAR_3A_MAX_EMPLOYED, PILLAR_3A_MAX_SELF_EMPLOYED


def render_optimization_tools(profile: UserProfile, current_deductions: DeductionResult):
    """Render interactive optimization tools."""
    st.header("Tax Optimization Tools")
    st.caption("Use these interactive tools to see how different deductions affect your taxes")

    income = profile.net_salary

    # Pillar 3a Optimizer
    st.subheader("💡 Pillar 3a Optimizer")

    max_3a = PILLAR_3A_MAX_EMPLOYED if profile.employment_type != 'self_employed' else PILLAR_3A_MAX_SELF_EMPLOYED
    current_3a = current_deductions.pillar_3a

    col1, col2 = st.columns([3, 1])

    with col1:
        optimized_3a = st.slider(
            "Annual Pillar 3a Contribution",
            min_value=0,
            max_value=int(max_3a),
            value=int(current_3a),
            step=100,
            format="CHF %d"
        )

    # Calculate tax with different 3a amounts
    temp_deductions_no_3a = current_deductions.total_deductions - current_deductions.pillar_3a
    temp_deductions_with_3a = temp_deductions_no_3a + optimized_3a

    tax_no_3a = calculate_complete_taxes(income, temp_deductions_no_3a, profile)
    tax_with_3a = calculate_complete_taxes(income, temp_deductions_with_3a, profile)

    tax_savings = tax_no_3a.total_tax - tax_with_3a.total_tax
    net_cost = optimized_3a - tax_savings
    roi = (tax_savings / optimized_3a * 100) if optimized_3a > 0 else 0

    with col2:
        st.metric("Tax Savings", format_currency(tax_savings))
        st.metric("Net Cost", format_currency(net_cost))
        st.metric("ROI", format_percent(roi))

    st.progress(optimized_3a / max_3a)
    st.caption(f"Remaining contribution room: {format_currency(max_3a - optimized_3a)}")

    # Pillar 2 Buy-In Impact
    st.divider()
    st.subheader("💡 Pillar 2 Buy-In Impact")

    buyins = st.number_input(
        "Pillar 2 Buy-In Amount",
        min_value=0,
        max_value=100000,
        value=int(current_deductions.pillar_2_buyins),
        step=1000,
        format="%d"
    )

    if buyins > 0:
        temp_deductions_no_buyins = current_deductions.total_deductions - current_deductions.pillar_2_buyins
        temp_deductions_with_buyins = temp_deductions_no_buyins + buyins

        tax_no_buyins = calculate_complete_taxes(income, temp_deductions_no_buyins, profile)
        tax_with_buyins = calculate_complete_taxes(income, temp_deductions_with_buyins, profile)

        buyins_savings = tax_no_buyins.total_tax - tax_with_buyins.total_tax

        col1, col2 = st.columns(2)
        with col1:
            st.success(f"Tax savings: {format_currency(buyins_savings)}")
        with col2:
            st.info(f"Net cost: {format_currency(buyins - buyins_savings)}")

        st.warning("⚠️ Remember: 3-year lock-in period for capital withdrawal")

    # Medical Costs Calculator
    st.divider()
    st.subheader("💡 Medical Costs Calculator")

    threshold = income * 0.05
    st.info(f"Only medical costs above {format_currency(threshold)} (5% of income) are deductible")

    medical_costs = st.number_input(
        "Total Medical Costs",
        min_value=0,
        value=int(current_deductions.medical_costs),
        step=100
    )

    if medical_costs > threshold:
        deductible = medical_costs - threshold

        temp_deductions_with_medical = current_deductions.total_deductions - current_deductions.medical_costs_deductible + deductible
        tax_with_medical = calculate_complete_taxes(income, temp_deductions_with_medical, profile)
        tax_without_medical = calculate_complete_taxes(income, current_deductions.total_deductions - current_deductions.medical_costs_deductible, profile)

        medical_savings = tax_without_medical.total_tax - tax_with_medical.total_tax

        col1, col2 = st.columns(2)
        with col1:
            st.success(f"Deductible amount: {format_currency(deductible)}")
        with col2:
            st.success(f"Tax savings: {format_currency(medical_savings)}")
    else:
        st.warning(f"Below threshold. Need {format_currency(threshold - medical_costs)} more for deduction.")

    # Summary
    st.divider()
    st.subheader("🎯 Optimization Summary")

    # Calculate optimized scenario
    optimized_deductions = DeductionResult()
    optimized_deductions.total_automatic = current_deductions.total_automatic
    optimized_deductions.pillar_3a = optimized_3a
    optimized_deductions.pillar_2_buyins = buyins
    optimized_deductions.medical_costs_deductible = max(0, medical_costs - threshold) if medical_costs > threshold else 0
    optimized_deductions.calculate_totals()

    tax_current = calculate_complete_taxes(income, current_deductions.total_deductions, profile)
    tax_optimized = calculate_complete_taxes(income, optimized_deductions.total_deductions, profile)

    potential_savings = tax_current.total_tax - tax_optimized.total_tax

    if potential_savings > 0:
        st.success(f"💰 Additional savings potential: {format_currency(potential_savings)}")

        # Create comparison table
        comparison_df = pd.DataFrame({
            'Scenario': ['Current', 'Optimized'],
            'Pillar 3a': [format_currency(current_deductions.pillar_3a), format_currency(optimized_3a)],
            'Pillar 2': [format_currency(current_deductions.pillar_2_buyins), format_currency(buyins)],
            'Total Deductions': [format_currency(current_deductions.total_deductions), format_currency(optimized_deductions.total_deductions)],
            'Total Tax': [format_currency(tax_current.total_tax), format_currency(tax_optimized.total_tax)],
            'Savings': [format_currency(0), format_currency(potential_savings)],
        })

        st.dataframe(comparison_df, hide_index=True, use_container_width=True)
    else:
        st.info("You're already optimized! No additional savings potential found.")


# Add pandas import at the top
import pandas as pd
