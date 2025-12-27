"""
Streamlit input form components

Provides sidebar input forms for user profile and deduction inputs.
"""

import streamlit as st
from models.user_profile import UserProfile, CivilStatus, Canton
from config.municipality_data import get_municipality_multiplier, get_municipality_names
from utils.constants import (
    DEFAULT_CANTON,
    DEFAULT_MUNICIPALITY,
    DEFAULT_EMPLOYMENT_PERCENTAGE,
    DEFAULT_HAS_PILLAR2,
    HELP_TEXT
)


def render_basic_info_form() -> UserProfile:
    """
    Render basic user information input form in sidebar

    Returns:
        UserProfile object with user inputs
    """
    st.sidebar.header("📋 Personal Information")

    # Gross salary
    gross_salary = st.sidebar.number_input(
        "Annual Gross Salary (CHF)",
        min_value=0.0,
        max_value=10_000_000.0,
        value=80_000.0,
        step=1_000.0,
        help=HELP_TEXT["gross_salary"]
    )

    # Employment percentage
    employment_percentage = st.sidebar.slider(
        "Employment Percentage (%)",
        min_value=10.0,
        max_value=100.0,
        value=DEFAULT_EMPLOYMENT_PERCENTAGE,
        step=10.0,
        help=HELP_TEXT["employment_percentage"]
    )

    # Has Pillar 2
    has_pillar2 = st.sidebar.checkbox(
        "Enrolled in Pillar 2 (Company Pension)",
        value=DEFAULT_HAS_PILLAR2,
        help=HELP_TEXT["has_pillar2"]
    )

    # Municipality selection
    st.sidebar.subheader("📍 Location")

    municipality_names = get_municipality_names('ZH')
    municipality = st.sidebar.selectbox(
        "Municipality",
        options=municipality_names,
        index=municipality_names.index(DEFAULT_MUNICIPALITY) if DEFAULT_MUNICIPALITY in municipality_names else 0,
        help=HELP_TEXT["municipality"]
    )

    municipality_multiplier = get_municipality_multiplier(municipality, 'ZH')

    st.sidebar.info(f"📊 Municipal tax multiplier: **{municipality_multiplier}** (119%)")

    # Create UserProfile
    user_profile = UserProfile(
        civil_status=CivilStatus.SINGLE,
        canton=Canton.ZURICH,
        municipality=municipality,
        municipality_multiplier=municipality_multiplier,
        gross_salary=gross_salary,
        has_pillar2=has_pillar2,
        num_children=0,
        employment_percentage=employment_percentage
    )

    return user_profile


def render_deduction_inputs():
    """
    Render deduction input form in sidebar

    Returns:
        Dictionary with deduction inputs
    """
    st.sidebar.header("💼 Deductions")

    with st.sidebar.expander("🚇 Commuting & Meals"):
        # Transport type
        transport_type = st.radio(
            "How do you commute?",
            options=["Public Transport", "Bicycle", "Car (requires justification)", "Work from home"],
            index=0,
            help=HELP_TEXT["commuting"]
        )

        # Public transport cost
        public_transport_cost = 0.0
        if transport_type == "Public Transport":
            public_transport_cost = st.number_input(
                "Annual Public Transport Cost (CHF)",
                min_value=0.0,
                max_value=10_000.0,
                value=0.0,
                step=100.0,
                help="Enter your annual GA or travel pass cost (2nd class)"
            )

        st.divider()

        # Professional expenses deduction (opt-in)
        claim_professional = st.checkbox(
            "Claim Professional Expenses Deduction",
            value=False,
            help="Pauschal deduction for tools, software, professional literature, work clothes (3% of salary, min CHF 2,000, max CHF 4,000). Technically no proof required, but use responsibly."
        )

        if claim_professional:
            st.caption("⚠️ This reduces your taxable income. Ensure you have legitimate work-related expenses.")

        # Meal expenses deduction (opt-in)
        claim_meals = st.checkbox(
            "Claim Meal Expense Deduction",
            value=False,
            help="Deduction for eating lunch away from home during work (CHF 1,600-3,200/year). Only claim if you cannot reasonably eat at home."
        )

        has_canteen = False
        if claim_meals:
            has_canteen = st.checkbox(
                "I have canteen or meal subsidy from employer",
                value=False,
                help="With subsidy: CHF 1,600/year | Without subsidy: CHF 3,200/year"
            )
            st.caption("⚠️ Only claim if you cannot eat lunch at home due to distance/time constraints.")

    with st.sidebar.expander("🏥 Insurance"):
        insurance_premiums = st.number_input(
            "Annual Insurance Premiums (CHF)",
            min_value=0.0,
            max_value=20_000.0,
            value=4_800.0,
            step=100.0,
            help=HELP_TEXT["insurance"] + " (Health insurance typically CHF 300-500/month)"
        )

        premium_subsidies = st.number_input(
            "Premium Subsidies Received (CHF)",
            min_value=0.0,
            max_value=10_000.0,
            value=0.0,
            step=100.0,
            help="Prämienverbilligung - must be subtracted from premiums"
        )

    with st.sidebar.expander("💰 Pillar 3a"):
        pillar3a_contribution = st.number_input(
            "Pillar 3a Contribution (CHF)",
            min_value=0.0,
            max_value=10_000.0,
            value=0.0,
            step=500.0,
            help=HELP_TEXT["pillar_3a"] + " (Max CHF 7,258 in 2025 with Pillar 2)"
        )

    with st.sidebar.expander("📚 Education & Other", expanded=False):
        education_costs = st.number_input(
            "Further Education Costs (CHF)",
            min_value=0.0,
            max_value=15_000.0,
            value=0.0,
            step=100.0,
            help=HELP_TEXT["education"]
        )

        charitable_donations = st.number_input(
            "Charitable Donations (CHF)",
            min_value=0.0,
            max_value=50_000.0,
            value=0.0,
            step=100.0,
            help=HELP_TEXT["charitable"]
        )

        political_donations = st.number_input(
            "Political Party Donations (CHF)",
            min_value=0.0,
            max_value=15_000.0,
            value=0.0,
            step=100.0,
            help=HELP_TEXT["political"]
        )

    return {
        'transport_type': transport_type,
        'public_transport_cost': public_transport_cost,
        'claim_professional': claim_professional,
        'claim_meals': claim_meals,
        'has_canteen': has_canteen,
        'insurance_premiums': insurance_premiums,
        'premium_subsidies': premium_subsidies,
        'pillar3a_contribution': pillar3a_contribution,
        'education_costs': education_costs,
        'charitable_donations': charitable_donations,
        'political_donations': political_donations
    }
