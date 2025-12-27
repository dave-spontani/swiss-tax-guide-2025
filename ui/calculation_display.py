"""
Calculation display UI component

Displays step-by-step tax calculation breakdown.
"""

import streamlit as st
import pandas as pd
from models.tax_calculation import TaxBreakdown
from utils.formatters import format_chf, format_percentage
from utils.constants import COLOR_INCOME, COLOR_DEDUCTION, COLOR_TAX


def render_summary_metrics(breakdown: TaxBreakdown):
    """
    Render key metrics in cards at the top

    Args:
        breakdown: TaxBreakdown object with calculation results
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Gross Salary",
            value=format_chf(breakdown.gross_salary, decimals=0),
            help="Annual gross salary before taxes and social security"
        )

    with col2:
        st.metric(
            label="Total Tax",
            value=format_chf(breakdown.total_tax, decimals=0),
            delta=f"-{breakdown.effective_tax_rate:.1f}%",
            delta_color="inverse",
            help="Total federal + cantonal + municipal tax"
        )

    with col3:
        st.metric(
            label="Net Annual Income",
            value=format_chf(breakdown.net_annual_income, decimals=0),
            help="Take-home pay after all taxes and social security"
        )

    with col4:
        st.metric(
            label="Net Monthly Income",
            value=format_chf(breakdown.net_monthly_income, decimals=0),
            help="Net annual income divided by 12 months"
        )


def render_tax_breakdown(breakdown: TaxBreakdown):
    """
    Render detailed tax breakdown

    Args:
        breakdown: TaxBreakdown object with calculation results
    """
    st.subheader("🧾 Tax Breakdown")

    # Create breakdown dataframe
    tax_data = {
        "Tax Component": ["Federal Tax", "Cantonal Tax", "Municipal Tax", "**Total Tax**"],
        "Amount": [
            format_chf(breakdown.federal_tax),
            format_chf(breakdown.cantonal_tax),
            format_chf(breakdown.municipal_tax),
            f"**{format_chf(breakdown.total_tax)}**"
        ],
        "% of Gross": [
            format_percentage(breakdown.federal_tax / breakdown.gross_salary * 100 if breakdown.gross_salary > 0 else 0),
            format_percentage(breakdown.cantonal_tax / breakdown.gross_salary * 100 if breakdown.gross_salary > 0 else 0),
            format_percentage(breakdown.municipal_tax / breakdown.gross_salary * 100 if breakdown.gross_salary > 0 else 0),
            f"**{format_percentage(breakdown.effective_tax_rate)}**"
        ]
    }

    df = pd.DataFrame(tax_data)
    st.table(df)

    # Additional info
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Effective Tax Rate:** {breakdown.effective_tax_rate:.2f}%  \nTotal tax as % of gross salary")
    with col2:
        st.info(f"**Marginal Tax Rate:** {breakdown.marginal_tax_rate:.2f}%  \nTax rate on your next CHF earned")


def render_deduction_summary(breakdown: TaxBreakdown):
    """
    Render summary of deductions applied

    Args:
        breakdown: TaxBreakdown object with calculation results
    """
    st.subheader("📉 Deductions Applied")

    if not breakdown.deduction_details:
        st.warning("No deductions applied. Consider using available deductions to reduce your tax burden!")
        return

    # Create deductions dataframe
    deduction_data = []
    for deduction in breakdown.deduction_details:
        deduction_data.append({
            "Deduction": deduction.description,
            "Amount": format_chf(deduction.amount),
            "Type": "🟢 Automatic (no proof)" if deduction.is_automatic else "📄 Requires proof"
        })

    # Add total row
    deduction_data.append({
        "Deduction": "**Total Deductions**",
        "Amount": f"**{format_chf(breakdown.total_deductions)}**",
        "Type": ""
    })

    df = pd.DataFrame(deduction_data)
    st.table(df)


def render_calculation_steps(breakdown: TaxBreakdown):
    """
    Render step-by-step calculation

    Args:
        breakdown: TaxBreakdown object with calculation results
    """
    st.subheader("📊 Step-by-Step Calculation")

    with st.expander("Show detailed calculation steps", expanded=False):
        for step in breakdown.calculation_steps:
            # Determine color based on amount
            if step.amount > 0:
                if "Tax" in step.title or "Social Security" in step.title:
                    color = "red"
                else:
                    color = "green"
            elif step.amount < 0:
                color = "blue"
            else:
                color = "gray"

            # Display step
            st.markdown(f"**{step.step_number}. {step.title}**")
            if step.description:
                st.caption(step.description)

            if step.formula:
                st.code(step.formula, language=None)

            amount_display = format_chf(abs(step.amount))
            if step.amount < 0:
                st.markdown(f":{color}[-{amount_display}]")
            else:
                st.markdown(f":{color}[{amount_display}]")

            st.divider()


def render_calculation_breakdown(breakdown: TaxBreakdown):
    """
    Render complete calculation breakdown

    Args:
        breakdown: TaxBreakdown object with calculation results
    """
    # Summary metrics
    render_summary_metrics(breakdown)

    st.divider()

    # Tax breakdown
    col1, col2 = st.columns(2)

    with col1:
        render_tax_breakdown(breakdown)

    with col2:
        render_deduction_summary(breakdown)

    st.divider()

    # Detailed steps
    render_calculation_steps(breakdown)
