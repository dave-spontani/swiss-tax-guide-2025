"""
Swiss Tax Deduction Questionnaire + Calculator
Streamlit application for calculating Swiss taxes with smart deduction guidance
"""
import streamlit as st
from ui.wizard import init_wizard_state, render_progress_bar, render_navigation_buttons, restart_wizard
from questionnaire.qualifying_questions import render_qualifying_questions
from questionnaire.automatic_deductions import render_automatic_deductions
from questionnaire.optional_deductions import render_optional_deductions
from ui.tax_comparison import render_tax_comparison
from ui.optimization import render_optimization_tools
from utils.formatters import format_currency, format_percent
import pandas as pd


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Swiss Tax Calculator - Zurich",
        page_icon="🇨🇭",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Initialize wizard state
    init_wizard_state()

    # Header
    st.title("🇨🇭 Swiss Tax Calculator - Zürich")
    st.caption("Smart tax deduction questionnaire with automatic and optional deductions")

    # Progress bar
    render_progress_bar(st.session_state.wizard_step)

    st.divider()

    # Render current step
    if st.session_state.wizard_step == 1:
        # Step 1: Qualifying Questions
        st.session_state.profile = render_qualifying_questions(st.session_state.profile)

    elif st.session_state.wizard_step == 2:
        # Step 2: Automatic Deductions Review
        deductions, insurance = render_automatic_deductions(st.session_state.profile)
        st.session_state.deductions = deductions

    elif st.session_state.wizard_step == 3:
        # Step 3: Optional Deductions
        st.session_state.deductions = render_optional_deductions(
            st.session_state.profile,
            st.session_state.deductions
        )

    elif st.session_state.wizard_step == 4:
        # Step 4: Tax Results
        comparison, final_tax_result = render_tax_comparison(
            st.session_state.profile,
            st.session_state.deductions
        )

        # Combined Overview for Married Couples
        if st.session_state.profile.marital_status == 'married':
            st.divider()
            render_combined_overview(st.session_state.profile, st.session_state.deductions)

        # Detailed Breakdowns
        st.divider()
        st.header("Detailed Breakdown")

        tab1, tab2, tab3 = st.tabs(["Deductions", "Tax Brackets", "Optimization"])

        with tab1:
            render_deductions_breakdown(st.session_state.deductions)

        with tab2:
            render_bracket_breakdown(final_tax_result, st.session_state.profile)

        with tab3:
            render_optimization_tools(st.session_state.profile, st.session_state.deductions)

        # Restart button
        st.divider()
        if st.button("🔄 Start Over", type="secondary"):
            restart_wizard()

    # Navigation buttons
    st.divider()
    render_navigation_buttons(st.session_state.wizard_step)

    # Footer
    render_footer()


def render_combined_overview(profile, deductions):
    """Render combined overview for married couples showing totals."""
    st.header("💰 Combined Household Overview")
    st.caption("Summary of combined accounts and contributions for both persons")

    # Income Section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 💵 Income")
        st.metric("Person 1", format_currency(profile.spouse1_net_salary))
        st.metric("Person 2", format_currency(profile.spouse2_net_salary))
        combined_income = profile.spouse1_net_salary + profile.spouse2_net_salary
        st.metric("Combined Income", format_currency(combined_income),
                 label_visibility="visible")

    # Insurance Section
    with col2:
        st.markdown("### 🏥 Insurance Premiums")
        st.metric("Person 1", format_currency(profile.spouse1_insurance_premiums))
        st.metric("Person 2", format_currency(profile.spouse2_insurance_premiums))
        combined_insurance = profile.spouse1_insurance_premiums + profile.spouse2_insurance_premiums
        st.metric("Combined Insurance", format_currency(combined_insurance),
                 label_visibility="visible")

    # Investments Section
    with col3:
        st.markdown("### 📈 Investments")
        st.metric("Person 1 Securities", format_currency(profile.spouse1_securities_value))
        st.metric("Person 2 Securities", format_currency(profile.spouse2_securities_value))
        combined_securities = profile.spouse1_securities_value + profile.spouse2_securities_value
        st.metric("Combined Securities", format_currency(combined_securities),
                 label_visibility="visible")

    st.divider()

    # Wealth Section
    st.markdown("### 💎 Net Wealth")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Person 1 Wealth", format_currency(profile.spouse1_wealth))
    with col2:
        st.metric("Person 2 Wealth", format_currency(profile.spouse2_wealth))
    with col3:
        combined_wealth = profile.spouse1_wealth + profile.spouse2_wealth
        st.metric("Combined Net Wealth", format_currency(combined_wealth),
                 help="Total assets minus liabilities for both persons")

    st.divider()

    # Pension Contributions Section
    st.markdown("### 🏦 Pension Contributions")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Person 1**")
        st.metric("Pillar 3a", format_currency(profile.spouse1_pillar_3a))
        st.metric("Pillar 2 Buy-ins", format_currency(profile.spouse1_pillar_2_buyins))

    with col2:
        st.markdown("**Person 2**")
        st.metric("Pillar 3a", format_currency(profile.spouse2_pillar_3a))
        st.metric("Pillar 2 Buy-ins", format_currency(profile.spouse2_pillar_2_buyins))

    with col3:
        st.markdown("**Combined**")
        combined_3a = profile.spouse1_pillar_3a + profile.spouse2_pillar_3a
        combined_p2 = profile.spouse1_pillar_2_buyins + profile.spouse2_pillar_2_buyins
        st.metric("Total Pillar 3a", format_currency(combined_3a))
        st.metric("Total Pillar 2", format_currency(combined_p2))

    # Summary Box
    st.divider()
    with st.container(border=True):
        st.markdown("### 📊 Household Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Combined Totals:**")
            st.write(f"• Total Income: **{format_currency(combined_income)}**")
            st.write(f"• Total Insurance: **{format_currency(combined_insurance)}**")
            st.write(f"• Total Securities: **{format_currency(combined_securities)}**")
            st.write(f"• Total Wealth: **{format_currency(combined_wealth)}**")
            combined_3a = profile.spouse1_pillar_3a + profile.spouse2_pillar_3a
            combined_p2 = profile.spouse1_pillar_2_buyins + profile.spouse2_pillar_2_buyins
            if combined_3a > 0 or combined_p2 > 0:
                st.write(f"• Total Pillar 3a: **{format_currency(combined_3a)}**")
                st.write(f"• Total Pillar 2: **{format_currency(combined_p2)}**")

        with col2:
            st.markdown("**Total Deductions:**")
            st.write(f"• Automatic: **{format_currency(deductions.total_automatic)}**")
            st.write(f"• Optional: **{format_currency(deductions.total_optional)}**")
            if deductions.pillar_3a > 0:
                st.write(f"  - Pillar 3a: {format_currency(deductions.pillar_3a)}")
            if deductions.pillar_2_buyins > 0:
                st.write(f"  - Pillar 2: {format_currency(deductions.pillar_2_buyins)}")
            st.write(f"• **Total: {format_currency(deductions.total_deductions)}**")


def render_deductions_breakdown(deductions):
    """Render detailed deductions breakdown."""
    st.subheader("Deductions Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Automatic Deductions")
        auto_items = []

        if deductions.commuting_pauschal > 0:
            # Check if commuting exceeds limits
            from models.constants import COMMUTING_MAX_FEDERAL, COMMUTING_MAX_CANTONAL
            if deductions.commuting_pauschal > COMMUTING_MAX_FEDERAL:
                note = f"Fed max: CHF {COMMUTING_MAX_FEDERAL:,} | Cant max: CHF {COMMUTING_MAX_CANTONAL:,}"
            else:
                note = "No receipts"
            auto_items.append(("Commuting", deductions.commuting_pauschal, note))
        if deductions.meal_costs_pauschal > 0:
            auto_items.append(("Meals", deductions.meal_costs_pauschal, "No receipts"))
        if deductions.professional_expenses > 0:
            auto_items.append(("Professional expenses", deductions.professional_expenses, "3% of salary"))
        if deductions.side_income_deduction > 0:
            auto_items.append(("Side income", deductions.side_income_deduction, "20% or max"))
        if deductions.child_deductions > 0:
            auto_items.append(("Children", deductions.child_deductions, "No receipts"))
        if deductions.property_maintenance > 0:
            auto_items.append(("Property", deductions.property_maintenance, "20% pauschal"))
        if deductions.asset_management > 0:
            auto_items.append(("Asset mgmt", deductions.asset_management, "3‰ pauschal"))
        if deductions.insurance_premiums > 0:
            auto_items.append(("Insurance", deductions.insurance_premiums, "Up to limit"))
        if deductions.dual_income_deduction > 0:
            auto_items.append(("Dual income", deductions.dual_income_deduction, "No receipts"))

        if auto_items:
            auto_df = pd.DataFrame(auto_items, columns=['Type', 'Amount', 'Notes'])
            auto_df['Amount'] = auto_df['Amount'].apply(format_currency)
            st.dataframe(auto_df, hide_index=True, use_container_width=True)
            st.metric("Total Automatic", format_currency(deductions.total_automatic))

            # Show info about commuting caps if exceeded
            from models.constants import COMMUTING_MAX_FEDERAL, COMMUTING_MAX_CANTONAL
            if deductions.commuting_pauschal > COMMUTING_MAX_FEDERAL:
                st.info(f"""
                ℹ️ **Commuting cost caps applied:**
                - Your commuting costs: {format_currency(deductions.commuting_pauschal)}
                - Federal tax deduction: {format_currency(min(deductions.commuting_pauschal, COMMUTING_MAX_FEDERAL))} (max)
                - Cantonal tax deduction: {format_currency(min(deductions.commuting_pauschal, COMMUTING_MAX_CANTONAL))} (max)
                """)
        else:
            st.info("No automatic deductions")

    with col2:
        st.markdown("#### Optional Deductions")
        opt_items = []

        if deductions.pillar_3a > 0:
            opt_items.append(("Pillar 3a", deductions.pillar_3a, "Certificate required"))
        if deductions.pillar_2_buyins > 0:
            opt_items.append(("Pillar 2 buy-ins", deductions.pillar_2_buyins, "Confirmation required"))
        if deductions.mortgage_interest > 0:
            opt_items.append(("Mortgage interest", deductions.mortgage_interest, "Bank statement"))
        if deductions.other_debt_interest > 0:
            opt_items.append(("Other debt interest", deductions.other_debt_interest, "Loan statement"))
        if deductions.medical_costs_deductible > 0:
            opt_items.append(("Medical costs", deductions.medical_costs_deductible, "Receipts required"))
        if deductions.childcare_costs > 0:
            opt_items.append(("Childcare", deductions.childcare_costs, "Invoices required"))
        if deductions.donations > 0:
            opt_items.append(("Donations", deductions.donations, "Receipts required"))
        if deductions.political_contributions > 0:
            opt_items.append(("Political", deductions.political_contributions, "Receipts required"))
        if deductions.alimony_payments > 0:
            opt_items.append(("Alimony", deductions.alimony_payments, "Decree + receipts"))
        if deductions.support_payments > 0:
            opt_items.append(("Support", deductions.support_payments, "Receipts required"))

        if opt_items:
            opt_df = pd.DataFrame(opt_items, columns=['Type', 'Amount', 'Documentation'])
            opt_df['Amount'] = opt_df['Amount'].apply(format_currency)
            st.dataframe(opt_df, hide_index=True, use_container_width=True)
            st.metric("Total Optional", format_currency(deductions.total_optional))
        else:
            st.info("No optional deductions")


def render_bracket_breakdown(tax_result, profile):
    """Render tax bracket breakdown."""
    st.subheader("Tax Bracket Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Federal Tax Brackets")
        if tax_result.federal_breakdown:
            fed_data = []
            for b in tax_result.federal_breakdown:
                fed_data.append({
                    'Bracket': f"{format_currency(b['range_start'])} - {format_currency(b['range_end']) if b['range_end'] != float('inf') else '∞'}",
                    'Rate': f"{b['rate']:.2f}%",
                    'Income': format_currency(b['taxable_amount']),
                    'Tax': format_currency(b['tax_paid']),
                    'Active': '✓' if b['is_active'] else ''
                })
            fed_df = pd.DataFrame(fed_data)
            st.dataframe(fed_df, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("#### Cantonal Tax Brackets (Zurich)")
        if tax_result.cantonal_breakdown:
            cant_data = []
            for b in tax_result.cantonal_breakdown:
                cant_data.append({
                    'Bracket': f"{format_currency(b['range_start'])} - {format_currency(b['range_end']) if b['range_end'] != float('inf') else '∞'}",
                    'Rate': f"{b['rate']}%",
                    'Income': format_currency(b['taxable_amount']),
                    'Einfache': format_currency(b['tax_paid']),
                    'Active': '✓' if b['is_active'] else ''
                })
            cant_df = pd.DataFrame(cant_data)
            st.dataframe(cant_df, hide_index=True, use_container_width=True)

    # Progress in current bracket
    if tax_result.amount_to_next_bracket > 0:
        st.divider()
        st.subheader("Bracket Progress")
        st.progress(tax_result.progress_in_bracket / 100)
        st.caption(f"{format_currency(tax_result.amount_to_next_bracket)} to next bracket")

    # Wealth Tax Breakdown (if applicable)
    if profile.total_wealth > 0:
        st.divider()
        st.subheader("Wealth Tax Breakdown")

        from calculations.wealth_tax import calculate_wealth_tax
        from models.constants import WEALTH_DEDUCTION_PER_CHILD

        wealth_result = calculate_wealth_tax(
            profile.total_wealth,
            profile.num_children,
            profile.gemeinde_steuerfuss,
            profile.marital_status
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Wealth", format_currency(profile.total_wealth))
            st.caption("Assets minus liabilities")

        with col2:
            st.metric("Wealth Deductions", format_currency(wealth_result['deductions']))
            if profile.num_children > 0:
                st.caption(f"{profile.num_children} × {format_currency(WEALTH_DEDUCTION_PER_CHILD)}")
            else:
                st.caption("No per-adult deductions in ZH")

        with col3:
            st.metric("Taxable Wealth", format_currency(wealth_result['taxable_wealth']))
            st.caption(f"Effective rate: {format_percent(wealth_result['effective_rate'])}")

        if wealth_result['wealth_tax'] > 0:
            st.divider()
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Cantonal Wealth Tax", format_currency(wealth_result['cantonal_wealth_tax']))
                st.caption(f"Cantonal Steuerfuss: 98%")

            with col2:
                st.metric("Municipal Wealth Tax", format_currency(wealth_result['municipal_wealth_tax']))
                st.caption(f"Municipal Steuerfuss: {profile.gemeinde_steuerfuss}%")

            with col3:
                st.metric("Total Wealth Tax", format_currency(wealth_result['wealth_tax']))
        else:
            st.info("✓ No wealth tax payable (below threshold)")


def render_footer():
    """Render application footer."""
    st.divider()
    st.caption("""
    **Sources:**
    - Federal tax: [DBG Art. 36](https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de)
    - Cantonal tax: [StG § 35 (ZH)](https://www.zh.ch/de/steuern-finanzen/steuern/treuhaender/steuerbuch/)
    - Deductions: Schmitt Treuhand Tax Guide 2024

    **Disclaimer:** Tax calculations are estimates based on 2024/2025 rates and standard deductions.
    Actual tax liability may differ. Consult official sources and tax professionals for exact calculations.
    """)


if __name__ == "__main__":
    main()
