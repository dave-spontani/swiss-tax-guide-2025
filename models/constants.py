"""
Swiss Tax Constants - Zurich Canton 2024
Based on official tax brackets and deduction rules
"""

# ============================================================================
# FEDERAL TAX BRACKETS (DBG - Direct Federal Tax)
# Source: https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de (Art. 36 DBG)
# ============================================================================

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

# ============================================================================
# ZURICH CANTONAL TAX BRACKETS
# Source: StG § 35 (adjusted for 2024 cold progression: 3.3%)
# ============================================================================

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

# Cantonal Steuerfuss (tax multiplier) - 2024
CANTONAL_STEUERFUSS = 98  # 98% for Zurich canton (2024)

# Municipal Steuerfüsse (tax multipliers by municipality) - 2026
MUNICIPALITY_STEUERFUESSE = {
    'Zürich': 119,
    'Winterthur': 122,
    'Uster': 108,
    'Dübendorf': 96,
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

# ============================================================================
# WEALTH TAX BRACKETS (Zurich)
# ============================================================================

WEALTH_TAX_BRACKETS = [
    {'threshold': 0,        'rate_per_thousand': 0},     # Tax-free below CHF 77,000
    {'threshold': 77000,    'rate_per_thousand': 0.5},   # 0.5‰
    {'threshold': 308000,   'rate_per_thousand': 1.0},   # 1.0‰
    {'threshold': 3158000,  'rate_per_thousand': 3.0},   # 3.0‰
]

# Wealth deductions
WEALTH_DEDUCTION_PER_ADULT = 82200   # CHF 82,200 per adult
WEALTH_DEDUCTION_PER_CHILD = 41100   # CHF 41,100 per child

# Personalsteuer (flat personal tax)
PERSONALSTEUER = 24  # CHF 24 annual personal tax

# ============================================================================
# CHURCH TAX MULTIPLIERS (Zurich)
# ============================================================================

CHURCH_TAX_MULTIPLIERS = {
    'none': 0,
    'reformed': 0.10,           # 10% of Einfache Staatssteuer
    'catholic': 0.11,           # 11% of Einfache Staatssteuer
    'christian-catholic': 0.15  # 15% of Einfache Staatssteuer (verify)
}

# ============================================================================
# DEDUCTION LIMITS AND CONSTANTS
# ============================================================================

# Pillar 3a limits (2025)
PILLAR_3A_MAX_EMPLOYED = 7258      # For employed persons (2025)
PILLAR_3A_MAX_SELF_EMPLOYED = 36288  # For self-employed (20% of income, 2025)

# Pillar 3a retroactive contributions (new from 2026)
PILLAR_3A_RETROACTIVE_ENABLED = True  # Can make retroactive contributions from 2026
PILLAR_3A_RETROACTIVE_FIRST_YEAR = 2025  # Earliest gap year that can be filled
PILLAR_3A_RETROACTIVE_MAX_YEARS = 10  # Can go back max 10 years

# Professional expense deductions
COMMUTING_PAUSCHAL = 700            # CHF 700 automatic
MEAL_COSTS_WITH_SUBSIDY = 1600      # CHF 7.50/day × 220 days
MEAL_COSTS_WITHOUT_SUBSIDY = 3200   # CHF 15/day × 220 days
PROFESSIONAL_EXPENSES_RATE = 0.03   # 3% of net salary
PROFESSIONAL_EXPENSES_MAX = 4000    # Max CHF 4,000
SIDE_INCOME_DEDUCTION = 2400        # 20% or max CHF 2,400

# Property deductions (Zurich)
PROPERTY_MAINTENANCE_PAUSCHAL = 0.20  # 20% of Eigenmietwert

# Asset management (Zurich)
ASSET_MANAGEMENT_RATE = 0.003       # 3‰ (3 per thousand)
ASSET_MANAGEMENT_MAX = 6000         # Max CHF 6,000

# Family deductions (Zurich)
CHILD_DEDUCTION_ZH = 9000           # CHF 9,000 per child
DUAL_INCOME_DEDUCTION_ZH = 5900     # CHF 5,900 for dual income

# Childcare deduction
CHILDCARE_MAX = 10100               # Max CHF 10,100

# Insurance premium limits (Zurich)
INSURANCE_LIMITS_ZH = {
    'married_with_pension': 5200,
    'married_without_pension': 7800,
    'single_with_pension': 2600,
    'single_without_pension': 3900,
    'per_child': 1300,
}

# Debt interest limits
DEBT_INTEREST_MAX = 50000           # Max CHF 50,000 + investment income

# Donations
DONATIONS_MAX_RATE = 0.20           # Max 20% of net income

# Political contributions (Zurich)
POLITICAL_CONTRIB_MAX_SINGLE = 10000
POLITICAL_CONTRIB_MAX_MARRIED = 20000

# Support payments
SUPPORT_PAYMENT_MIN = 6500          # Min CHF 6,500 (federal)
SUPPORT_PAYMENT_MIN_ZH = 2700       # Min CHF 2,700 (Zurich)

# Medical costs
MEDICAL_COSTS_DEDUCTIBLE_RATE = 0.05  # 5% deductible (Zurich)
