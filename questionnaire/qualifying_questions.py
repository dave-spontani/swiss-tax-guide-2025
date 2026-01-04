"""
Step 1: Qualifying Questions
Determines which deduction categories are relevant for the user
"""
import streamlit as st
from models.tax_data import UserProfile
from models.constants import MUNICIPALITY_STEUERFUESSE


def render_qualifying_questions(profile: UserProfile) -> UserProfile:
    """
    Render qualifying questions to determine relevant deductions.

    Args:
        profile: User profile to update

    Returns:
        Updated UserProfile
    """
    st.header("Step 1: Personal Information")
    st.caption("Answer these questions to determine which deductions apply to you")

    # Personal Details Section
    st.subheader("Personal Details")
    col1, col2 = st.columns(2)

    with col1:
        profile.marital_status = st.selectbox(
            "Marital Status",
            options=['single', 'married', 'separated', 'divorced'],
            index=0,
            format_func=lambda x: {
                'single': 'Single',
                'married': 'Married',
                'separated': 'Separated',
                'divorced': 'Divorced'
            }[x],
            help="Your legal marital status as of December 31"
        )

    with col2:
        profile.religious_affiliation = st.selectbox(
            "Religious Affiliation",
            options=['none', 'reformed', 'catholic', 'christian-catholic'],
            index=0,
            format_func=lambda x: {
                'none': 'None / No church tax',
                'reformed': 'Reformed Protestant',
                'catholic': 'Roman Catholic',
                'christian-catholic': 'Christian Catholic'
            }[x],
            help="Determines church tax liability"
        )

    # Children
    col1, col2 = st.columns(2)

    with col1:
        profile.num_children = st.number_input(
            "Number of Children",
            min_value=0,
            max_value=20,
            value=profile.num_children,
            help="Children under 18 or in education (up to age 25)"
        )

    with col2:
        if profile.num_children > 0:
            st.caption("Enter ages of children (optional, for childcare deduction)")
            ages_input = st.text_input(
                "Children's ages (comma-separated)",
                placeholder="e.g., 5, 8, 12",
                help="Needed to determine childcare deduction eligibility (under 14)"
            )
            if ages_input:
                try:
                    profile.children_ages = [int(age.strip()) for age in ages_input.split(',')]
                except ValueError:
                    st.error("Please enter valid ages separated by commas")

    # Employment & Income Section
    st.subheader("Employment & Income")

    col1, col2 = st.columns(2)

    with col1:
        profile.employment_type = st.selectbox(
            "Employment Status",
            options=['employed', 'self_employed', 'both', 'retired', 'not_working'],
            index=0,
            format_func=lambda x: {
                'employed': 'Employed',
                'self_employed': 'Self-employed',
                'both': 'Both employed and self-employed',
                'retired': 'Retired',
                'not_working': 'Not working'
            }[x],
            help="Your primary employment status"
        )

    with col2:
        profile.net_salary = st.number_input(
            "Annual Net Salary (CHF)",
            min_value=0.0,
            value=profile.net_salary if profile.net_salary > 0 else 100000.0,
            step=1000.0,
            help="Your annual net salary (after AHV/IV/ALV deductions)"
        )

    # Additional employment questions
    if profile.employment_type in ['employed', 'both']:
        st.caption("Commuting")
        col1, col2 = st.columns(2)

        with col1:
            profile.bikes_to_work = st.checkbox(
                "🚴 I bike to work",
                value=profile.bikes_to_work,
                help="Automatic CHF 700 pauschal deduction (no receipts needed)"
            )

        with col2:
            profile.uses_public_transport_car = st.checkbox(
                "🚗 I use public transport/car",
                value=profile.uses_public_transport_car,
                help="Can claim actual costs with receipts (slider in next step)"
            )

        # Update commutes_to_work flag
        profile.commutes_to_work = profile.bikes_to_work or profile.uses_public_transport_car

        st.caption("Meals")
        col1, col2 = st.columns(2)

        with col1:
            profile.works_away_from_home = st.checkbox(
                "Do you eat meals away from home?",
                value=True,
                help="If yes, you get automatic meal cost deduction"
            )

        with col2:
            if profile.works_away_from_home:
                profile.employer_meal_subsidy = st.checkbox(
                    "Employer subsidizes meals?",
                    value=False,
                    help="Affects meal deduction amount (CHF 1,600 vs 3,200)"
                )

    # Side income
    profile.has_side_income = st.checkbox(
        "Do you have side income (Nebenerwerb)?",
        value=profile.has_side_income,
        help="If yes, you get automatic CHF 2,400 deduction"
    )

    # Married-specific questions
    if profile.marital_status == 'married':
        profile.both_spouses_work = st.checkbox(
            "Do both spouses work?",
            value=profile.both_spouses_work,
            help="If yes, you get CHF 5,900 dual income deduction"
        )

    # Location Section
    st.subheader("Location")

    col1, col2 = st.columns(2)

    with col1:
        profile.municipality = st.selectbox(
            "Municipality",
            options=list(MUNICIPALITY_STEUERFUESSE.keys()),
            index=0,
            help="Your municipality determines the municipal tax rate"
        )

    with col2:
        profile.gemeinde_steuerfuss = MUNICIPALITY_STEUERFUESSE[profile.municipality]
        st.metric(
            "Municipal Tax Rate (Steuerfuss)",
            f"{profile.gemeinde_steuerfuss}%",
            help="This is the tax multiplier for your municipality"
        )

    # Assets Section
    st.subheader("Assets & Property")

    col1, col2 = st.columns(2)

    with col1:
        profile.owns_property = st.checkbox(
            "Do you own property in Switzerland?",
            value=profile.owns_property,
            help="If yes, you can deduct property maintenance costs"
        )

        if profile.owns_property:
            profile.property_age = st.number_input(
                "Property age (years)",
                min_value=0,
                max_value=200,
                value=profile.property_age if profile.property_age else 10,
                help="Age of the property"
            )

            profile.eigenmietwert = st.number_input(
                "Annual Eigenmietwert (CHF)",
                min_value=0.0,
                value=profile.eigenmietwert if profile.eigenmietwert else 24000.0,
                step=1000.0,
                help="Annual imputed rental value (from tax assessment)"
            )

    with col2:
        profile.has_securities = st.checkbox(
            "Do you have securities/investments?",
            value=profile.has_securities,
            help="If yes, you can deduct asset management costs"
        )

        if profile.has_securities:
            profile.securities_value = st.number_input(
                "Total securities value (CHF)",
                min_value=0.0,
                value=profile.securities_value if profile.securities_value else 100000.0,
                step=10000.0,
                help="Total value of your securities portfolio"
            )

    # Wealth
    profile.total_wealth = st.number_input(
        "Total Net Wealth (CHF)",
        min_value=0.0,
        value=profile.total_wealth,
        step=10000.0,
        help="Total assets minus liabilities (for wealth tax calculation)"
    )

    # Special Circumstances Section
    st.subheader("Special Circumstances")

    col1, col2, col3 = st.columns(3)

    with col1:
        profile.is_disabled = st.checkbox(
            "Are you or a dependent disabled?",
            value=profile.is_disabled,
            help="If yes, you can deduct disability-related costs"
        )

    with col2:
        profile.supports_others = st.checkbox(
            "Do you support others financially?",
            value=profile.supports_others,
            help="If yes, you may be able to deduct support payments"
        )

    with col3:
        profile.pays_alimony = st.checkbox(
            "Do you pay alimony/child support?",
            value=profile.pays_alimony,
            help="If yes, you can deduct these payments"
        )

    return profile
