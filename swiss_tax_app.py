import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Swiss Tax Guide 2025",
    page_icon="🇨🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #DC143C;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin-top: 2rem;
    }
    .highlight-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #DC143C;
    }
    .tax-tip {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #0066cc;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🇨🇭 Swiss Tax Guide 2025")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Tax Calculator", "Canton Comparison", "Deductions Checklist",
     "Pillar 3a Guide", "Investment Income", "Real Estate Tax"]
)

# Canton data
canton_data = {
    "Canton": ["Zug", "Schwyz", "Appenzell Innerrhoden", "Nidwalden", "Obwalden",
               "Uri", "Lucerne", "Schaffhausen", "Appenzell Ausserrhoden", "Glarus",
               "Thurgau", "St. Gallen", "Graubünden", "Solothurn", "Aargau",
               "Fribourg", "Neuchâtel", "Jura", "Valais", "Zurich",
               "Ticino", "Basel-Stadt", "Bern", "Vaud", "Basel-Landschaft", "Geneva"],
    "Capital": ["Zug", "Schwyz", "Appenzell", "Stans", "Sarnen",
                "Altdorf", "Lucerne", "Schaffhausen", "Herisau", "Glarus",
                "Frauenfeld", "St. Gallen", "Chur", "Solothurn", "Aarau",
                "Fribourg", "Neuchâtel", "Delémont", "Sion", "Zurich",
                "Bellinzona", "Basel", "Bern", "Lausanne", "Liestal", "Geneva"],
    "Max_Tax_Rate": [22.2, 22.59, 23.8, 24.3, 24.3,
                     25.3, 30.6, 30.0, 30.7, 31.1,
                     31.7, 32.8, 32.2, 33.7, 34.5,
                     35.3, 36.0, 36.0, 36.5, 39.8,
                     40.1, 40.5, 41.2, 41.5, 42.2, 45.0],
    "Wealth_Tax_Min": [0.14, 0.15, 0.25, 0.10, 0.20,
                       0.25, 0.30, 0.28, 0.30, 0.28,
                       0.30, 0.32, 0.30, 0.35, 0.33,
                       0.38, 0.40, 0.40, 0.35, 0.38,
                       0.42, 0.45, 0.40, 0.64, 0.50, 0.50],
    "Wealth_Tax_Max": [0.21, 0.30, 0.35, 0.10, 0.25,
                       0.30, 0.45, 0.35, 0.40, 0.35,
                       0.40, 0.45, 0.40, 0.50, 0.45,
                       0.50, 0.55, 0.55, 0.50, 0.55,
                       0.60, 0.65, 0.60, 0.76, 0.88, 0.75]
}

df_cantons = pd.DataFrame(canton_data)

# Federal tax brackets (single)
def calculate_federal_tax_single(income):
    """Calculate federal tax for single taxpayers"""
    if income <= 15200:
        return 0
    elif income < 18500:
        return 0  # Below collection threshold
    elif income <= 32800:
        return (income - 15000) * 0.0077
    elif income <= 42900:
        return 137.05 + (income - 32800) * 0.0088
    elif income <= 57200:
        return 225.90 + (income - 42900) * 0.0264
    elif income <= 793400:
        # Progressive rates - simplified approximation
        base_tax = 603.40
        excess = income - 57200
        return base_tax + excess * 0.0297  # Approximation
    else:
        return income * 0.115  # Maximum rate

def calculate_federal_tax_married(income):
    """Calculate federal tax for married couples using splitting"""
    if income <= 29700:
        return 0
    elif income < 32200:
        return 0  # Below collection threshold

    # Income splitting
    half_income = income / 2
    single_tax = calculate_federal_tax_single(half_income)
    return single_tax * 2

# HOME PAGE
if page == "Home":
    st.markdown('<h1 class="main-header">🇨🇭 Complete Swiss Tax Guide 2025</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="highlight-box">
        <h3>📊 Key Facts</h3>
        <ul>
        <li>3-tier tax system</li>
        <li>Federal max: <strong>11.5%</strong></li>
        <li>Total: <strong>22-45%</strong></li>
        <li>26 different cantons</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="highlight-box">
        <h3>💰 Best Cantons</h3>
        <ul>
        <li>Zug: <strong>22.2%</strong></li>
        <li>Schwyz: <strong>22.59%</strong></li>
        <li>Nidwalden: <strong>24.3%</strong></li>
        <li>Obwalden: <strong>24.3%</strong></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="highlight-box">
        <h3>🎯 Tax Optimization</h3>
        <ul>
        <li>Pillar 3a: <strong>CHF 7,258</strong></li>
        <li>Capital gains: <strong>Tax-free</strong></li>
        <li>Wealth tax: <strong>0.1-0.88%</strong></li>
        <li>Deductions matter!</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick comparison chart
    st.subheader("📈 Canton Tax Rates Comparison")

    fig = px.bar(
        df_cantons.sort_values('Max_Tax_Rate'),
        x='Canton',
        y='Max_Tax_Rate',
        color='Max_Tax_Rate',
        color_continuous_scale=['green', 'yellow', 'red'],
        title='Maximum Tax Rates by Canton (Federal + Cantonal + Municipal)',
        labels={'Max_Tax_Rate': 'Tax Rate (%)', 'Canton': 'Canton'}
    )
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Quick tips
    st.markdown("---")
    st.subheader("⚡ Top 5 Tax Tips for 2025")

    tips = [
        "**Maximize Pillar 3a**: Contribute CHF 7,258 before Dec 31 for full deduction",
        "**Capital Gains are Tax-Free**: Hold investments 6+ months as private investor",
        "**Don't Forget Small Deductions**: Meal costs (CHF 15/meal), asset management fees (3‰)",
        "**Plan Location**: Moving cantons can save 10-20% in taxes annually",
        "**Eigenmietwert Reform**: Major changes to homeowner taxation coming in 2028"
    ]

    for i, tip in enumerate(tips, 1):
        st.markdown(f'<div class="tax-tip"><strong>{i}.</strong> {tip}</div>', unsafe_allow_html=True)

# TAX CALCULATOR PAGE
elif page == "Tax Calculator":
    st.markdown('<h1 class="main-header">💰 Swiss Tax Calculator 2025</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Your Information")

        marital_status = st.selectbox(
            "Marital Status",
            ["Single", "Married/Registered Partnership"]
        )

        gross_income = st.number_input(
            "Gross Annual Income (CHF)",
            min_value=0,
            max_value=5000000,
            value=100000,
            step=5000
        )

        selected_canton = st.selectbox(
            "Canton of Residence",
            df_cantons['Canton'].tolist()
        )

        st.subheader("Deductions")

        pillar_3a = st.number_input(
            "Pillar 3a Contribution (CHF)",
            min_value=0,
            max_value=7258,
            value=7258,
            help="Maximum CHF 7,258 for employees with 2nd pillar"
        )

        pillar_2_buyback = st.number_input(
            "Pillar 2 Buyback (CHF)",
            min_value=0,
            max_value=500000,
            value=0
        )

        other_deductions = st.number_input(
            "Other Deductions (CHF)",
            min_value=0,
            max_value=200000,
            value=10000,
            help="Health insurance, professional expenses, etc."
        )

    with col2:
        st.subheader("Tax Calculation Results")

        # Calculate taxable income
        total_deductions = pillar_3a + pillar_2_buyback + other_deductions
        taxable_income = max(0, gross_income - total_deductions)

        # Calculate federal tax
        if marital_status == "Single":
            federal_tax = calculate_federal_tax_single(taxable_income)
        else:
            federal_tax = calculate_federal_tax_married(taxable_income)

        # Get canton tax rate
        canton_info = df_cantons[df_cantons['Canton'] == selected_canton].iloc[0]
        canton_rate = canton_info['Max_Tax_Rate']

        # Estimate cantonal + municipal tax (approximate)
        cantonal_municipal_rate = canton_rate - 11.5  # Subtract federal max rate
        cantonal_municipal_tax = taxable_income * (cantonal_municipal_rate / 100)

        total_tax = federal_tax + cantonal_municipal_tax
        effective_rate = (total_tax / gross_income * 100) if gross_income > 0 else 0
        net_income = gross_income - total_tax

        # Display results
        st.markdown(f"""
        <div class="highlight-box">
        <h3>💵 Tax Summary</h3>
        <table style="width:100%">
        <tr><td><strong>Gross Income:</strong></td><td style="text-align:right">CHF {gross_income:,.2f}</td></tr>
        <tr><td><strong>Total Deductions:</strong></td><td style="text-align:right">- CHF {total_deductions:,.2f}</td></tr>
        <tr><td><strong>Taxable Income:</strong></td><td style="text-align:right">CHF {taxable_income:,.2f}</td></tr>
        <tr><td colspan="2"><hr></td></tr>
        <tr><td><strong>Federal Tax:</strong></td><td style="text-align:right">CHF {federal_tax:,.2f}</td></tr>
        <tr><td><strong>Cantonal + Municipal Tax:</strong></td><td style="text-align:right">CHF {cantonal_municipal_tax:,.2f}</td></tr>
        <tr><td><strong style="font-size:1.2em; color:#DC143C">Total Tax:</strong></td><td style="text-align:right; font-size:1.2em; color:#DC143C"><strong>CHF {total_tax:,.2f}</strong></td></tr>
        <tr><td colspan="2"><hr></td></tr>
        <tr><td><strong>Effective Tax Rate:</strong></td><td style="text-align:right">{effective_rate:.2f}%</td></tr>
        <tr><td><strong style="font-size:1.2em; color:green">Net Income:</strong></td><td style="text-align:right; font-size:1.2em; color:green"><strong>CHF {net_income:,.2f}</strong></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

        # Tax breakdown chart
        st.subheader("Tax Breakdown")

        breakdown_data = pd.DataFrame({
            'Category': ['Federal Tax', 'Cantonal/Municipal Tax', 'Net Income'],
            'Amount': [federal_tax, cantonal_municipal_tax, net_income]
        })

        fig = px.pie(
            breakdown_data,
            values='Amount',
            names='Category',
            color_discrete_sequence=['#DC143C', '#FF6B6B', '#4CAF50']
        )
        st.plotly_chart(fig, use_container_width=True)

        # Savings from deductions
        st.info(f"""
        **💡 Tax Savings**: Your deductions of CHF {total_deductions:,.2f}
        saved you approximately CHF {total_deductions * (canton_rate/100):,.2f} in taxes!
        """)

# CANTON COMPARISON PAGE
elif page == "Canton Comparison":
    st.markdown('<h1 class="main-header">🗺️ Canton Tax Comparison</h1>', unsafe_allow_html=True)

    st.subheader("Compare Tax Rates Across All 26 Cantons")

    # Interactive table
    st.dataframe(
        df_cantons.style.background_gradient(subset=['Max_Tax_Rate'], cmap='RdYlGn_r')
                       .background_gradient(subset=['Wealth_Tax_Min', 'Wealth_Tax_Max'], cmap='RdYlGn_r')
                       .format({
                           'Max_Tax_Rate': '{:.2f}%',
                           'Wealth_Tax_Min': '{:.2f}%',
                           'Wealth_Tax_Max': '{:.2f}%'
                       }),
        use_container_width=True,
        height=600
    )

    st.markdown("---")

    # Comparison selector
    st.subheader("📊 Compare Specific Cantons")

    selected_cantons = st.multiselect(
        "Select cantons to compare (2-5)",
        df_cantons['Canton'].tolist(),
        default=['Zug', 'Zurich', 'Geneva']
    )

    if len(selected_cantons) >= 2:
        comparison_df = df_cantons[df_cantons['Canton'].isin(selected_cantons)]

        col1, col2 = st.columns(2)

        with col1:
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=comparison_df['Canton'],
                y=comparison_df['Max_Tax_Rate'],
                name='Max Tax Rate',
                marker_color='indianred'
            ))
            fig1.update_layout(
                title='Income Tax Rates Comparison',
                yaxis_title='Tax Rate (%)',
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=comparison_df['Canton'],
                y=comparison_df['Wealth_Tax_Max'],
                name='Wealth Tax',
                marker_color='lightseagreen'
            ))
            fig2.update_layout(
                title='Wealth Tax Rates Comparison',
                yaxis_title='Wealth Tax (%)',
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Tax savings comparison
        st.subheader("💰 Potential Savings Calculator")

        income_for_comparison = st.slider(
            "Annual Income (CHF)",
            min_value=50000,
            max_value=500000,
            value=150000,
            step=10000
        )

        savings_data = []
        for canton in selected_cantons:
            rate = df_cantons[df_cantons['Canton'] == canton]['Max_Tax_Rate'].values[0]
            estimated_tax = income_for_comparison * (rate / 100)
            savings_data.append({
                'Canton': canton,
                'Estimated Tax': estimated_tax,
                'Net Income': income_for_comparison - estimated_tax
            })

        savings_df = pd.DataFrame(savings_data).sort_values('Estimated Tax')

        st.dataframe(
            savings_df.style.format({
                'Estimated Tax': 'CHF {:,.2f}',
                'Net Income': 'CHF {:,.2f}'
            }),
            use_container_width=True
        )

        # Calculate max savings
        max_tax = savings_df['Estimated Tax'].max()
        min_tax = savings_df['Estimated Tax'].min()
        potential_savings = max_tax - min_tax

        st.success(f"""
        **Maximum Potential Savings**: CHF {potential_savings:,.2f} per year
        By moving from {savings_df.iloc[-1]['Canton']} to {savings_df.iloc[0]['Canton']}
        """)

# DEDUCTIONS CHECKLIST PAGE
elif page == "Deductions Checklist":
    st.markdown('<h1 class="main-header">✅ Tax Deductions Checklist 2025</h1>', unsafe_allow_html=True)

    st.info("Use this checklist to ensure you're claiming all eligible deductions!")

    # Create tabs for different categories
    tab1, tab2, tab3, tab4 = st.tabs(["💼 Professional", "👨‍👩‍👧 Personal & Family", "🏠 Real Estate", "💎 Commonly Forgotten"])

    with tab1:
        st.subheader("Professional Expenses")

        prof_deductions = {
            "Commuting costs (public transport or distance-based)": False,
            "Meal expenses (CHF 15/meal without subsidy, CHF 7.50 with)": False,
            "Professional expenses flat-rate (3% of income, max CHF 4,000)": False,
            "Work equipment (tools, literature, professional clothing)": False,
            "Home office equipment": False,
            "Professional subscriptions and memberships": False,
            "Education costs (up to CHF 13,000 for post-secondary)": False,
            "Professional development and training": False,
        }

        total_prof = 0
        for item in prof_deductions:
            col1, col2 = st.columns([3, 1])
            with col1:
                checked = st.checkbox(item, key=f"prof_{item}")
            with col2:
                if checked:
                    amount = st.number_input("CHF", min_value=0, max_value=100000, value=0, key=f"amt_prof_{item}", label_visibility="collapsed")
                    total_prof += amount

        st.metric("Total Professional Deductions", f"CHF {total_prof:,.2f}")

    with tab2:
        st.subheader("Personal & Family Deductions")

        personal_deductions = {
            "Pillar 3a contributions (max CHF 7,258)": False,
            "Pillar 2 buybacks": False,
            "Health insurance premiums (actual costs)": False,
            "Life insurance premiums": False,
            "Childcare costs (up to CHF 25,800 federal)": False,
            "Alimony payments": False,
            "Double household costs (second residence for work)": False,
            "Child deduction (CHF 6,800 per child - federal)": False,
            "Married couple deduction (CHF 2,800 - federal)": False,
        }

        total_personal = 0
        for item in personal_deductions:
            col1, col2 = st.columns([3, 1])
            with col1:
                checked = st.checkbox(item, key=f"pers_{item}")
            with col2:
                if checked:
                    amount = st.number_input("CHF", min_value=0, max_value=100000, value=0, key=f"amt_pers_{item}", label_visibility="collapsed")
                    total_personal += amount

        st.metric("Total Personal Deductions", f"CHF {total_personal:,.2f}")

    with tab3:
        st.subheader("Real Estate Deductions (Until 2028 Reform)")

        st.warning("⚠️ Note: The Eigenmietwert system will be abolished around January 1, 2028")

        real_estate_deductions = {
            "Mortgage interest (fully deductible)": False,
            "Maintenance costs (actual or flat-rate 10-20%)": False,
            "Renovations (value-maintaining, not value-increasing)": False,
            "Energy efficiency improvements": False,
            "Property management fees": False,
        }

        total_re = 0
        for item in real_estate_deductions:
            col1, col2 = st.columns([3, 1])
            with col1:
                checked = st.checkbox(item, key=f"re_{item}")
            with col2:
                if checked:
                    amount = st.number_input("CHF", min_value=0, max_value=500000, value=0, key=f"amt_re_{item}", label_visibility="collapsed")
                    total_re += amount

        st.metric("Total Real Estate Deductions", f"CHF {total_re:,.2f}")

    with tab4:
        st.subheader("⭐ Commonly Forgotten Deductions")

        st.markdown("""
        <div class="tax-tip">
        <strong>💡 Pro Tip:</strong> These deductions are frequently overlooked but can add up to significant savings!
        </div>
        """, unsafe_allow_html=True)

        forgotten_deductions = {
            "Expected federal tax as debt (from wealth calculation)": False,
            "Asset management fees flat-rate (2-3‰ of portfolio)": False,
            "Political donations & party fees (up to CHF 10,600)": False,
            "Charitable donations (min CHF 100, max 20% of income)": False,
            "All loan interest (personal loans, credit cards, car loans)": False,
            "Property underutilization (unused room reduces Eigenmietwert)": False,
        }

        total_forgotten = 0
        for item in forgotten_deductions:
            col1, col2 = st.columns([3, 1])
            with col1:
                checked = st.checkbox(item, key=f"forg_{item}")
            with col2:
                if checked:
                    amount = st.number_input("CHF", min_value=0, max_value=50000, value=0, key=f"amt_forg_{item}", label_visibility="collapsed")
                    total_forgotten += amount

        st.metric("Total 'Forgotten' Deductions", f"CHF {total_forgotten:,.2f}")

    # Grand total
    st.markdown("---")
    grand_total = total_prof + total_personal + total_re + total_forgotten

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Deductions", f"CHF {grand_total:,.2f}")
    with col2:
        estimated_savings = grand_total * 0.30  # Approximate 30% tax rate
        st.metric("💰 Estimated Tax Savings", f"CHF {estimated_savings:,.2f}")
    with col3:
        st.metric("📅 Deadline", "December 31, 2025")

# PILLAR 3A GUIDE PAGE
elif page == "Pillar 3a Guide":
    st.markdown('<h1 class="main-header">🏦 Pillar 3a Optimization Guide</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("What is Pillar 3a?")
        st.markdown("""
        Pillar 3a is Switzerland's **#1 tax deduction** - a voluntary private pension plan with significant tax advantages:

        ✅ **100% tax deductible** from taxable income
        ✅ **Tax-free growth** - No income or wealth tax during investment
        ✅ **Compound interest amplified**
        ✅ Withdrawals taxed at **reduced separate rate** (much lower than income tax)
        """)

        st.subheader("2025 Contribution Limits")

        employment_status = st.radio(
            "Your Employment Status",
            ["Employed with 2nd pillar (pension fund)", "Self-employed without 2nd pillar"]
        )

        if employment_status == "Employed with 2nd pillar (pension fund)":
            max_contribution = 7258
            st.success(f"**Maximum 2025 Contribution: CHF {max_contribution:,}**")
        else:
            max_contribution = 36288
            st.success(f"""
            **Maximum 2025 Contribution: CHF {max_contribution:,}**
            (or 20% of net income, whichever is lower)
            """)

        st.markdown("---")

        st.subheader("💰 Calculate Your Tax Savings")

        your_contribution = st.slider(
            "Your Pillar 3a Contribution (CHF)",
            min_value=0,
            max_value=max_contribution,
            value=max_contribution,
            step=100
        )

        your_canton = st.selectbox(
            "Your Canton",
            df_cantons['Canton'].tolist(),
            key="pillar3a_canton"
        )

        canton_rate = df_cantons[df_cantons['Canton'] == your_canton]['Max_Tax_Rate'].values[0]

        tax_savings = your_contribution * (canton_rate / 100)

        st.markdown(f"""
        <div class="highlight-box">
        <h3>Your Estimated Tax Savings</h3>
        <p style="font-size: 2rem; color: green; text-align: center; margin: 20px 0;">
        <strong>CHF {tax_savings:,.2f}</strong>
        </p>
        <p style="text-align: center;">
        By contributing CHF {your_contribution:,} to Pillar 3a<br>
        (Based on {canton_rate}% tax rate in {your_canton})
        </p>
        </div>
        """, unsafe_allow_html=True)

        # Long-term projection
        st.subheader("📈 Long-Term Projection (30 years)")

        annual_return = st.slider("Expected Annual Return (%)", min_value=0.0, max_value=8.0, value=4.0, step=0.5)

        years = list(range(0, 31))
        with_pillar3a = []
        without_pillar3a = []
        cumulative_tax_savings = []

        total_value = 0
        total_tax_saved = 0

        for year in years:
            if year == 0:
                with_pillar3a.append(0)
                without_pillar3a.append(0)
                cumulative_tax_savings.append(0)
            else:
                # With Pillar 3a: full contribution + tax savings reinvested
                total_value = (total_value + your_contribution) * (1 + annual_return/100)
                with_pillar3a.append(total_value)

                # Without Pillar 3a: contribution minus tax
                after_tax_contribution = your_contribution - tax_savings
                without_value = (without_pillar3a[-1] + after_tax_contribution) * (1 + annual_return/100)
                without_pillar3a.append(without_value)

                # Cumulative tax savings
                total_tax_saved += tax_savings
                cumulative_tax_savings.append(total_tax_saved)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=with_pillar3a, name='With Pillar 3a',
                                 line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=years, y=without_pillar3a, name='Without Pillar 3a',
                                 line=dict(color='red', width=3)))
        fig.add_trace(go.Scatter(x=years, y=cumulative_tax_savings, name='Cumulative Tax Savings',
                                 line=dict(color='orange', width=2, dash='dash')))

        fig.update_layout(
            title=f'Pillar 3a Growth Projection ({annual_return}% annual return)',
            xaxis_title='Years',
            yaxis_title='Value (CHF)',
            height=500,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

        final_difference = with_pillar3a[-1] - without_pillar3a[-1]

        st.success(f"""
        **After 30 years:**
        - 💚 With Pillar 3a: CHF {with_pillar3a[-1]:,.2f}
        - ❌ Without Pillar 3a: CHF {without_pillar3a[-1]:,.2f}
        - 🎯 **Extra wealth: CHF {final_difference:,.2f}**
        """)

    with col2:
        st.markdown("""
        <div class="tax-tip">
        <h4>⏰ Important Deadlines</h4>
        <ul>
        <li><strong>Dec 31, 2025:</strong> Last day to contribute for 2025 tax year</li>
        <li>Contributions above maximum are NOT deductible</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="tax-tip">
        <h4>🆕 NEW for 2026</h4>
        <ul>
        <li>Retroactive contributions allowed</li>
        <li>Catch up missed contributions for up to <strong>10 years</strong></li>
        <li>Only applies to contributions missed from 2025 onwards</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="tax-tip">
        <h4>⚠️ Withdrawal Rules</h4>
        <ul>
        <li>Earliest: 5 years before retirement</li>
        <li>Latest: Official retirement age</li>
        <li>Taxed at reduced separate rate</li>
        <li>Can withdraw for: home purchase, self-employment, leaving Switzerland</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="tax-tip">
        <h4>💡 Pro Tips</h4>
        <ul>
        <li>Open multiple 3a accounts for staggered withdrawals</li>
        <li>Reduces tax on withdrawal</li>
        <li>Max 5 years between withdrawals</li>
        <li>Invest in stocks for long-term (20+ years)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# INVESTMENT INCOME PAGE
elif page == "Investment Income":
    st.markdown('<h1 class="main-header">📈 Investment Income & Wealth Tax</h1>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["💹 Capital Gains", "💰 Dividends", "🏦 Wealth Tax"])

    with tab1:
        st.subheader("Capital Gains Tax - TAX FREE! ✅")

        st.success("""
        **Great News!** In Switzerland, capital gains on securities are **generally tax-free**
        for private investors - a major advantage compared to other countries!
        """)

        st.markdown("### Requirements to Qualify as Private Investor")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="highlight-box">
            <h4>✅ You QUALIFY if:</h4>
            <ul>
            <li>Hold securities <strong>6+ months</strong> before selling</li>
            <li>Annual trading ≤ <strong>5× portfolio value</strong></li>
            <li>Capital gains NOT primary income</li>
            <li>Derivatives mainly for hedging</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="highlight-box" style="border-left-color: #DC143C;">
            <h4>❌ Professional Trader if:</h4>
            <ul>
            <li>Frequent short-term trading</li>
            <li>Trading volume > 5× portfolio</li>
            <li>Rely on trading as income</li>
            <li>Use leverage extensively</li>
            </ul>
            <p><strong>→ Taxed as income!</strong></p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🧮 Check Your Trading Volume")

        portfolio_value = st.number_input(
            "Portfolio Value (CHF)",
            min_value=0,
            max_value=10000000,
            value=100000,
            step=10000
        )

        annual_trades = st.number_input(
            "Annual Trading Volume (CHF)",
            min_value=0,
            max_value=50000000,
            value=200000,
            step=10000,
            help="Total value of all buy and sell transactions in a year"
        )

        max_allowed = portfolio_value * 5
        ratio = annual_trades / portfolio_value if portfolio_value > 0 else 0

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Trading Volume", f"CHF {annual_trades:,}")
            st.metric("Maximum Allowed (5× portfolio)", f"CHF {max_allowed:,}")

        with col2:
            st.metric("Your Ratio", f"{ratio:.2f}×")

            if ratio <= 5:
                st.success("✅ You qualify as private investor - Capital gains are TAX-FREE!")
            else:
                st.error("⚠️ You may be classified as professional trader - Capital gains taxed as income!")

    with tab2:
        st.subheader("Dividend Taxation")

        st.warning("**Note:** Dividends ARE taxed as regular income (unlike capital gains)")

        st.markdown("### Swiss Withholding Tax (Verrechnungssteuer)")

        st.markdown("""
        - 🔴 **35% withheld** on Swiss dividends and interest
        - ✅ **100% reclaimable** when you declare securities in tax return
        - 📋 Must declare ALL securities holdings
        """)

        st.markdown("### Calculate Dividend Tax")

        annual_dividends = st.number_input(
            "Annual Dividend Income (CHF)",
            min_value=0,
            max_value=1000000,
            value=5000,
            step=500
        )

        swiss_portion = st.slider(
            "Swiss Stock Portion (%)",
            min_value=0,
            max_value=100,
            value=50
        )

        ker_portion = st.slider(
            "Tax-Free KER Portion of Swiss Dividends (%)",
            min_value=0,
            max_value=50,
            value=0,
            help="Capital Reserves (KER) - check your dividend statements"
        )

        your_tax_rate = st.slider(
            "Your Marginal Tax Rate (%)",
            min_value=15.0,
            max_value=45.0,
            value=30.0,
            step=0.5
        )

        # Calculate
        swiss_dividends = annual_dividends * (swiss_portion / 100)
        foreign_dividends = annual_dividends - swiss_dividends

        taxable_swiss_dividends = swiss_dividends * (1 - ker_portion / 100)

        withholding_tax = swiss_dividends * 0.35
        tax_on_dividends = (taxable_swiss_dividends + foreign_dividends) * (your_tax_rate / 100)
        net_tax = tax_on_dividends - withholding_tax  # Withholding tax is reclaimable

        st.markdown(f"""
        <div class="highlight-box">
        <h4>Dividend Tax Breakdown</h4>
        <table style="width:100%">
        <tr><td>Total Dividends:</td><td style="text-align:right">CHF {annual_dividends:,.2f}</td></tr>
        <tr><td>- Swiss Dividends ({swiss_portion}%):</td><td style="text-align:right">CHF {swiss_dividends:,.2f}</td></tr>
        <tr><td>- Foreign Dividends:</td><td style="text-align:right">CHF {foreign_dividends:,.2f}</td></tr>
        <tr><td colspan="2"><hr></td></tr>
        <tr><td>Swiss Withholding Tax (35%):</td><td style="text-align:right">CHF {withholding_tax:,.2f}</td></tr>
        <tr><td>Tax on Dividends ({your_tax_rate}%):</td><td style="text-align:right">CHF {tax_on_dividends:,.2f}</td></tr>
        <tr><td>Less: Reclaimable Withholding:</td><td style="text-align:right">- CHF {withholding_tax:,.2f}</td></tr>
        <tr><td colspan="2"><hr></td></tr>
        <tr><td><strong>Net Tax on Dividends:</strong></td><td style="text-align:right"><strong>CHF {max(0, net_tax):,.2f}</strong></td></tr>
        <tr><td><strong>After-Tax Dividends:</strong></td><td style="text-align:right; color:green"><strong>CHF {annual_dividends - max(0, net_tax):,.2f}</strong></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

        st.info("""
        💡 **Pro Tip:** Always declare your securities to reclaim the 35% Swiss withholding tax!
        Failure to declare means you lose this reclaim.
        """)

    with tab3:
        st.subheader("Wealth Tax")

        st.info("Switzerland is one of the few countries with an annual wealth tax (cantonal level only)")

        st.markdown("### Calculate Your Wealth Tax")

        selected_canton_wealth = st.selectbox(
            "Canton",
            df_cantons['Canton'].tolist(),
            key="wealth_canton"
        )

        canton_wealth_info = df_cantons[df_cantons['Canton'] == selected_canton_wealth].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            securities_value = st.number_input(
                "Securities Portfolio (Dec 31 value)",
                min_value=0,
                max_value=50000000,
                value=500000,
                step=10000
            )

            real_estate_value = st.number_input(
                "Real Estate (tax value)",
                min_value=0,
                max_value=50000000,
                value=0,
                step=50000
            )

            cash_savings = st.number_input(
                "Cash & Savings",
                min_value=0,
                max_value=10000000,
                value=50000,
                step=5000
            )

        with col2:
            pillar_2_assets = st.number_input(
                "Pillar 2 Assets (EXEMPT)",
                min_value=0,
                max_value=5000000,
                value=200000,
                step=10000,
                help="Pillar 2 & 3a are exempt from wealth tax!"
            )

            pillar_3a_assets = st.number_input(
                "Pillar 3a Assets (EXEMPT)",
                min_value=0,
                max_value=500000,
                value=50000,
                step=5000
            )

            debts = st.number_input(
                "Debts & Mortgages (deductible)",
                min_value=0,
                max_value=10000000,
                value=0,
                step=10000
            )

        gross_wealth = securities_value + real_estate_value + cash_savings
        taxable_wealth = gross_wealth - debts

        # Use mid-point of wealth tax range
        wealth_tax_rate = (canton_wealth_info['Wealth_Tax_Min'] + canton_wealth_info['Wealth_Tax_Max']) / 2
        annual_wealth_tax = taxable_wealth * (wealth_tax_rate / 100)

        st.markdown(f"""
        <div class="highlight-box">
        <h4>Wealth Tax Calculation</h4>
        <table style="width:100%">
        <tr><td>Securities:</td><td style="text-align:right">CHF {securities_value:,.2f}</td></tr>
        <tr><td>Real Estate:</td><td style="text-align:right">CHF {real_estate_value:,.2f}</td></tr>
        <tr><td>Cash & Savings:</td><td style="text-align:right">CHF {cash_savings:,.2f}</td></tr>
        <tr><td><strong>Gross Wealth:</strong></td><td style="text-align:right"><strong>CHF {gross_wealth:,.2f}</strong></td></tr>
        <tr><td colspan="2"><hr></td></tr>
        <tr><td>Less: Debts:</td><td style="text-align:right">- CHF {debts:,.2f}</td></tr>
        <tr><td><strong>Taxable Wealth:</strong></td><td style="text-align:right"><strong>CHF {taxable_wealth:,.2f}</strong></td></tr>
        <tr><td colspan="2"><hr></td></tr>
        <tr><td>Wealth Tax Rate ({selected_canton_wealth}):</td><td style="text-align:right">{wealth_tax_rate:.2f}%</td></tr>
        <tr><td style="font-size:1.2em; color:#DC143C"><strong>Annual Wealth Tax:</strong></td><td style="text-align:right; font-size:1.2em; color:#DC143C"><strong>CHF {annual_wealth_tax:,.2f}</strong></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"""
        ✅ **Exempt from Wealth Tax:**
        Pillar 2: CHF {pillar_2_assets:,.2f}
        Pillar 3a: CHF {pillar_3a_assets:,.2f}
        **Total Exempt: CHF {pillar_2_assets + pillar_3a_assets:,.2f}**
        """)

        st.markdown("### 💡 Wealth Tax Optimization Strategies")

        st.markdown("""
        1. **Maximize Pillar 2 & 3a** - These are exempt from wealth tax
        2. **Consider Pillar 2 buybacks** - Moves taxable wealth to exempt category
        3. **Deduct expected federal tax** - Reduces taxable wealth
        4. **Timing matters** - Wealth assessed on December 31
        5. **Real estate** - Usually assessed below market value
        """)

# REAL ESTATE TAX PAGE
elif page == "Real Estate Tax":
    st.markdown('<h1 class="main-header">🏠 Real Estate & Property Tax</h1>', unsafe_allow_html=True)

    st.warning("""
    🗳️ **MAJOR REFORM - September 2025**
    On September 28, 2025, Swiss voters (57.7%) approved abolishing the Eigenmietwert (imputed rental value) system.
    Expected implementation: **January 1, 2028**
    """)

    tab1, tab2, tab3 = st.tabs(["📋 Current System (Until 2028)", "🆕 New System (From 2028)", "⚖️ Comparison"])

    with tab1:
        st.subheader("Current Eigenmietwert System (Until ~2028)")

        st.markdown("""
        ### What is Eigenmietwert?

        Homeowners must declare **notional rental income** for owner-occupied property:
        - Calculated as **60-70% of market rent**
        - Added to your taxable income
        - In return, you can deduct mortgage interest and maintenance costs
        """)

        st.markdown("### Calculate Current Tax Impact")

        market_rent = st.number_input(
            "Estimated Monthly Market Rent (CHF)",
            min_value=0,
            max_value=20000,
            value=2500,
            step=100
        )

        eigenmietwert_rate = st.slider(
            "Eigenmietwert Rate (%)",
            min_value=60,
            max_value=70,
            value=65
        )

        mortgage_interest_paid = st.number_input(
            "Annual Mortgage Interest Paid (CHF)",
            min_value=0,
            max_value=500000,
            value=15000,
            step=1000
        )

        maintenance_costs = st.number_input(
            "Annual Maintenance Costs (CHF)",
            min_value=0,
            max_value=200000,
            value=5000,
            step=500
        )

        your_tax_rate_re = st.slider(
            "Your Marginal Tax Rate (%)",
            min_value=15.0,
            max_value=45.0,
            value=30.0,
            step=0.5,
            key="re_tax_rate"
        )

        # Calculate
        annual_market_rent = market_rent * 12
        imputed_rental_value = annual_market_rent * (eigenmietwert_rate / 100)
        total_deductions_re = mortgage_interest_paid + maintenance_costs
        net_taxable_amount = imputed_rental_value - total_deductions_re
        tax_impact = net_taxable_amount * (your_tax_rate_re / 100)

        st.markdown(f"""
        <div class="highlight-box">
        <h4>Current System Tax Impact</h4>
        <table style="width:100%">
        <tr><td>Market Rent (annual):</td><td style="text-align:right">CHF {annual_market_rent:,.2f}</td></tr>
        <tr><td>Eigenmietwert ({eigenmietwert_rate}%):</td><td style="text-align:right; color:red">+ CHF {imputed_rental_value:,.2f}</td></tr>
        <tr><td colspan="2"><hr></td></tr>
        <tr><td><strong>Deductions:</strong></td><td></td></tr>
        <tr><td>Mortgage Interest:</td><td style="text-align:right; color:green">- CHF {mortgage_interest_paid:,.2f}</td></tr>
        <tr><td>Maintenance Costs:</td><td style="text-align:right; color:green">- CHF {maintenance_costs:,.2f}</td></tr>
        <tr><td colspan="2"><hr></td></tr>
        <tr><td><strong>Net Taxable Amount:</strong></td><td style="text-align:right"><strong>CHF {net_taxable_amount:,.2f}</strong></td></tr>
        <tr><td colspan="2"><hr></td></tr>
        <tr><td><strong>Tax Impact ({your_tax_rate_re}% rate):</strong></td><td style="text-align:right; font-size:1.2em; color:#DC143C"><strong>CHF {tax_impact:,.2f}</strong></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

        if net_taxable_amount > 0:
            st.error(f"❌ Current system: You pay extra CHF {tax_impact:,.2f} in taxes annually")
        else:
            st.success(f"✅ Current system: Tax benefit of CHF {abs(tax_impact):,.2f} annually")

    with tab2:
        st.subheader("New System (Expected January 1, 2028)")

        st.markdown("""
        ### What Changes:

        ❌ **No more** imputed rental value taxation
        ❌ **No more** general mortgage interest deductions
        ❌ **No more** maintenance/renovation deductions

        ### Exceptions:

        ✅ **Rental properties**: Can still deduct mortgage interest and costs
        ✅ **First-time buyers**: Transitional mortgage interest deduction
        """)

        st.markdown("### First-Time Buyer Transitional Benefit")

        is_first_time = st.radio(
            "Are you a first-time buyer after the reform?",
            ["Yes", "No"]
        )

        if is_first_time == "Yes":
            marital_status_re = st.radio(
                "Marital Status",
                ["Single", "Married"],
                key="re_marital"
            )

            if marital_status_re == "Married":
                base_deduction = 10000
            else:
                base_deduction = 5000

            st.markdown("### Transitional Deduction Schedule")

            years = list(range(1, 11))
            deductions = [base_deduction * (1 - (year - 1) * 0.1) for year in years]

            deduction_df = pd.DataFrame({
                'Year': years,
                'Deduction (CHF)': deductions,
                'Tax Saving (30%)': [d * 0.30 for d in deductions]
            })

            st.dataframe(
                deduction_df.style.format({
                    'Deduction (CHF)': 'CHF {:,.0f}',
                    'Tax Saving (30%)': 'CHF {:,.0f}'
                }),
                use_container_width=True
            )

            total_deduction = sum(deductions)
            total_saving = total_deduction * 0.30

            st.success(f"""
            **10-Year Total:**
            Deductions: CHF {total_deduction:,.0f}
            Tax Savings (at 30%): CHF {total_saving:,.0f}
            """)
        else:
            st.info("No transitional benefits available for existing homeowners under the new system.")

    with tab3:
        st.subheader("⚖️ Current vs New System Comparison")

        st.markdown("### Compare Your Situation")

        col1, col2 = st.columns(2)

        with col1:
            comparison_rent = st.number_input(
                "Monthly Market Rent (CHF)",
                min_value=0,
                max_value=20000,
                value=2500,
                step=100,
                key="comp_rent"
            )

            comparison_mortgage = st.number_input(
                "Annual Mortgage Interest (CHF)",
                min_value=0,
                max_value=500000,
                value=15000,
                step=1000,
                key="comp_mortgage"
            )

        with col2:
            comparison_maintenance = st.number_input(
                "Annual Maintenance (CHF)",
                min_value=0,
                max_value=200000,
                value=5000,
                step=500,
                key="comp_maint"
            )

            comparison_tax_rate = st.slider(
                "Tax Rate (%)",
                min_value=15.0,
                max_value=45.0,
                value=30.0,
                step=0.5,
                key="comp_rate"
            )

        # Current system calculation
        annual_rent_comp = comparison_rent * 12
        eigenmietwert_comp = annual_rent_comp * 0.65
        deductions_comp = comparison_mortgage + comparison_maintenance
        net_current = eigenmietwert_comp - deductions_comp
        tax_current = net_current * (comparison_tax_rate / 100)

        # New system calculation
        tax_new = 0  # No imputed value, no deductions

        difference = tax_new - tax_current

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current System (Until 2028)",
                f"CHF {tax_current:,.2f}",
                help="Annual tax impact under current Eigenmietwert system"
            )

        with col2:
            st.metric(
                "New System (From 2028)",
                f"CHF {tax_new:,.2f}",
                help="Annual tax impact under new system"
            )

        with col3:
            st.metric(
                "Annual Difference",
                f"CHF {abs(difference):,.2f}",
                delta=f"{difference:,.2f}",
                delta_color="inverse" if difference > 0 else "normal"
            )

        if difference > 0:
            st.success(f"✅ The new system will SAVE you CHF {difference:,.2f} per year!")
        elif difference < 0:
            st.error(f"❌ The new system will COST you CHF {abs(difference):,.2f} more per year")
        else:
            st.info("Neutral impact - no significant change between systems")

        # Who wins/loses
        st.markdown("### Who Benefits from the Reform?")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="highlight-box">
            <h4>✅ Winners</h4>
            <ul>
            <li>Owners with low/no mortgage</li>
            <li>Properties in expensive areas (high Eigenmietwert)</li>
            <li>Owners who don't maximize deductions</li>
            <li>Simplified tax filing</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="highlight-box" style="border-left-color: #DC143C;">
            <h4>❌ Potential Losers</h4>
            <ul>
            <li>Owners with large mortgages</li>
            <li>Properties needing significant maintenance</li>
            <li>Energy efficiency renovations</li>
            <li>Lose tax optimization strategies</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
<p><strong>Swiss Tax Guide 2025</strong></p>
<p>This tool is for informational purposes only. Tax laws change frequently.
Consult a qualified tax advisor for personalized advice.</p>
<p><em>Last Updated: December 2025</em></p>
</div>
""", unsafe_allow_html=True)
