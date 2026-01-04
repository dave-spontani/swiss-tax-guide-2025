"""
Step 3: Optional Deductions (require documentation)
Collect amounts for deductions that need receipts/certificates
"""
import streamlit as st
from models.tax_data import UserProfile, DeductionResult
from calculations.deductions import (
    validate_pillar_3a,
    validate_childcare_costs,
    validate_medical_costs,
    validate_donations,
    validate_political_contributions,
    validate_debt_interest
)
from utils.formatters import format_currency


def render_optional_deductions(profile: UserProfile, deductions: DeductionResult) -> DeductionResult:
    """
    Render optional deductions that require documentation.

    Args:
        profile: User profile
        deductions: Deduction result with automatic deductions

    Returns:
        Updated DeductionResult with optional deductions
    """
    st.header("Step 3: Optional Deductions")
    st.caption("These deductions require documentation (receipts, certificates)")

    # Pension & Savings Section
    st.subheader("Pension & Savings")

    col1, col2 = st.columns(2)

    # Pillar 3a
    with col1:
        pillar_3a_amount = st.number_input(
            "Pillar 3a Contributions (CHF)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            help="Contributions to your Pillar 3a account"
        )

        validation = validate_pillar_3a(pillar_3a_amount, profile)
        deductions.pillar_3a = validation['amount']

        if pillar_3a_amount > 0:
            if not validation['is_valid']:
                st.error(f"Exceeds maximum of {format_currency(validation['max_limit'])}")
            else:
                st.success(f"Remaining contribution room: {format_currency(validation['remaining'])}")
            st.caption("📄 Required: Pillar 3a certificate from bank/insurance")

    # Pillar 2
    with col2:
        deductions.pillar_2_buyins = st.number_input(
            "Pillar 2 Buy-ins (CHF)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            help="Additional purchases into your pension fund"
        )

        if deductions.pillar_2_buyins > 0:
            st.caption("📄 Required: Pillar 2 buy-in confirmation")
            st.warning("⚠️ Remember: 3-year lock-in period for capital withdrawal")

    # Major Expenses Section
    st.divider()
    st.subheader("Major Expenses")

    # Mortgage/Debt Interest
    if profile.owns_property or profile.has_securities:
        col1, col2 = st.columns(2)

        with col1:
            deductions.mortgage_interest = st.number_input(
                "Mortgage Interest (CHF)",
                min_value=0.0,
                value=0.0,
                step=100.0,
                help="Interest paid on mortgage"
            )
            if deductions.mortgage_interest > 0:
                st.caption("📄 Required: Bank statement showing interest paid")

        with col2:
            other_debt = st.number_input(
                "Other Debt Interest (CHF)",
                min_value=0.0,
                value=0.0,
                step=100.0,
                help="Interest on other loans (not leasing!)"
            )

            debt_validation = validate_debt_interest(other_debt)
            deductions.other_debt_interest = debt_validation['deductible']

            if other_debt > 0:
                if not debt_validation['is_valid']:
                    st.warning(f"Exceeds max of {format_currency(debt_validation['max_limit'])}")
                st.caption("📄 Required: Loan statements")

    # Medical Costs
    medical_total = st.number_input(
        "Total Medical Costs (CHF)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Doctor, dentist, therapies, medications"
    )

    if medical_total > 0:
        medical_validation = validate_medical_costs(medical_total, profile.net_salary)
        deductions.medical_costs = medical_total
        deductions.medical_costs_deductible = medical_validation['deductible']

        if medical_validation['below_threshold']:
            st.warning(f"Below 5% threshold of {format_currency(medical_validation['threshold'])}. Not deductible.")
        else:
            st.success(f"Deductible amount: {format_currency(medical_validation['deductible'])}")
        st.caption("📄 Required: Annual statement from health insurance, dentist invoices")

    # Childcare
    if profile.num_children > 0:
        childcare_amount = st.number_input(
            "Childcare Costs (CHF)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            help="Daycare, nanny, after-school care"
        )

        if childcare_amount > 0:
            childcare_validation = validate_childcare_costs(childcare_amount, profile)
            deductions.childcare_costs = childcare_validation['deductible_amount']

            if not childcare_validation['eligible']:
                st.error(childcare_validation['reason'])
            elif not childcare_validation['is_valid']:
                st.warning(f"Exceeds maximum of {format_currency(childcare_validation['max_limit'])}")
            else:
                st.success(f"Deductible: {format_currency(deductions.childcare_costs)}")
            st.caption("📄 Required: Childcare invoices")

    # Contributions Section
    st.divider()
    st.subheader("Contributions")

    col1, col2 = st.columns(2)

    # Donations
    with col1:
        donations_amount = st.number_input(
            "Donations (CHF)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            help="Donations to tax-exempt organizations"
        )

        if donations_amount > 0:
            donation_validation = validate_donations(donations_amount, profile.net_salary)
            deductions.donations = donation_validation['deductible']

            if not donation_validation['is_valid']:
                st.warning(f"Exceeds 20% of income ({format_currency(donation_validation['max_limit'])})")
            st.caption("📄 Required: Donation receipts from registered organizations")

    # Political Contributions
    with col2:
        political_amount = st.number_input(
            "Political Party Contributions (CHF)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            help="Contributions to political parties"
        )

        if political_amount > 0:
            political_validation = validate_political_contributions(political_amount, profile)
            deductions.political_contributions = political_validation['deductible']

            if not political_validation['is_valid']:
                st.warning(f"Exceeds maximum of {format_currency(political_validation['max_limit'])}")
            st.caption("📄 Required: Party membership receipts")

    # Support Payments Section
    if profile.pays_alimony or profile.supports_others:
        st.divider()
        st.subheader("Support Payments")

        if profile.pays_alimony:
            deductions.alimony_payments = st.number_input(
                "Alimony/Child Support Payments (CHF)",
                min_value=0.0,
                value=0.0,
                step=1000.0,
                help="Payments to ex-spouse or children"
            )
            if deductions.alimony_payments > 0:
                st.caption("📄 Required: Divorce decree, payment confirmations")

        if profile.supports_others:
            deductions.support_payments = st.number_input(
                "Support Payments to Others (CHF)",
                min_value=0.0,
                value=0.0,
                step=1000.0,
                help="Support to financially weak or incapacitated persons"
            )
            if deductions.support_payments > 0:
                st.caption("📄 Required: Payment confirmations, proof of need")

    # Calculate totals
    deductions.calculate_totals()

    # Summary
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Automatic Deductions", format_currency(deductions.total_automatic))
    with col2:
        st.metric("Optional Deductions", format_currency(deductions.total_optional))
    with col3:
        st.metric("Total Deductions", format_currency(deductions.total_deductions))

    return deductions
