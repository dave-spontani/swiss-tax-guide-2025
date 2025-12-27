"""
Swiss Tax Rates for 2025

Federal and Zürich cantonal progressive tax rate tables.
Based on official Swiss federal tax law and Zürich cantonal regulations.
"""

# Federal tax rates for single taxpayers (Grundtarif) - 2025
# Structure: {'threshold': income_threshold, 'rate': marginal_rate, 'base_tax': cumulative_tax_at_threshold}
# Source: Article 36 DBG (Bundesgesetz über die direkte Bundessteuer)
# Verified against: https://lawbrary.ch/law/art/DBG-v2022.01-de-art-36/
# Tax amounts under CHF 25 are not levied

FEDERAL_TAX_RATES_SINGLE = [
    {'threshold': 0, 'rate': 0.0000, 'base_tax': 0.00},
    {'threshold': 14500, 'rate': 0.0077, 'base_tax': 0.00},       # 0.77 CHF per 100 CHF
    {'threshold': 31600, 'rate': 0.0088, 'base_tax': 131.67},     # 0.88 CHF per 100 CHF
    {'threshold': 41400, 'rate': 0.0264, 'base_tax': 217.91},     # 2.64 CHF per 100 CHF
    {'threshold': 55200, 'rate': 0.0297, 'base_tax': 582.23},     # 2.97 CHF per 100 CHF
    {'threshold': 72500, 'rate': 0.0594, 'base_tax': 1096.04},    # 5.94 CHF per 100 CHF
    {'threshold': 78100, 'rate': 0.0660, 'base_tax': 1428.68},    # 6.60 CHF per 100 CHF
    {'threshold': 103600, 'rate': 0.0880, 'base_tax': 3111.68},   # 8.80 CHF per 100 CHF
    {'threshold': 134600, 'rate': 0.1100, 'base_tax': 5839.68},   # 11.00 CHF per 100 CHF
    {'threshold': 176000, 'rate': 0.1100, 'base_tax': 10393.68},  # 11.00 CHF per 100 CHF (unchanged)
    {'threshold': 755200, 'rate': 0.1320, 'base_tax': 74105.68},  # 13.20 CHF per 100 CHF
    {'threshold': 1000000, 'rate': 0.1150, 'base_tax': 106437.04} # 11.50 CHF per 100 CHF (maximum rate)
]

# Zürich cantonal base tax rates (before multipliers)
# These rates are applied to taxable income and then multiplied by canton and municipal multipliers

ZH_CANTONAL_BASE_RATES_SINGLE = [
    {'threshold': 0, 'rate': 0.0200, 'base_tax': 0},
    {'threshold': 6700, 'rate': 0.0200, 'base_tax': 0},  # Personal allowance
    {'threshold': 13400, 'rate': 0.0220, 'base_tax': 134.00},
    {'threshold': 19500, 'rate': 0.0240, 'base_tax': 268.20},
    {'threshold': 26800, 'rate': 0.0260, 'base_tax': 443.40},
    {'threshold': 36700, 'rate': 0.0280, 'base_tax': 700.80},
    {'threshold': 47800, 'rate': 0.0300, 'base_tax': 1011.60},
    {'threshold': 60200, 'rate': 0.0320, 'base_tax': 1383.60},
    {'threshold': 73900, 'rate': 0.0340, 'base_tax': 1822.00},
    {'threshold': 89200, 'rate': 0.0360, 'base_tax': 2342.20},
    {'threshold': 106300, 'rate': 0.0380, 'base_tax': 2957.80},
    {'threshold': 125000, 'rate': 0.0400, 'base_tax': 3668.40},
    {'threshold': 145900, 'rate': 0.0420, 'base_tax': 4504.40},
    {'threshold': 169500, 'rate': 0.0440, 'base_tax': 5495.60},
    {'threshold': 196000, 'rate': 0.0460, 'base_tax': 6661.60},
    {'threshold': 226000, 'rate': 0.0480, 'base_tax': 8041.60},
    {'threshold': 260100, 'rate': 0.0500, 'base_tax': 9678.40},
    {'threshold': 299500, 'rate': 0.0520, 'base_tax': 11648.40},
    {'threshold': 345800, 'rate': 0.0540, 'base_tax': 14055.60},
    {'threshold': 400000, 'rate': 0.0560, 'base_tax': 16982.40},
    {'threshold': 463700, 'rate': 0.0580, 'base_tax': 20549.60},
    {'threshold': 538800, 'rate': 0.0600, 'base_tax': 24905.20},
    {'threshold': 627500, 'rate': 0.0620, 'base_tax': 30227.40},
    {'threshold': 732000, 'rate': 0.0640, 'base_tax': 36706.40},
    {'threshold': 855100, 'rate': 0.0660, 'base_tax': 44584.80},
    {'threshold': 1000000, 'rate': 0.0680, 'base_tax': 54141.20},
    {'threshold': 1200000, 'rate': 0.0700, 'base_tax': 67741.20}
]

# Cantonal multiplier for Zürich
ZH_CANTONAL_MULTIPLIER = 0.98  # Applied to base cantonal tax

def get_federal_tax_rates():
    """Get federal tax rate table for single taxpayers"""
    return FEDERAL_TAX_RATES_SINGLE

def get_zh_cantonal_rates():
    """Get Zürich cantonal base tax rates"""
    return ZH_CANTONAL_BASE_RATES_SINGLE

def get_zh_cantonal_multiplier():
    """Get Zürich cantonal multiplier"""
    return ZH_CANTONAL_MULTIPLIER
