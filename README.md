# Swiss Tax Deduction Analyzer 🇨🇭

A comprehensive Streamlit web application that helps **single, employed individuals** in Zürich calculate their tax liability and identify all available deductions for the 2025 tax year.

## Features

✅ **Three-Tier Swiss Tax Calculation**
- Federal progressive tax
- Zürich cantonal tax (with 0.98 multiplier)
- Municipal tax (varies by municipality)

✅ **Comprehensive Deduction Support**
- Automatic/pauschal deductions (no proof required)
- Professional expenses, meal costs, commuting
- Insurance premiums, Pillar 3a contributions
- Education costs, charitable/political donations

✅ **Step-by-Step Breakdown**
- Detailed calculation from gross to net income
- Tax breakdown by federal/cantonal/municipal
- Real-time deduction validation

✅ **User-Friendly Interface**
- Interactive sidebar inputs
- Clear visualization of tax burden
- Helpful tooltips and explanations

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**

```bash
cd C:\Users\davim\Desktop\Python_Scripts
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## How to Use

### 1. Enter Your Information

In the sidebar, provide:
- **Annual Gross Salary**: Your yearly gross salary before any deductions
- **Employment Percentage**: 100% for full-time, 50% for part-time, etc.
- **Pillar 2 Enrollment**: Whether you're enrolled in a company pension fund
- **Municipality**: Your municipality of residence in Zürich canton

### 2. Add Deductions

Expand the deduction sections to enter:

**🚇 Commuting & Meals:**
- Commute type (public transport, bicycle, car, work from home)
- Annual public transport costs (if applicable)
- Whether you have canteen subsidy

**🏥 Insurance:**
- Annual insurance premiums (health, accident, life)
- Premium subsidies received (Prämienverbilligung)

**💰 Pillar 3a:**
- Annual contribution (max CHF 7,258 in 2025 with Pillar 2)

**📚 Education & Other:**
- Further education costs
- Charitable donations
- Political party donations

### 3. Calculate

Click the **"🧮 Calculate Taxes"** button to see:
- Your complete tax breakdown
- Step-by-step calculation
- Net annual and monthly income
- Effective and marginal tax rates

## Project Structure

```
swiss_tax_analyzer/
├── app.py                          # Main Streamlit application
├── config/
│   ├── tax_rates_2025.py          # Federal & cantonal tax rate tables
│   ├── deduction_limits.py         # All deduction limits and thresholds
│   └── municipality_data.py        # Municipality multipliers
├── models/
│   ├── user_profile.py            # User profile data model
│   ├── deduction.py               # Deduction category models
│   ├── tax_calculation.py         # Tax calculation result models
│   └── optimization.py            # Optimization suggestion models
├── services/
│   ├── tax_calculator.py          # Core tax calculation engine
│   └── deduction_validator.py     # Deduction eligibility checker
├── ui/
│   ├── input_forms.py             # Streamlit input components
│   └── calculation_display.py     # Step-by-step calculation display
├── utils/
│   ├── formatters.py              # Currency/number formatting
│   ├── validators.py              # Input validation utilities
│   └── constants.py               # Application constants
└── requirements.txt
```

## Deduction Categories

### Automatic Deductions (No Proof Required) 🟢

These are calculated automatically based on your inputs:

| Deduction | Amount | Notes |
|-----------|--------|-------|
| Professional Expenses | 3% of salary (min CHF 2,000, max CHF 4,000) | Includes tools, software, literature, work clothes |
| Meal Expenses | CHF 3,200/year without subsidy<br>CHF 1,600/year with subsidy | CHF 15/day or CHF 7.50/day |
| Bicycle Commuting | CHF 700/year | Pauschal amount |

### Proof-Required Deductions 📄

These require documentation:

| Deduction | Limit | Proof Needed |
|-----------|-------|--------------|
| Public Transport | CHF 3,000 (federal)<br>CHF 5,000 (Zürich) | Receipts, GA subscription |
| Insurance Premiums | CHF 1,700 (single with Pillar 2) | Premium statements |
| Pillar 3a | CHF 7,258 (2025) | Official contribution certificate |
| Further Education | CHF 12,000 | Receipts (CHF 500 in ZH without proof) |
| Charitable Donations | Max 20% of net income, min CHF 100 | Donation receipts |
| Political Donations | CHF 10,000 (Zürich) | Donation receipts |

## Tax Calculation

### Three-Tier System

Switzerland has a three-tier tax system:

1. **Federal Tax**: Progressive rates from 0.77% to 11.5% (capped)
2. **Cantonal Tax**: Progressive rates specific to Zürich canton (× 0.98 multiplier)
3. **Municipal Tax**: Cantonal tax × municipal multiplier (e.g., 1.19 for Zürich City)

### Calculation Flow

```
Gross Salary
  ↓
- Social Security Contributions (AHV/IV: 5.3%, ALV: 1.1%, NBU: ~0.7%)
  ↓
= Adjusted Income
  ↓
- All Deductions (professional, commuting, insurance, Pillar 3a, etc.)
  ↓
= Taxable Income
  ↓
→ Federal Tax (progressive)
→ Cantonal Tax (progressive × 0.98)
→ Municipal Tax (cantonal base × 1.19)
  ↓
= Total Tax
  ↓
Net Income = Gross - Social Security - Total Tax
```

## Example Calculation

**Profile:**
- Single, employed in Zürich City
- Gross salary: CHF 80,000/year
- Pillar 2 enrolled, no children
- Public transport: CHF 2,400/year
- Insurance: CHF 4,800/year
- Pillar 3a: CHF 7,258/year

**Results:**
- Taxable Income: ~CHF 54,900
- Federal Tax: ~CHF 1,800
- Cantonal Tax: ~CHF 3,200
- Municipal Tax: ~CHF 3,800
- **Total Tax: ~CHF 8,800**
- **Net Annual Income: ~CHF 66,600**
- **Effective Tax Rate: ~11%**

## Data Sources

This tool is based on:
- **SchmittTreuhand_Steuertipps_web3.pdf**: Comprehensive Swiss tax deduction guide
- **Swiss Federal Tax Law** (https://www.fedlex.admin.ch): Official federal tax regulations
- **Zürich Cantonal Tax Administration**: Cantonal tax rates and rules

## Limitations

This tool currently supports:
- ✅ Single individuals (not married couples)
- ✅ Employed persons with salary income
- ✅ Zürich canton only
- ✅ No children
- ✅ No self-employment income
- ✅ No investment/rental income
- ✅ No real estate ownership (Eigenmietwert)

**Future enhancements** may include support for married couples, children, other cantons, and additional income sources.

## Disclaimer

⚠️ **This tool provides estimates for informational and planning purposes only.**

- Tax calculations are based on 2025 rates and regulations
- Actual tax liability may vary based on individual circumstances
- Always consult with a qualified tax professional for official tax returns
- The Swiss tax system is complex; this tool simplifies certain aspects

## Technical Details

### Technology Stack
- **Python 3.8+**
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation
- **Plotly**: Visualizations (future enhancement)
- **ReportLab**: PDF export (future enhancement)

### Tax Rate Tables

Tax rates are stored in `config/tax_rates_2025.py`:
- Progressive federal brackets from 0.77% to 11.5%
- Zürich cantonal progressive rates
- Municipal multipliers for various Zürich municipalities

### Testing

To validate calculations:
1. Compare against official Zürich tax calculator
2. Cross-reference with tax guide examples
3. Verify against actual tax assessments

## Contributing

This is a demonstration project. Suggestions for improvements:
- Add support for married couples
- Include children and family deductions
- Support additional cantons
- Add visualization charts
- Implement PDF/CSV export
- Create optimization suggestion engine

## License

This project is provided for educational and informational purposes.

## Support

For questions or issues:
- Review the "About" tab in the application
- Check the SchmittTreuhand PDF for detailed deduction rules
- Consult the Swiss federal tax administration website

---

**Built with ❤️ for Swiss taxpayers**
