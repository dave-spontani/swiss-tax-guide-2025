"""
Step 2: Automatic Deductions Review
Shows what automatic deductions the user gets based on their profile
"""
import streamlit as st
from models.tax_data import UserProfile, DeductionResult
from calculations.deductions import calculate_automatic_deductions, calculate_insurance_premium_limit
from utils.formatters import format_currency


def render_automatic_deductions(profile: UserProfile) -> tuple[DeductionResult, float]:
    """
    Render automatic deductions review and insurance premium input.

    Args:
        profile: User profile from Step 1

    Returns:
        Tuple of (DeductionResult with automatic deductions, insurance premium amount)
    """
    st.header("Step 2: Your Automatic Deductions")
    st.caption("These are deductions you get automatically without receipts")

    # Calculate automatic deductions
    deductions = calculate_automatic_deductions(profile)

    # Display automatic deductions in a nice box
    st.success("Based on your answers, you automatically get these deductions:")

    # Create a table-like display
    deduction_items = []

    if deductions.commuting_pauschal > 0:
        deduction_items.append(("Commuting costs", deductions.commuting_pauschal, "Pauschal, no receipts"))

    if deductions.meal_costs_pauschal > 0:
        meal_note = f"{'With' if profile.employer_meal_subsidy else 'Without'} employer subsidy"
        deduction_items.append(("Meal costs", deductions.meal_costs_pauschal, meal_note))

    if deductions.professional_expenses > 0:
        deduction_items.append(("Professional expenses", deductions.professional_expenses, "3% of salary"))

    if deductions.side_income_deduction > 0:
        deduction_items.append(("Side income deduction", deductions.side_income_deduction, "20% or max"))

    if deductions.child_deductions > 0:
        deduction_items.append((
            f"Child deductions ({profile.num_children} {'child' if profile.num_children == 1 else 'children'})",
            deductions.child_deductions,
            f"{format_currency(deductions.child_deductions / profile.num_children)} per child"
        ))

    if deductions.property_maintenance > 0:
        deduction_items.append(("Property maintenance", deductions.property_maintenance, "20% of Eigenmietwert"))

    if deductions.asset_management > 0:
        deduction_items.append(("Asset management", deductions.asset_management, "3‰ of securities"))

    if deductions.dual_income_deduction > 0:
        deduction_items.append(("Dual income deduction", deductions.dual_income_deduction, "Both spouses working"))

    # Display as table
    if deduction_items:
        for item, amount, note in deduction_items:
            col1, col2, col3 = st.columns([3, 2, 3])
            with col1:
                st.write(f"✓ {item}")
            with col2:
                st.write(f"**{format_currency(amount)}**")
            with col3:
                st.caption(note)

        st.divider()
        col1, col2 = st.columns(2)
        with col2:
            st.metric("Total Automatic Deductions", format_currency(deductions.total_automatic))
    else:
        st.info("No automatic deductions apply based on your profile")

    # Insurance premiums section (not pauschal but commonly claimed)
    st.subheader("Insurance Premiums")
    st.caption("Enter your annual insurance premiums (no receipts needed for tax return)")

    insurance_limit = calculate_insurance_premium_limit(profile)

    insurance_amount = st.number_input(
        "Total Insurance Premiums (CHF/year)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Health insurance, accident insurance, life insurance (Säule 3b)"
    )

    deductions.insurance_premiums = min(insurance_amount, insurance_limit)

    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"Maximum deductible: {format_currency(insurance_limit)}")
    with col2:
        if insurance_amount > insurance_limit:
            st.warning(f"Amount exceeds limit. Only {format_currency(insurance_limit)} will be deducted.")
        elif insurance_amount > 0:
            remaining = insurance_limit - insurance_amount
            st.info(f"Remaining room: {format_currency(remaining)}")

    # Recalculate totals with insurance
    deductions.calculate_totals()

    # Option to claim higher amounts
    st.divider()
    st.subheader("Want to Claim Higher Amounts?")
    st.caption("You can claim actual costs instead of pauschal amounts if they're higher (requires receipts)")

    claim_higher = st.expander("Click here to claim actual costs for specific deductions")

    with claim_higher:
        # Commuting
        if deductions.commuting_pauschal > 0:
            profile.claim_actual_commuting = st.checkbox(
                f"I have actual commuting costs > {format_currency(deductions.commuting_pauschal)}",
                value=profile.claim_actual_commuting,
                help="Need receipts/justification for actual costs"
            )

            if profile.claim_actual_commuting:
                # Default to pauschal + 300 if no actual costs set yet
                default_commuting = profile.actual_commuting_costs if profile.actual_commuting_costs > deductions.commuting_pauschal else (deductions.commuting_pauschal + 300)

                profile.actual_commuting_costs = st.number_input(
                    "Actual commuting costs (CHF/year)",
                    min_value=float(deductions.commuting_pauschal),
                    value=float(default_commuting),
                    step=100.0,
                    help="Enter your actual annual commuting costs (must be higher than pauschal to claim)"
                )
                st.caption("📄 Requires: Travel logs, public transport tickets, or car justification")

        # Professional expenses
        if deductions.professional_expenses > 0:
            profile.claim_actual_professional = st.checkbox(
                f"I have actual professional expenses > {format_currency(deductions.professional_expenses)}",
                value=profile.claim_actual_professional,
                help="Need receipts for actual costs"
            )

            if profile.claim_actual_professional:
                # Default to pauschal + 1000 if no actual costs set yet
                default_professional = profile.actual_professional_costs if profile.actual_professional_costs > deductions.professional_expenses else (deductions.professional_expenses + 1000)

                profile.actual_professional_costs = st.number_input(
                    "Actual professional expenses (CHF/year)",
                    min_value=float(deductions.professional_expenses),
                    value=float(default_professional),
                    step=100.0,
                    help="Enter your actual annual professional expenses (must be higher than pauschal to claim)"
                )
                st.caption("📄 Requires: Receipts for work tools, computer, home office, etc.")

        # Property maintenance
        if deductions.property_maintenance > 0:
            profile.claim_actual_property_maintenance = st.checkbox(
                f"I have actual property maintenance costs > {format_currency(deductions.property_maintenance)}",
                value=profile.claim_actual_property_maintenance,
                help="Need receipts for actual maintenance costs"
            )

            if profile.claim_actual_property_maintenance:
                # Default to pauschal * 1.5 if no actual costs set yet
                default_property = profile.actual_property_maintenance_costs if profile.actual_property_maintenance_costs > deductions.property_maintenance else (deductions.property_maintenance * 1.5)

                profile.actual_property_maintenance_costs = st.number_input(
                    "Actual property maintenance costs (CHF/year)",
                    min_value=float(deductions.property_maintenance),
                    value=float(default_property),
                    step=1000.0,
                    help="Enter your actual annual property maintenance costs (must be higher than pauschal to claim)"
                )
                st.caption("📄 Requires: Invoices for repairs, maintenance, renovations")

    # Recalculate with actual costs if claimed
    if any([profile.claim_actual_commuting, profile.claim_actual_professional, profile.claim_actual_property_maintenance]):
        deductions = calculate_automatic_deductions(profile)
        deductions.insurance_premiums = min(insurance_amount, insurance_limit)
        deductions.calculate_totals()

        st.info(f"Updated total with actual costs: {format_currency(deductions.total_automatic)}")

    return deductions, insurance_amount
