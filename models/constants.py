"""
Swiss Tax Constants - Zurich Canton 2024
Based on official tax brackets and deduction rules
"""

# ============================================================================
# FEDERAL TAX BRACKETS (DBG - Direct Federal Tax)
# Source: https://www.fedlex.admin.ch/eli/cc/1991/1184_1184_1184/de (Art. 36 DBG)
# Updated: 2024 (includes cold progression adjustment from Sept 2023)
# ============================================================================

# Federal tax brackets for SINGLE individuals (Art. 36 Abs. 1)
FEDERAL_TAX_BRACKETS = [
    {'threshold': 0,       'base_tax': 0,        'rate_per_hundred': 0},      # Tax-free
    {'threshold': 15000,   'base_tax': 0,        'rate_per_hundred': 0.77},
    {'threshold': 32800,   'base_tax': 137.05,   'rate_per_hundred': 0.88},
    {'threshold': 42900,   'base_tax': 225.90,   'rate_per_hundred': 2.64},
    {'threshold': 57200,   'base_tax': 603.40,   'rate_per_hundred': 2.97},
    {'threshold': 75200,   'base_tax': 1138.00,  'rate_per_hundred': 5.94},
    {'threshold': 81000,   'base_tax': 1482.50,  'rate_per_hundred': 6.60},
    {'threshold': 107400,  'base_tax': 3224.90,  'rate_per_hundred': 8.80},
    {'threshold': 139600,  'base_tax': 6058.50,  'rate_per_hundred': 11.00},
    {'threshold': 182600,  'base_tax': 10788.50, 'rate_per_hundred': 13.20},
    {'threshold': 783200,  'base_tax': 90067.70, 'rate_per_hundred': 0},      # Cap
    {'threshold': 783300,  'base_tax': 90079.50, 'rate_per_hundred': 11.50},  # Higher incomes
]

# Federal tax brackets for MARRIED couples (Art. 36 Abs. 2)
# For married couples in legally and factually unseparated marriage
FEDERAL_TAX_BRACKETS_MARRIED = [
    {'threshold': 0,       'base_tax': 0,        'rate_per_hundred': 0},      # Tax-free
    {'threshold': 29300,   'base_tax': 0,        'rate_per_hundred': 1.00},
    {'threshold': 52700,   'base_tax': 234.00,   'rate_per_hundred': 2.00},
    {'threshold': 60500,   'base_tax': 390.00,   'rate_per_hundred': 3.00},
    {'threshold': 78100,   'base_tax': 918.00,   'rate_per_hundred': 4.00},
    {'threshold': 93600,   'base_tax': 1538.00,  'rate_per_hundred': 5.00},
    {'threshold': 107200,  'base_tax': 2218.00,  'rate_per_hundred': 6.00},
    {'threshold': 119000,  'base_tax': 2926.00,  'rate_per_hundred': 7.00},
    {'threshold': 128800,  'base_tax': 3612.00,  'rate_per_hundred': 8.00},
    {'threshold': 136600,  'base_tax': 4236.00,  'rate_per_hundred': 9.00},
    {'threshold': 142300,  'base_tax': 4749.00,  'rate_per_hundred': 10.00},
    {'threshold': 146300,  'base_tax': 5149.00,  'rate_per_hundred': 11.00},
    {'threshold': 148300,  'base_tax': 5369.00,  'rate_per_hundred': 12.00},
    {'threshold': 150300,  'base_tax': 5609.00,  'rate_per_hundred': 13.00},
    {'threshold': 928600,  'base_tax': 106788.00, 'rate_per_hundred': 0},     # Cap
    {'threshold': 928700,  'base_tax': 106800.50, 'rate_per_hundred': 11.50}, # Higher incomes
]

# ============================================================================
# ZURICH CANTONAL TAX BRACKETS
# Source: StG § 35 (adjusted for 2024 cold progression: 3.3%)
# ============================================================================

# Zurich tax brackets for SINGLE individuals (Grundtarif - § 35 Abs. 1)
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

# Zurich tax brackets for MARRIED couples (Verheiratetentarif - § 35 Abs. 2)
# TODO: VERIFY THESE BRACKETS - Approximated based on federal married/single ratio
# Official source should be verified at: https://www.zh.ch/de/steuern-finanzen/steuern/
# Contact Zurich tax authority or use official calculator for exact values
ZURICH_TAX_BRACKETS_MARRIED = [
    {'threshold': 0,       'rate': 0},   # Tax-free (estimate: ~CHF 13,800)
    {'threshold': 13800,   'rate': 1},   # Approximate
    {'threshold': 23600,   'rate': 2},   # Approximate
    {'threshold': 33200,   'rate': 3},   # Approximate
    {'threshold': 49000,   'rate': 4},   # Approximate
    {'threshold': 68200,   'rate': 5},   # Approximate
    {'threshold': 90200,   'rate': 6},   # Approximate
    {'threshold': 116000,  'rate': 7},   # Approximate
    {'threshold': 150800,  'rate': 8},   # Approximate
    {'threshold': 218000,  'rate': 9},   # Approximate
    {'threshold': 284400,  'rate': 10},  # Approximate
    {'threshold': 389800,  'rate': 11},  # Approximate
    {'threshold': 526600,  'rate': 13},  # Approximate (13% on income above)
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
# Source: https://acheteur.ch/de/post/vermogenssteuer-zurich
# ============================================================================

# Wealth tax brackets for SINGLE individuals (Zurich)
WEALTH_TAX_BRACKETS_SINGLE = [
    {'threshold': 0,          'rate_per_thousand': 0},     # Tax-free
    {'threshold': 80000,      'rate_per_thousand': 0.5},   # 0.5‰
    {'threshold': 318000,     'rate_per_thousand': 1.0},   # 1.0‰
    {'threshold': 717000,     'rate_per_thousand': 1.5},   # 1.5‰
    {'threshold': 1673000,    'rate_per_thousand': 2.0},   # 2.0‰
    {'threshold': 2626000,    'rate_per_thousand': 2.5},   # 2.5‰
    {'threshold': 3579000,    'rate_per_thousand': 3.0},   # 3.0‰ (max)
]

# Wealth tax brackets for MARRIED couples (Zurich) - reduced tariff
WEALTH_TAX_BRACKETS_MARRIED = [
    {'threshold': 0,          'rate_per_thousand': 0},     # Tax-free
    {'threshold': 159000,     'rate_per_thousand': 0.5},   # ~2× single threshold
    {'threshold': 636000,     'rate_per_thousand': 1.0},   # ~2× single threshold
    {'threshold': 1434000,    'rate_per_thousand': 1.5},
    {'threshold': 3346000,    'rate_per_thousand': 2.0},
    {'threshold': 5252000,    'rate_per_thousand': 2.5},
    {'threshold': 7158000,    'rate_per_thousand': 3.0},   # 3.0‰ (max)
]

# Wealth deductions
# Note: Zurich has NO per-adult deductions. Singles and married use different brackets.
# Only per-child deductions apply.
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
COMMUTING_PAUSCHAL = 700            # CHF 700 for bike commuters (Velo-Pauschalabzug)
COMMUTING_MAX_FEDERAL = 3200        # Max CHF 3,200 for federal tax (DBG)
COMMUTING_MAX_CANTONAL = 5000       # Max CHF 5,000 for cantonal tax (Staatssteuer)
MEAL_COSTS_WITH_SUBSIDY = 1600      # CHF 7.50/day × 220 days
MEAL_COSTS_WITHOUT_SUBSIDY = 3200   # CHF 15/day × 220 days
PROFESSIONAL_EXPENSES_RATE = 0.03   # 3% of net salary
PROFESSIONAL_EXPENSES_MAX = 4000    # Max CHF 4,000

# Nebenerwerb (side income) deduction
SIDE_INCOME_DEDUCTION_MIN = 800     # Minimum deduction
SIDE_INCOME_DEDUCTION_RATE = 0.20   # 20% of side income
SIDE_INCOME_DEDUCTION_MAX = 2400    # Maximum deduction

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
