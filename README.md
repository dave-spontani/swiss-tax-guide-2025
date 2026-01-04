# Swiss Tax Deduction Questionnaire + Calculator

A comprehensive Streamlit application for calculating Swiss taxes (Zurich canton) with smart deduction guidance.

## Features

- **Smart Questionnaire**: Multi-step wizard that only asks relevant questions
- **Automatic Deductions**: Shows deductions you get without receipts (pauschal)
- **Optional Deductions**: Guided input for deductions requiring documentation
- **3-Level Tax Comparison**:
  - Before any deductions
  - After automatic deductions
  - After all deductions
- **Interactive Optimization**: Real-time sliders to optimize Pillar 3a, Pillar 2, and other deductions
- **Detailed Breakdowns**: Tax bracket breakdowns for federal and cantonal taxes

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the application
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Application Structure

```
├── app.py                          # Main Streamlit application
├── models/
│   ├── tax_data.py                # Data models
│   └── constants.py               # Tax brackets and rates
├── calculations/
│   ├── federal_tax.py             # Federal tax calculation (DBG)
│   ├── cantonal_tax.py            # Zurich cantonal tax
│   ├── church_tax.py              # Church tax
│   ├── wealth_tax.py              # Wealth tax
│   └── deductions.py              # Deduction logic
├── questionnaire/
│   ├── qualifying_questions.py    # Step 1: Personal info
│   ├── automatic_deductions.py    # Step 2: Automatic deductions
│   └── optional_deductions.py     # Step 3: Optional deductions
├── ui/
│   ├── wizard.py                  # Wizard flow logic
│   ├── tax_comparison.py          # 3-level comparison display
│   └── optimization.py            # Interactive optimization tools
└── utils/
    └── formatters.py              # Swiss number formatting
```

## Tax Calculations

### Federal Tax (DBG - Art. 36)
- Progressive brackets from CHF 15,200 to CHF 793,300+
- Formula: `total_tax = base_tax + (excess_income / 100) × rate_per_hundred`
- Marginal rates from 0.77% to 13.20%

### Zurich Cantonal Tax (StG § 35)
- Two-step calculation:
  1. Calculate "Einfache Staatssteuer" (simple state tax)
  2. Apply Steuerfüsse (tax multipliers):
     - Cantonal: 98%
     - Municipal: varies by municipality (e.g., Zürich 119%)
- Progressive brackets from CHF 6,900 to CHF 263,300+
- Marginal rates from 2% to 13%

### Automatic Deductions (No Receipts)
- Commuting: CHF 700 pauschal
- Meals: CHF 1,600 (with subsidy) or CHF 3,200 (without)
- Professional expenses: 3% of salary (max CHF 4,000)
- Side income: CHF 2,400
- Child deductions: CHF 9,000 per child (Zurich)
- Property maintenance: 20% of Eigenmietwert
- Asset management: 3‰ of securities (max CHF 6,000)
- Dual income: CHF 5,900 (if married, both working)

### Optional Deductions (Require Documentation)
- Pillar 3a: Max CHF 7,056 (employed) / CHF 35,280 (self-employed)
- Pillar 2 buy-ins: Unlimited (with certificate)
- Mortgage interest: Actual amount
- Medical costs: Above 5% of income
- Childcare: Max CHF 10,100
- Donations: Max 20% of income
- Political contributions: Max CHF 10,000 (single) / CHF 20,000 (married)

## Sources

- Federal tax: [DBG (fedlex.admin.ch)](https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de)
- Cantonal tax: [StG § 35 (zh.ch)](https://www.zh.ch/de/steuern-finanzen/steuern/)
- Deductions: Schmitt Treuhand Tax Guide 2024

## Disclaimer

Tax calculations are estimates based on 2024/2025 rates and standard deductions. Actual tax liability may differ based on individual circumstances. Consult official sources and tax professionals for exact calculations.

## License

This project is for educational purposes only.
