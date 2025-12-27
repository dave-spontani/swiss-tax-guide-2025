"""
Swiss Tax Deduction Analyzer - Main Streamlit Application

A comprehensive tool to calculate Swiss taxes and identify available deductions
for single, employed individuals in Zürich canton.
"""

import streamlit as st
from typing import List

# Import models
from models.user_profile import UserProfile
from models.deduction import Deduction, DeductionCategory

# Import services
from services.tax_calculator import SwissTaxCalculator
from services.deduction_validator import DeductionValidator

# Import UI components
from ui.input_forms import render_basic_info_form, render_deduction_inputs
from ui.calculation_display import render_calculation_breakdown

# Import utilities
from utils.formatters import format_chf
from utils.constants import APP_NAME, APP_ICON, TAX_YEAR


# Page configuration
st.set_page_config(
    page_title=f"{APP_NAME} - {TAX_YEAR}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


def collect_deductions(user_profile: UserProfile, deduction_inputs: dict) -> List[Deduction]:
    """
    Collect all applicable deductions based on user inputs

    Args:
        user_profile: User profile information
        deduction_inputs: Dictionary with deduction input values

    Returns:
        List of Deduction objects
    """
    validator = DeductionValidator()
    deductions = []

    # 1. Automatic deductions (professional expenses, meals)
    auto_deductions = validator.get_all_automatic_deductions(
        user_profile,
        has_canteen_subsidy=deduction_inputs['has_canteen']
    )
    deductions.extend(auto_deductions)

    # 2. Commuting deduction
    transport_type_map = {
        "Public Transport": "public_transport",
        "Bicycle": "bicycle",
        "Car (requires justification)": "car",
        "Work from home": None
    }

    transport_type = transport_type_map[deduction_inputs['transport_type']]

    if transport_type:
        commuting_deduction = validator.calculate_commuting_deduction(
            transport_type=transport_type,
            annual_cost=deduction_inputs['public_transport_cost'],
            canton='ZH'
        )
        if commuting_deduction.amount > 0:
            deductions.append(commuting_deduction)

    # 3. Insurance premiums
    if deduction_inputs['insurance_premiums'] > 0:
        insurance_deduction = validator.calculate_insurance_deduction(
            annual_premiums=deduction_inputs['insurance_premiums'],
            premium_subsidies=deduction_inputs['premium_subsidies'],
            user_profile=user_profile
        )
        if insurance_deduction.amount > 0:
            deductions.append(insurance_deduction)

    # 4. Pillar 3a
    if deduction_inputs['pillar3a_contribution'] > 0:
        is_valid, message, max_allowed, pillar3a_deduction = validator.validate_pillar3a_contribution(
            deduction_inputs['pillar3a_contribution'],
            user_profile
        )

        if is_valid and pillar3a_deduction:
            deductions.append(pillar3a_deduction)
        elif not is_valid:
            st.sidebar.warning(f"⚠️ Pillar 3a: {message}")

    # 5. Education costs
    if deduction_inputs['education_costs'] > 0:
        is_valid, message, education_deduction = validator.calculate_education_deduction(
            deduction_inputs['education_costs'],
            has_proof=True  # Assume user has proof
        )

        if is_valid and education_deduction:
            deductions.append(education_deduction)
        elif not is_valid:
            st.sidebar.info(f"ℹ️ Education: {message}")

    # 6. Charitable donations
    if deduction_inputs['charitable_donations'] > 0:
        is_valid, message, charitable_deduction = validator.calculate_charitable_deduction(
            deduction_inputs['charitable_donations'],
            user_profile.gross_salary
        )

        if is_valid and charitable_deduction:
            deductions.append(charitable_deduction)
        elif not is_valid:
            st.sidebar.info(f"ℹ️ Charitable: {message}")

    # 7. Political donations
    if deduction_inputs['political_donations'] > 0:
        is_valid, message, political_deduction = validator.calculate_political_donation_deduction(
            deduction_inputs['political_donations']
        )

        if is_valid and political_deduction:
            deductions.append(political_deduction)
        elif not is_valid:
            st.sidebar.info(f"ℹ️ Political: {message}")

    return deductions


def main():
    """Main application logic"""

    # Header
    st.title(f"{APP_ICON} {APP_NAME}")
    st.subheader(f"Zürich Canton - Tax Year {TAX_YEAR}")

    st.markdown("""
    Calculate your Swiss taxes and discover all available deductions to optimize your tax burden.
    This tool focuses on **single, employed individuals** in Zürich canton.
    """)

    # Sidebar inputs
    user_profile = render_basic_info_form()
    deduction_inputs = render_deduction_inputs()

    # Calculate button
    st.sidebar.divider()
    calculate_button = st.sidebar.button("🧮 Calculate Taxes", type="primary", use_container_width=True)

    # Main content
    if calculate_button or 'calculated' in st.session_state:
        st.session_state['calculated'] = True

        # Collect deductions
        deductions = collect_deductions(user_profile, deduction_inputs)

        # Calculate taxes
        calculator = SwissTaxCalculator(TAX_YEAR)
        breakdown = calculator.calculate_complete_breakdown(user_profile, deductions)

        # Store in session state
        st.session_state['breakdown'] = breakdown
        st.session_state['deductions'] = deductions
        st.session_state['user_profile'] = user_profile

    # Display results if available
    if 'breakdown' in st.session_state:
        breakdown = st.session_state['breakdown']

        # Create tabs
        tab1, tab2, tab3 = st.tabs([
            "📊 Tax Calculation",
            "💡 Optimization Tips",
            "ℹ️ About"
        ])

        with tab1:
            render_calculation_breakdown(breakdown)

        with tab2:
            st.subheader("💡 Optimization Tips")
            st.info("Optimization suggestions coming soon! This will analyze your current deductions and suggest ways to reduce your tax burden.")

            # Quick tips
            st.markdown("""
            ### Quick Tips to Reduce Taxes:

            1. **Maximize Pillar 3a**: Contribute up to CHF 7,258 (2025 limit) - fully deductible
            2. **Claim automatic deductions**: Professional expenses and meal costs don't require proof
            3. **Track your commuting costs**: Public transport costs are fully deductible up to CHF 5,000 in Zürich
            4. **Consider further education**: Job-related courses up to CHF 12,000 are deductible
            5. **Review insurance premiums**: Health insurance premiums are deductible (up to CHF 1,700 for single persons)

            💰 **Estimated savings potential**: {format_chf(0)} *(detailed analysis coming soon)*
            """)

        with tab3:
            st.subheader("ℹ️ About This Tool")
            st.markdown(f"""
            This Swiss Tax Deduction Analyzer helps you:
            - Calculate federal, cantonal, and municipal taxes for Zürich
            - Identify all available tax deductions
            - Understand automatic (pauschal) deductions that require no proof
            - Optimize your tax burden with actionable suggestions

            **Tax Year:** {TAX_YEAR}
            **Target Audience:** Single, employed individuals in Zürich canton
            **Data Sources:** SchmittTreuhand tax guide, Swiss federal tax law

            **Note:** This tool provides estimates for informational purposes. Always consult with a tax professional for official tax returns.

            ---

            ### Automatic Deductions (No Proof Required)
            These deductions are calculated automatically and don't require documentation:

            - **Professional Expenses**: 3% of salary (min CHF 2,000, max CHF 4,000)
            - **Meal Expenses**: CHF 15/day without subsidy, CHF 7.50/day with subsidy
            - **Bicycle Commuting**: CHF 700/year pauschal

            ### Proof-Required Deductions
            These deductions require receipts or certificates:

            - **Public Transport**: Actual costs up to CHF 5,000 (Zürich)
            - **Insurance Premiums**: Health, accident, life insurance (Säule 3b)
            - **Pillar 3a**: Official contribution certificate required
            - **Further Education**: Receipts for job-related courses
            - **Charitable Donations**: Donation receipts from tax-exempt organizations
            """)

    else:
        # Welcome message
        st.info("👈 Enter your information in the sidebar and click **Calculate Taxes** to see your tax breakdown.")

        # Example
        st.markdown("""
        ### How It Works:

        1. **Enter Your Information**: Input your salary, employment percentage, and municipality in the sidebar
        2. **Add Deductions**: Specify your commuting costs, insurance premiums, Pillar 3a contributions, etc.
        3. **Calculate**: Click the "Calculate Taxes" button to see your complete tax breakdown
        4. **Optimize**: Review suggestions to reduce your tax burden

        ### Example Calculation:

        For a single person earning **CHF 80,000/year** in Zürich City:
        - Federal Tax: ~CHF 2,400
        - Cantonal Tax: ~CHF 4,800
        - Municipal Tax: ~CHF 5,700
        - **Total Tax: ~CHF 12,900** (16.1% effective rate)
        - **Net Annual Income: ~CHF 62,500** (after taxes and social security)

        *Actual amounts depend on deductions claimed*
        """)


if __name__ == "__main__":
    main()
