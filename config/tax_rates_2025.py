"""
Swiss Tax Rates for 2025

Federal and Zürich cantonal progressive tax rate tables.
Based on official Swiss federal tax law and Zürich cantonal regulations.
"""

# Federal tax rates for single taxpayers (Grundtarif) - 2025
# Structure: {'threshold': income_threshold, 'rate': marginal_rate, 'base_tax': cumulative_tax_at_threshold}

FEDERAL_TAX_RATES_SINGLE = [
    {'threshold': 0, 'rate': 0.0000, 'base_tax': 0},
    {'threshold': 14000, 'rate': 0.0077, 'base_tax': 0},  # Personal allowance threshold
    {'threshold': 18200, 'rate': 0.0088, 'base_tax': 32.34},
    {'threshold': 20800, 'rate': 0.0099, 'base_tax': 55.22},
    {'threshold': 27100, 'rate': 0.0110, 'base_tax': 117.59},
    {'threshold': 33400, 'rate': 0.0121, 'base_tax': 186.89},
    {'threshold': 39700, 'rate': 0.0132, 'base_tax': 263.12},
    {'threshold': 46000, 'rate': 0.0143, 'base_tax': 346.28},
    {'threshold': 57800, 'rate': 0.0165, 'base_tax': 515.02},
    {'threshold': 75300, 'rate': 0.0209, 'base_tax': 803.77},
    {'threshold': 90300, 'rate': 0.0253, 'base_tax': 1117.77},
    {'threshold': 105400, 'rate': 0.0297, 'base_tax': 1499.30},
    {'threshold': 131100, 'rate': 0.0341, 'base_tax': 2262.60},
    {'threshold': 156900, 'rate': 0.0385, 'base_tax': 3142.38},
    {'threshold': 182700, 'rate': 0.0429, 'base_tax': 4136.68},
    {'threshold': 208500, 'rate': 0.0473, 'base_tax': 5245.50},
    {'threshold': 234300, 'rate': 0.0517, 'base_tax': 6468.84},
    {'threshold': 260100, 'rate': 0.0561, 'base_tax': 7806.70},
    {'threshold': 285900, 'rate': 0.0594, 'base_tax': 9259.08},
    {'threshold': 312200, 'rate': 0.0627, 'base_tax': 10822.70},
    {'threshold': 338500, 'rate': 0.0660, 'base_tax': 12471.51},
    {'threshold': 364800, 'rate': 0.0693, 'base_tax': 14207.31},
    {'threshold': 391100, 'rate': 0.0726, 'base_tax': 16030.10},
    {'threshold': 417400, 'rate': 0.0759, 'base_tax': 17939.88},
    {'threshold': 443700, 'rate': 0.0792, 'base_tax': 19936.65},
    {'threshold': 679100, 'rate': 0.0825, 'base_tax': 38584.93},
    {'threshold': 895900, 'rate': 0.1100, 'base_tax': 56471.93},
    {'threshold': 1000000, 'rate': 0.1150, 'base_tax': 67922.93}  # Cap at 11.5%
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
