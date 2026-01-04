# Swiss Tax Calculator - Complete Technical Documentation

## Overview

This is a comprehensive Swiss tax calculator application that computes federal, cantonal (Zurich), municipal, church, and wealth taxes for single individuals. The application uses real Swiss tax brackets and rates based on official government sources.

**Tech Stack**: Next.js 14+ with TypeScript, React, Tailwind CSS

## Application Architecture

### Core Calculation Flow

```
User Input → Deductions Calculation → Tax Calculations → Results Display
                                      ├─ Federal Tax
                                      ├─ Cantonal Tax (Zurich)
                                      ├─ Municipal Tax
                                      ├─ Church Tax (optional)
                                      └─ Wealth Tax (optional)
```

## Data Model

### QuestionnaireData Interface

```typescript
interface QuestionnaireData {
  // Personal Details
  maritalStatus: 'single'              // Currently only single supported
  numberOfChildren: number             // Children under 18 or in education
  numberOfDependents: number           // Other dependents beyond children
  religiousAffiliation: ReligiousAffiliation  // 'none' | 'reformed' | 'catholic' | 'christian-catholic'
  totalWealth: number                  // Total assets minus liabilities

  // Income & Location
  income: number                       // Annual gross income in CHF
  municipality: string                 // Municipality name (e.g., "Zürich")
  gemeindeSteuerfuss: number          // Municipal tax multiplier (%)

  // Voluntary Deductions
  pillar3aContribution: number        // Pillar 3a contributions (max CHF 7,056)
  pillar2AdditionalContribution: number  // Pillar 2 additional purchases
  otherDeductions: number             // Professional expenses, insurance, etc.
}
```

### Default Values

```python
DEFAULT_VALUES = {
    'marital_status': 'single',
    'number_of_children': 0,
    'number_of_dependents': 0,
    'religious_affiliation': 'none',
    'total_wealth': 0,
    'income': 100000,
    'municipality': 'Zürich',
    'gemeinde_steuerfuss': 119,
    'pillar_3a_contribution': 0,
    'pillar_2_additional_contribution': 0,
    'other_deductions': 0
}
```

## Tax Bracket Systems

### 1. Federal Tax Brackets (DBG - Direct Federal Tax)

**Source**: https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de (Art. 36 DBG)

**Calculation Formula**:
```
Total Tax = baseTax + (excessIncome / 100) × ratePerHundred
```

**Bracket Structure**:

```python
FEDERAL_TAX_BRACKETS = [
    {'threshold': 0,       'base_tax': 0,        'rate_per_hundred': 0},      # Tax-free
    {'threshold': 15200,   'base_tax': 0,        'rate_per_hundred': 0.77},
    {'threshold': 33200,   'base_tax': 138.60,   'rate_per_hundred': 0.88},
    {'threshold': 43500,   'base_tax': 229.20,   'rate_per_hundred': 2.64},
    {'threshold': 58000,   'base_tax': 612.00,   'rate_per_hundred': 2.97},
    {'threshold': 76100,   'base_tax': 1149.55,  'rate_per_hundred': 5.94},
    {'threshold': 82000,   'base_tax': 1500.00,  'rate_per_hundred': 6.60},
    {'threshold': 108800,  'base_tax': 3268.80,  'rate_per_hundred': 8.80},
    {'threshold': 141500,  'base_tax': 6146.40,  'rate_per_hundred': 11.00},
    {'threshold': 184900,  'base_tax': 10920.40, 'rate_per_hundred': 13.20},
    {'threshold': 793300,  'base_tax': 91229.20, 'rate_per_hundred': 0},      # Cap
    {'threshold': 793400,  'base_tax': 91241.00, 'rate_per_hundred': 11.50},  # Higher incomes
]
```

**Key Characteristics**:
- Progressive tax system
- First CHF 15,200 is tax-free
- Marginal rates range from 0.77% to 13.20%
- Special handling for incomes above CHF 793,300

### 2. Zurich Cantonal Tax Brackets

**Source**: StG § 35 (adjusted for 2024 cold progression: 3.3%)
https://www.zh.ch/de/steuern-finanzen/steuern/treuhaender/steuerbuch/steuerbuch-definition/zstb-34-1.html

**Key Concept**: The Zurich system uses "Einfache Staatssteuer" (simple state tax) which is then multiplied by tax multipliers (Steuerfüsse).

**Bracket Structure**:

```python
ZURICH_TAX_BRACKETS = [
    {'threshold': 0,       'rate': 0},   # First CHF 6,900 tax-free
    {'threshold': 6900,    'rate': 2},   # 2% on next CHF 4,900
    {'threshold': 11800,   'rate': 3},   # 3% on next CHF 4,800
    {'threshold': 16600,   'rate': 4},   # 4% on next CHF 7,900
    {'threshold': 24500,   'rate': 5},   # 5% on next CHF 9,600
    {'threshold': 34100,   'rate': 6},   # 6% on next CHF 11,000
    {'threshold': 45100,   'rate': 7},   # 7% on next CHF 12,900
    {'threshold': 58000,   'rate': 8},   # 8% on next CHF 17,400
    {'threshold': 75400,   'rate': 9},   # 9% on next CHF 33,600
    {'threshold': 109000,  'rate': 10},  # 10% on next CHF 33,200
    {'threshold': 142200,  'rate': 11},  # 11% on next CHF 52,700
    {'threshold': 194900,  'rate': 12},  # 12% on next CHF 68,400
    {'threshold': 263300,  'rate': 13},  # 13% on income above
]
```

**Tax Multipliers (Steuerfüsse) - 2024**:

```python
CANTONAL_STEUERFUSS = 98  # Cantonal: 98%
```

**Municipal Steuerfüsse** (varies by municipality):

```python
MUNICIPALITY_STEUERFUESSE = {
    'Zürich': 119,
    'Winterthur': 122,
    'Uster': 108,
    'Dübendorf': 106,
    'Dietikon': 118,
    'Wetzikon': 105,
    'Horgen': 93,
    'Bülach': 104,
    'Thalwil': 82,
    'Zollikon': 77,
    'Küsnacht': 77,
    'Meilen': 80,
    'Zumikon': 73,
    'Kilchberg': 72,
}
```

### 3. Wealth Tax Brackets (Zurich)

**Bracket Structure**:

```python
WEALTH_TAX_BRACKETS = [
    {'threshold': 0,        'rate_per_thousand': 0},     # Tax-free below CHF 77,000
    {'threshold': 77000,    'rate_per_thousand': 0.5},   # 0.5‰
    {'threshold': 308000,   'rate_per_thousand': 1.0},   # 1.0‰
    {'threshold': 3158000,  'rate_per_thousand': 3.0},   # 3.0‰
]
```

**Wealth Deductions**:

```python
WEALTH_DEDUCTION_PER_ADULT = 82200   # CHF 82,200 per adult
WEALTH_DEDUCTION_PER_CHILD = 41100   # CHF 41,100 per child
```

## Deduction System

### Deduction Calculation

```python
def calculate_deductions(data):
    """
    Calculate total deductions from income.

    Returns:
    {
        'pillar_3a': float,
        'pillar_2_additional': float,
        'other': float,
        'child_deduction': float,    # Currently 0 for Zurich
        'dependent_deduction': float, # Currently 0 for Zurich
        'total': float
    }
    """
    MAX_PILLAR_3A_EMPLOYED = 7056  # 2024 limit for employed persons

    # Validate Pillar 3a (cap at maximum)
    pillar_3a = min(data['pillar_3a_contribution'], MAX_PILLAR_3A_EMPLOYED)

    # Pillar 2 additional contributions (unlimited but must be validated)
    pillar_2_additional = data['pillar_2_additional_contribution']

    # Other deductions (professional expenses, insurance premiums, etc.)
    other = data['other_deductions']

    # Note: Zurich doesn't have standard child deductions on income tax
    # These are placeholders for extensibility
    child_deduction = 0
    dependent_deduction = 0

    total = pillar_3a + pillar_2_additional + other + child_deduction + dependent_deduction

    return {
        'pillar_3a': pillar_3a,
        'pillar_2_additional': pillar_2_additional,
        'other': other,
        'child_deduction': child_deduction,
        'dependent_deduction': dependent_deduction,
        'total': total
    }
```

### Validation Rules

**Pillar 3a**:
- Maximum CHF 7,056 for employed persons (2024)
- Maximum CHF 35,280 for self-employed persons (not currently implemented)
- Display error if exceeded
- Show remaining contribution room

## Tax Calculation Algorithms

### 1. Federal Tax Calculation

```python
def calculate_federal_tax(income, deductions=0):
    """
    Calculate Swiss federal income tax (DBG).

    Returns comprehensive tax result including:
    - Total tax
    - Effective rate
    - Marginal rate
    - Current bracket index
    - Breakdown by bracket
    - Progress within current bracket
    - Amount to next bracket
    """

    # Calculate taxable income
    taxable_income = max(0, income - deductions)

    if taxable_income <= 0:
        return create_zero_tax_result(income, deductions)

    # Find current bracket
    current_bracket_index = 0
    for i in range(len(FEDERAL_TAX_BRACKETS) - 1, -1, -1):
        if taxable_income >= FEDERAL_TAX_BRACKETS[i]['threshold']:
            current_bracket_index = i
            break

    current_bracket = FEDERAL_TAX_BRACKETS[current_bracket_index]
    next_bracket = FEDERAL_TAX_BRACKETS[current_bracket_index + 1] if current_bracket_index + 1 < len(FEDERAL_TAX_BRACKETS) else None

    # Calculate total tax using Swiss federal formula
    excess_income = taxable_income - current_bracket['threshold']
    tax_on_excess = (excess_income / 100) * current_bracket['rate_per_hundred']
    total_tax = current_bracket['base_tax'] + tax_on_excess

    # Calculate effective rate (based on ORIGINAL income, not taxable income)
    effective_rate = (total_tax / income * 100) if income > 0 else 0

    # Marginal rate is the rate per hundred at current bracket
    marginal_rate = current_bracket['rate_per_hundred']

    # Calculate progress within current bracket
    if next_bracket:
        bracket_range = next_bracket['threshold'] - current_bracket['threshold']
        position_in_bracket = taxable_income - current_bracket['threshold']
        progress_in_bracket = (position_in_bracket / bracket_range) * 100
        amount_to_next_bracket = next_bracket['threshold'] - taxable_income
    else:
        progress_in_bracket = 100  # At top bracket
        amount_to_next_bracket = 0

    # Calculate breakdown for each bracket
    breakdown = get_federal_bracket_breakdown(taxable_income, current_bracket_index)

    return {
        'total_tax': total_tax,
        'effective_rate': effective_rate,
        'marginal_rate': marginal_rate,
        'current_bracket_index': current_bracket_index,
        'breakdown': breakdown,
        'progress_in_bracket': progress_in_bracket,
        'amount_to_next_bracket': amount_to_next_bracket,
        'taxable_income': taxable_income,
        'total_deductions': deductions
    }


def get_federal_bracket_breakdown(income, current_bracket_index):
    """
    Calculate how much tax is paid in each bracket.

    Returns list of:
    {
        'bracket_index': int,
        'range_start': float,
        'range_end': float,
        'rate': float,           # Rate per hundred
        'taxable_amount': float,  # Amount of income in this bracket
        'tax_paid': float,        # Tax paid on amount in this bracket
        'is_active': bool         # Whether this is the current bracket
    }
    """
    breakdown = []

    for i, bracket in enumerate(FEDERAL_TAX_BRACKETS):
        next_bracket = FEDERAL_TAX_BRACKETS[i + 1] if i + 1 < len(FEDERAL_TAX_BRACKETS) else None

        # Skip first bracket if it has 0 rate (tax-free threshold)
        if bracket['rate_per_hundred'] == 0 and i == 0:
            continue

        range_start = bracket['threshold']
        range_end = next_bracket['threshold'] if next_bracket else float('inf')

        # Calculate taxable amount in this bracket
        taxable_amount = 0
        if income > range_start:
            if income >= range_end:
                taxable_amount = range_end - range_start
            else:
                taxable_amount = income - range_start

        # Calculate tax paid in this bracket
        tax_paid = (taxable_amount / 100) * bracket['rate_per_hundred']

        if taxable_amount > 0 or i <= current_bracket_index:
            breakdown.append({
                'bracket_index': i,
                'range_start': range_start,
                'range_end': range_end,
                'rate': bracket['rate_per_hundred'],
                'taxable_amount': taxable_amount,
                'tax_paid': tax_paid,
                'is_active': i == current_bracket_index
            })

    return breakdown
```

### 2. Zurich Cantonal Tax Calculation

```python
def calculate_zurich_tax(income, gemeinde_steuerfuss=119, deductions=0):
    """
    Calculate Zurich cantonal and municipal taxes.

    The system works in two steps:
    1. Calculate "Einfache Staatssteuer" (simple state tax) using progressive brackets
    2. Apply tax multipliers (Steuerfüsse) to get actual cantonal and municipal taxes

    Returns:
    {
        'einfache_staatssteuer': float,    # Base simple state tax
        'kantonale_steuer': float,         # Cantonal tax (einfache × 98%)
        'gemeinde_steuer': float,          # Municipal tax (einfache × gemeinde_steuerfuss%)
        'total_steuer': float,             # Total cantonal + municipal
        'effective_rate': float,           # Total as % of income
        'marginal_rate': float,            # Current bracket rate
        'current_bracket_index': int,
        'breakdown': list,
        'progress_in_bracket': float,
        'amount_to_next_bracket': float,
        'taxable_income': float,
        'total_deductions': float
    }
    """

    taxable_income = max(0, income - deductions)

    if taxable_income <= 0:
        return create_zero_zurich_tax_result(income, deductions)

    # Step 1: Calculate Einfache Staatssteuer (simple state tax)
    einfache_staatssteuer = 0
    current_bracket_index = 0
    breakdown = []

    for i, bracket in enumerate(ZURICH_TAX_BRACKETS):
        next_bracket = ZURICH_TAX_BRACKETS[i + 1] if i + 1 < len(ZURICH_TAX_BRACKETS) else None

        if taxable_income > bracket['threshold']:
            current_bracket_index = i

        # Skip the first (0%) bracket for breakdown display
        if bracket['rate'] == 0:
            continue

        range_start = bracket['threshold']
        range_end = next_bracket['threshold'] if next_bracket else float('inf')

        # Calculate taxable amount in this bracket
        taxable_amount = 0
        if taxable_income > range_start:
            if next_bracket and taxable_income >= range_end:
                taxable_amount = range_end - range_start
            elif taxable_income > range_start:
                taxable_amount = taxable_income - range_start

        # Calculate tax for this bracket
        tax_paid = (taxable_amount * bracket['rate']) / 100
        einfache_staatssteuer += tax_paid

        if taxable_amount > 0:
            breakdown.append({
                'bracket_index': i,
                'range_start': range_start,
                'range_end': range_end,
                'rate': bracket['rate'],
                'taxable_amount': taxable_amount,
                'tax_paid': tax_paid,
                'is_active': i == current_bracket_index
            })

    # Step 2: Apply Steuerfüsse (tax multipliers)
    kantonale_steuer = (einfache_staatssteuer * CANTONAL_STEUERFUSS) / 100
    gemeinde_steuer = (einfache_staatssteuer * gemeinde_steuerfuss) / 100
    total_steuer = kantonale_steuer + gemeinde_steuer

    # Calculate effective rate (based on ORIGINAL income, not taxable income)
    effective_rate = (total_steuer / income * 100) if income > 0 else 0

    # Get current bracket info
    current_bracket = ZURICH_TAX_BRACKETS[current_bracket_index]
    next_bracket = ZURICH_TAX_BRACKETS[current_bracket_index + 1] if current_bracket_index + 1 < len(ZURICH_TAX_BRACKETS) else None
    marginal_rate = current_bracket['rate']

    # Calculate progress within current bracket
    if next_bracket:
        bracket_range = next_bracket['threshold'] - current_bracket['threshold']
        position_in_bracket = taxable_income - current_bracket['threshold']
        progress_in_bracket = (position_in_bracket / bracket_range) * 100
        amount_to_next_bracket = next_bracket['threshold'] - taxable_income
    else:
        progress_in_bracket = 100
        amount_to_next_bracket = 0

    return {
        'einfache_staatssteuer': einfache_staatssteuer,
        'kantonale_steuer': kantonale_steuer,
        'gemeinde_steuer': gemeinde_steuer,
        'total_steuer': total_steuer,
        'effective_rate': effective_rate,
        'marginal_rate': marginal_rate,
        'current_bracket_index': current_bracket_index,
        'breakdown': breakdown,
        'progress_in_bracket': progress_in_bracket,
        'amount_to_next_bracket': amount_to_next_bracket,
        'taxable_income': taxable_income,
        'total_deductions': deductions
    }
```

### 3. Church Tax Calculation

```python
# Church tax multipliers (approximate averages - actual rates vary by parish)
CHURCH_TAX_MULTIPLIERS = {
    'none': 0,
    'reformed': 0.10,           # 10% of (cantonal + municipal tax)
    'catholic': 0.15,           # 15% of (cantonal + municipal tax)
    'christian-catholic': 0.15  # 15% of (cantonal + municipal tax)
}


def calculate_church_tax(einfache_staatssteuer, kantonal_steuerfuss,
                        gemeinde_steuerfuss, religious_affiliation, income):
    """
    Calculate church tax for Zurich canton.

    Church tax is calculated as a percentage of the total cantonal + municipal tax.

    Returns:
    {
        'church_tax': float,
        'effective_rate': float,
        'denomination': str,
        'applied': bool
    }
    """

    if religious_affiliation == 'none' or income <= 0:
        return {
            'church_tax': 0,
            'effective_rate': 0,
            'denomination': religious_affiliation,
            'applied': False
        }

    # Church tax is based on total cantonal + municipal tax
    total_cantonal_municipal_tax = (
        (einfache_staatssteuer * kantonal_steuerfuss / 100) +
        (einfache_staatssteuer * gemeinde_steuerfuss / 100)
    )

    multiplier = CHURCH_TAX_MULTIPLIERS[religious_affiliation]
    church_tax = total_cantonal_municipal_tax * multiplier
    effective_rate = (church_tax / income * 100) if income > 0 else 0

    return {
        'church_tax': church_tax,
        'effective_rate': effective_rate,
        'denomination': religious_affiliation,
        'applied': True
    }
```

### 4. Wealth Tax Calculation

```python
def calculate_wealth_tax(total_wealth, number_of_children,
                        kantonal_steuerfuss, gemeinde_steuerfuss):
    """
    Calculate wealth tax for Zurich canton.

    Process:
    1. Calculate deductions (CHF 82,200 per adult + CHF 41,100 per child)
    2. Calculate taxable wealth
    3. Calculate "einfache" wealth tax using progressive brackets (rates in ‰)
    4. Apply cantonal and municipal Steuerfüsse

    Returns:
    {
        'taxable_wealth': float,
        'wealth_tax': float,
        'kantonale_wealth_tax': float,
        'gemeinde_wealth_tax': float,
        'effective_rate': float,
        'deductions': float
    }
    """

    if total_wealth <= 0:
        return create_zero_wealth_tax_result()

    # Calculate deductions (1 adult for single, + children)
    deductions = WEALTH_DEDUCTION_PER_ADULT + (number_of_children * WEALTH_DEDUCTION_PER_CHILD)
    taxable_wealth = max(0, total_wealth - deductions)

    if taxable_wealth == 0:
        return {
            'taxable_wealth': 0,
            'wealth_tax': 0,
            'kantonale_wealth_tax': 0,
            'gemeinde_wealth_tax': 0,
            'effective_rate': 0,
            'deductions': deductions
        }

    # Calculate "einfache" wealth tax using brackets
    einfache_wealth_tax = 0

    for i, bracket in enumerate(WEALTH_TAX_BRACKETS):
        next_bracket = WEALTH_TAX_BRACKETS[i + 1] if i + 1 < len(WEALTH_TAX_BRACKETS) else None

        if taxable_wealth <= bracket['threshold']:
            break

        taxable_in_bracket = (
            min(taxable_wealth, next_bracket['threshold']) - bracket['threshold']
            if next_bracket
            else taxable_wealth - bracket['threshold']
        )

        einfache_wealth_tax += (taxable_in_bracket / 1000) * bracket['rate_per_thousand']

    # Apply Steuerfüsse
    kantonale_wealth_tax = (einfache_wealth_tax * kantonal_steuerfuss) / 100
    gemeinde_wealth_tax = (einfache_wealth_tax * gemeinde_steuerfuss) / 100
    wealth_tax = kantonale_wealth_tax + gemeinde_wealth_tax

    effective_rate = (wealth_tax / total_wealth * 100) if total_wealth > 0 else 0

    return {
        'taxable_wealth': taxable_wealth,
        'wealth_tax': wealth_tax,
        'kantonale_wealth_tax': kantonale_wealth_tax,
        'gemeinde_wealth_tax': gemeinde_wealth_tax,
        'effective_rate': effective_rate,
        'deductions': deductions
    }
```

## User Interface Components

### Input Controls ("Slider Logic")

The application uses numeric input fields rather than traditional sliders. Each input has:

1. **Income Input**:
   - Text input with numeric filtering
   - Formatted display (e.g., "100,000" in Swiss format)
   - Currency prefix "CHF"
   - Real-time validation and formatting

2. **Municipality Select**:
   - Dropdown selector for municipality
   - Automatically updates gemeinde_steuerfuss when selected
   - Pre-populated with common Zurich municipalities

3. **Personal Details**:
   - Number of children (numeric input, 0-20)
   - Number of dependents (numeric input, 0-20)
   - Religious affiliation (dropdown select)
   - Total wealth (numeric input with CHF formatting)

4. **Deductions**:
   - Pillar 3a contributions (numeric input, max CHF 7,056)
     - Shows remaining contribution room
     - Displays error if exceeds limit
   - Pillar 2 additional contributions (numeric input, unlimited)
   - Other deductions (numeric input)

### UI Layout

The application uses a tabbed interface:

**Tab 1: Questionnaire**
- Income & Location card
- Personal Details card
- Voluntary Deductions card

**Tab 2: Tax Results**
- Total tax summary card
- Breakdown cards (4-column grid):
  - Federal tax
  - Cantonal tax (with steuerfuss)
  - Municipal tax (with steuerfuss)
  - Einfache Staatssteuer
- Church tax card (conditional - only if applicable)
- Wealth tax card (conditional - only if wealth > 0)
- Deductions breakdown (conditional - only if deductions > 0)
- Bracket progress visualization
- Tax chart (visual representation of tax by income)
- Federal bracket breakdown table
- Cantonal bracket breakdown table

### Real-Time Calculation

All calculations update immediately when any input changes:

```python
# State management pattern
def on_input_change(field, value):
    # Update form data
    form_data[field] = value

    # Recalculate deductions
    deductions_breakdown = calculate_deductions(form_data)

    # Recalculate all taxes
    federal_result = calculate_federal_tax(
        form_data['income'],
        deductions_breakdown['total']
    )

    zurich_result = calculate_zurich_tax(
        form_data['income'],
        form_data['gemeinde_steuerfuss'],
        deductions_breakdown['total']
    )

    church_tax_result = calculate_church_tax(
        zurich_result['einfache_staatssteuer'],
        CANTONAL_STEUERFUSS,
        form_data['gemeinde_steuerfuss'],
        form_data['religious_affiliation'],
        form_data['income']
    )

    wealth_tax_result = calculate_wealth_tax(
        form_data['total_wealth'],
        form_data['number_of_children'],
        CANTONAL_STEUERFUSS,
        form_data['gemeinde_steuerfuss']
    )

    # Calculate total tax
    total_tax = (
        federal_result['total_tax'] +
        zurich_result['total_steuer'] +
        church_tax_result['church_tax'] +
        wealth_tax_result['wealth_tax']
    )

    # Update UI
    render_results(total_tax, federal_result, zurich_result,
                   church_tax_result, wealth_tax_result)
```

## Visualization Components

### 1. Bracket Progress Bar

Shows visual progress through current tax bracket:
- Current bracket highlighted
- Progress bar showing position within bracket (0-100%)
- Text showing "CHF X to next bracket"

### 2. Tax Chart

Line chart showing:
- X-axis: Income levels (CHF 0 to max)
- Y-axis: Tax amount or effective rate
- Multiple lines for different tax types
- Generated using income steps (e.g., every CHF 1,000)

```python
def generate_chart_data(max_income=200000, step=1000):
    """
    Generate chart data points for visualization.

    Returns list of:
    {
        'income': float,
        'tax': float,
        'rate': float
    }
    """
    data = []

    for income in range(0, max_income + step, step):
        result = calculate_federal_tax(income)
        data.append({
            'income': income,
            'tax': result['total_tax'],
            'rate': result['effective_rate']
        })

    return data
```

### 3. Bracket Breakdown Table

Table showing breakdown by bracket:
- Columns: Bracket range, Rate, Income in bracket, Tax paid
- Current bracket highlighted
- Shows cumulative tax calculation

## Formatting Utilities

```python
def format_currency(amount):
    """Format amount as Swiss currency (CHF)."""
    return f"CHF {amount:,.2f}".replace(',', "'")
    # Swiss format uses apostrophe as thousands separator
    # Example: CHF 100'000.00


def format_number(amount):
    """Format number with Swiss thousands separator."""
    return f"{int(amount):,}".replace(',', "'")
    # Example: 100'000


def format_percent(rate):
    """Format percentage with 2 decimal places."""
    return f"{rate:.2f}%"
    # Example: 12.34%
```

## Complete Implementation Example (Streamlit)

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# [Include all tax bracket definitions and calculation functions from above]

def main():
    st.set_page_config(
        page_title="Swiss Tax Calculator",
        page_icon="🇨🇭",
        layout="wide"
    )

    st.title("Swiss Tax Calculator")
    st.caption("Calculate your Swiss federal, cantonal, church, and wealth taxes")

    # Create tabs
    tab1, tab2 = st.tabs(["Questionnaire", "Tax Results"])

    with tab1:
        # Income & Location Section
        st.subheader("Income & Location")
        col1, col2 = st.columns(2)

        with col1:
            income = st.number_input(
                "Annual Income (CHF)",
                min_value=0,
                value=100000,
                step=1000,
                format="%d"
            )

        with col2:
            municipality = st.selectbox(
                "Municipality",
                options=list(MUNICIPALITY_STEUERFUESSE.keys()),
                index=0
            )
            gemeinde_steuerfuss = MUNICIPALITY_STEUERFUESSE[municipality]
            st.caption(f"Gemeinde Steuerfuss: {gemeinde_steuerfuss}%")

        # Personal Details Section
        st.subheader("Personal Details")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            number_of_children = st.number_input(
                "Number of Children",
                min_value=0,
                max_value=20,
                value=0,
                help="Children under 18 or in education"
            )

        with col2:
            number_of_dependents = st.number_input(
                "Other Dependents",
                min_value=0,
                max_value=20,
                value=0,
                help="Other persons you support"
            )

        with col3:
            religious_affiliation = st.selectbox(
                "Religious Affiliation",
                options=['none', 'reformed', 'catholic', 'christian-catholic'],
                format_func=lambda x: {
                    'none': 'None / No church tax',
                    'reformed': 'Reformed Protestant',
                    'catholic': 'Roman Catholic',
                    'christian-catholic': 'Christian Catholic'
                }[x],
                help="Determines church tax liability"
            )

        with col4:
            total_wealth = st.number_input(
                "Total Net Wealth (CHF)",
                min_value=0,
                value=0,
                step=10000,
                help="Total assets minus liabilities"
            )

        # Deductions Section
        st.subheader("Voluntary Deductions")
        col1, col2, col3 = st.columns(3)

        with col1:
            pillar_3a = st.number_input(
                "Pillar 3a Contributions (CHF)",
                min_value=0,
                max_value=7056,
                value=0,
                step=100,
                help=f"2024 limit: CHF 7,056 (employed)"
            )
            if pillar_3a > 0:
                remaining = 7056 - pillar_3a
                st.caption(f"Remaining: CHF {remaining:,}")

        with col2:
            pillar_2_additional = st.number_input(
                "Pillar 2 Additional Contributions (CHF)",
                min_value=0,
                value=0,
                step=1000,
                help="Additional purchases into your pension fund"
            )

        with col3:
            other_deductions = st.number_input(
                "Other Deductions (CHF)",
                min_value=0,
                value=0,
                step=1000,
                help="Professional expenses, insurance premiums, etc."
            )

    # Calculate all taxes
    form_data = {
        'income': income,
        'municipality': municipality,
        'gemeinde_steuerfuss': gemeinde_steuerfuss,
        'number_of_children': number_of_children,
        'number_of_dependents': number_of_dependents,
        'religious_affiliation': religious_affiliation,
        'total_wealth': total_wealth,
        'pillar_3a_contribution': pillar_3a,
        'pillar_2_additional_contribution': pillar_2_additional,
        'other_deductions': other_deductions
    }

    deductions_breakdown = calculate_deductions(form_data)
    federal_result = calculate_federal_tax(income, deductions_breakdown['total'])
    zurich_result = calculate_zurich_tax(income, gemeinde_steuerfuss, deductions_breakdown['total'])
    church_tax_result = calculate_church_tax(
        zurich_result['einfache_staatssteuer'],
        CANTONAL_STEUERFUSS,
        gemeinde_steuerfuss,
        religious_affiliation,
        income
    )
    wealth_tax_result = calculate_wealth_tax(
        total_wealth,
        number_of_children,
        CANTONAL_STEUERFUSS,
        gemeinde_steuerfuss
    )

    total_tax = (
        federal_result['total_tax'] +
        zurich_result['total_steuer'] +
        church_tax_result['church_tax'] +
        wealth_tax_result['wealth_tax']
    )

    with tab2:
        # Total Tax Summary
        st.metric(
            "Total Tax Liability",
            format_currency(total_tax),
            delta=f"{(total_tax / income * 100):.2f}% of income" if income > 0 else None
        )

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Gross Income", format_currency(income))
        with col2:
            st.metric("Total Deductions", format_currency(deductions_breakdown['total']))

        st.divider()

        # Tax Breakdown Cards
        st.subheader("Tax Breakdown")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Federal Tax",
                format_currency(federal_result['total_tax']),
                delta=f"{federal_result['effective_rate']:.2f}% effective"
            )

        with col2:
            st.metric(
                "Cantonal Tax (ZH)",
                format_currency(zurich_result['kantonale_steuer']),
                delta=f"{CANTONAL_STEUERFUSS}% Steuerfuss"
            )

        with col3:
            st.metric(
                "Municipal Tax",
                format_currency(zurich_result['gemeinde_steuer']),
                delta=f"{gemeinde_steuerfuss}% Steuerfuss"
            )

        with col4:
            st.metric(
                "Einfache Staatssteuer",
                format_currency(zurich_result['einfache_staatssteuer']),
                delta="Base tax"
            )

        # Church Tax (if applicable)
        if church_tax_result['applied']:
            st.divider()
            st.subheader("Church Tax")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Church Tax", format_currency(church_tax_result['church_tax']))
            with col2:
                st.metric("Denomination", church_tax_result['denomination'].title())
            with col3:
                st.metric("Effective Rate", format_percent(church_tax_result['effective_rate']))

        # Wealth Tax (if applicable)
        if wealth_tax_result['wealth_tax'] > 0:
            st.divider()
            st.subheader("Wealth Tax")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Wealth Tax", format_currency(wealth_tax_result['wealth_tax']))
            with col2:
                st.metric("Taxable Wealth", format_currency(wealth_tax_result['taxable_wealth']))
            with col3:
                st.metric("Deductions", format_currency(wealth_tax_result['deductions']))

        # Deductions Breakdown
        if deductions_breakdown['total'] > 0:
            st.divider()
            st.subheader("Deductions Breakdown")

            deductions_df = pd.DataFrame([
                {"Type": "Pillar 3a", "Amount": deductions_breakdown['pillar_3a']},
                {"Type": "Pillar 2 Additional", "Amount": deductions_breakdown['pillar_2_additional']},
                {"Type": "Other", "Amount": deductions_breakdown['other']},
            ])

            deductions_df = deductions_df[deductions_df['Amount'] > 0]
            deductions_df['Amount'] = deductions_df['Amount'].apply(format_currency)

            st.dataframe(deductions_df, use_container_width=True, hide_index=True)

        # Bracket Progress
        st.divider()
        st.subheader("Federal Tax Bracket Progress")

        current_bracket = FEDERAL_TAX_BRACKETS[federal_result['current_bracket_index']]
        next_bracket_idx = federal_result['current_bracket_index'] + 1

        if next_bracket_idx < len(FEDERAL_TAX_BRACKETS):
            next_bracket = FEDERAL_TAX_BRACKETS[next_bracket_idx]

            st.progress(federal_result['progress_in_bracket'] / 100)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Bracket", f"{format_currency(current_bracket['threshold'])}+")
            with col2:
                st.metric("Next Bracket", format_currency(next_bracket['threshold']))
            with col3:
                st.metric("Amount to Next", format_currency(federal_result['amount_to_next_bracket']))

        # Tax Chart
        st.divider()
        st.subheader("Tax Visualization")

        chart_data = generate_chart_data(max_income=min(income * 2, 300000), step=1000)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=[d['income'] for d in chart_data],
            y=[d['tax'] for d in chart_data],
            mode='lines',
            name='Federal Tax',
            line=dict(color='blue', width=2)
        ))

        fig.add_vline(x=income, line_dash="dash", line_color="red",
                     annotation_text="Your Income")

        fig.update_layout(
            xaxis_title="Income (CHF)",
            yaxis_title="Tax (CHF)",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Federal Bracket Breakdown Table
        st.divider()
        st.subheader("Federal Tax Bracket Breakdown")

        breakdown_df = pd.DataFrame([
            {
                "Bracket": f"{format_currency(b['range_start'])} - {format_currency(b['range_end']) if b['range_end'] != float('inf') else '∞'}",
                "Rate": format_percent(b['rate']),
                "Income in Bracket": format_currency(b['taxable_amount']),
                "Tax Paid": format_currency(b['tax_paid']),
                "Active": "✓" if b['is_active'] else ""
            }
            for b in federal_result['breakdown']
        ])

        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)

        # Zurich Bracket Breakdown Table
        st.divider()
        st.subheader("Zurich Cantonal Tax Bracket Breakdown")

        zurich_breakdown_df = pd.DataFrame([
            {
                "Bracket": f"{format_currency(b['range_start'])} - {format_currency(b['range_end']) if b['range_end'] != float('inf') else '∞'}",
                "Rate": format_percent(b['rate']),
                "Income in Bracket": format_currency(b['taxable_amount']),
                "Einfache Tax Paid": format_currency(b['tax_paid']),
                "Active": "✓" if b['is_active'] else ""
            }
            for b in zurich_result['breakdown']
        ])

        st.dataframe(zurich_breakdown_df, use_container_width=True, hide_index=True)

    # Footer
    st.divider()
    st.caption("""
    **Sources:**
    - Federal tax based on [DBG (fedlex.admin.ch)](https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de)
    - Cantonal tax based on [StG § 35 (zh.ch)](https://www.zh.ch/de/steuern-finanzen/steuern/treuhaender/steuerbuch/steuerbuch-definition/zstb-34-1.html)

    **Important:** Tax calculations are estimates based on 2024 rates and standard deductions.
    Church tax rates are approximate averages (10% Reformed, 15% Catholic) and vary by parish.
    Actual tax liability may differ based on individual circumstances.
    Consult official sources and tax professionals for exact calculations.
    """)


if __name__ == "__main__":
    main()
```

## Key Implementation Notes

1. **Reactive Updates**: All calculations should update immediately when any input changes
2. **Validation**: Validate inputs (especially Pillar 3a limit) and show helpful error messages
3. **Formatting**: Use Swiss number formatting (apostrophe as thousands separator)
4. **Currency**: Always display CHF with 2 decimal places
5. **Conditional Display**: Only show church tax and wealth tax sections when applicable
6. **Progressive Enhancement**: Start with basic calculations, add visualizations later
7. **State Management**: Keep all form data in a single state object for easy passing to calculation functions
8. **Separation of Concerns**: Keep calculation logic separate from UI components

## Testing Scenarios

Test the calculator with these scenarios:

1. **Low Income**: CHF 50,000 → Should pay minimal federal tax, moderate cantonal
2. **Middle Income**: CHF 100,000 → Balanced across brackets
3. **High Income**: CHF 200,000 → Higher brackets activated
4. **With Deductions**: CHF 100,000 - CHF 7,056 (Pillar 3a) → Lower taxable income
5. **With Church Tax**: Reformed at CHF 100,000 → Additional ~10% of cantonal+municipal
6. **With Wealth**: CHF 500,000 wealth with 2 children → Wealth tax after deductions
7. **Different Municipalities**: Compare Zürich (119%) vs Zollikon (77%) → Significant municipal tax difference

## Extension Possibilities

- Add married couples (different tax brackets)
- Add federal wealth tax calculation
- Support other cantons
- Multi-year comparison
- Tax optimization suggestions
- Export to PDF
- Save/load scenarios
- Historical rate comparisons
