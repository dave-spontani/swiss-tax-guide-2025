"""
Deduction limits and thresholds for Swiss taxes - 2025

Based on SchmittTreuhand_Steuertipps_web3.pdf and Swiss tax law.
All amounts in CHF.
"""

# ============================================================================
# DEDUCTION LIMITS 2025
# ============================================================================

DEDUCTION_LIMITS_2025 = {

    # ------------------------------------------------------------------------
    # COMMUTING COSTS (Arbeitswegkosten)
    # ------------------------------------------------------------------------
    'commuting': {
        'federal_max': 3000,  # Federal maximum
        'zh_cantonal_max': 5000,  # Zürich canton maximum
        'public_transport_unlimited': True,  # 2nd class costs fully deductible up to max
        'bicycle_pauschal': 700,  # Pauschal for bicycle/small motorcycle
        'car_rate_per_km': 0.70,  # CHF per km for car (requires justification)
        'motorcycle_rate_per_km': 0.40,  # CHF per km for motorcycle
        'proof_required': {
            'public_transport': True,  # Receipts/GA proof needed
            'bicycle': False,  # Pauschal, no proof
            'car': True  # Employer confirmation required
        }
    },

    # ------------------------------------------------------------------------
    # MEAL EXPENSES (Mehrkosten auswärtige Verpflegung)
    # ------------------------------------------------------------------------
    'meals': {
        'with_subsidy': 1600,  # With canteen/employer subsidy
        'without_subsidy': 3200,  # Without subsidy
        'per_day_with_subsidy': 7.50,  # Daily rate with subsidy
        'per_day_without_subsidy': 15,  # Daily rate without subsidy
        'proof_required': False,  # Pauschal deduction
        'work_days_per_year': 220  # Standard full-time
    },

    # ------------------------------------------------------------------------
    # PROFESSIONAL EXPENSES (Übrige Berufsauslagen)
    # ------------------------------------------------------------------------
    'professional_expenses': {
        'minimum': 2000,  # Minimum pauschal
        'maximum': 4000,  # Maximum pauschal
        'rate': 0.03,  # 3% of net salary
        'proof_required': False,  # Pauschal deduction
        'includes': [
            'Professional tools',
            'Computer hardware/software',
            'Professional literature',
            'Work clothes',
            'Professional association memberships',
            'Home office (if included in pauschal)'
        ]
    },

    # ------------------------------------------------------------------------
    # INSURANCE PREMIUMS (Versicherungsprämien)
    # ------------------------------------------------------------------------
    'insurance': {
        'single_with_pillar2': {
            'federal': 1700,
            'zh_cantonal': 3000  # Lower end of ZH range
        },
        'single_without_pillar2': {
            'federal': 2550,
            'zh_cantonal': 4400
        },
        'married_with_pillar2': {
            'federal': 3500,
            'zh_cantonal': 5600
        },
        'married_without_pillar2': {
            'federal': 5250,
            'zh_cantonal': 8700
        },
        'per_child_federal': 700,
        'per_child_zh': 1300,
        'includes': [
            'Health insurance (KVG)',
            'Accident insurance',
            'Life insurance (Säule 3b)',
            'Savings interest'
        ],
        'must_subtract_premium_subsidies': True
    },

    # ------------------------------------------------------------------------
    # PILLAR 3A (Säule 3a)
    # ------------------------------------------------------------------------
    'pillar_3a': {
        'with_pillar2': 7258,  # 2025 limit for those with Pillar 2
        'without_pillar2_max': 36288,  # 2025 limit for those without Pillar 2
        'without_pillar2_rate': 0.20,  # 20% of net income
        'proof_required': True,  # Official contribution certificate required
        'requires_ahv_income': True  # Must have AHV-liable income
    },

    # ------------------------------------------------------------------------
    # PILLAR 2 BUY-IN (Einkauf in zweite Säule)
    # ------------------------------------------------------------------------
    'pillar_2_buyback': {
        'max_amount': None,  # Unlimited if pension gap exists
        'proof_required': True,  # Pension fund certificate required
        'capital_withdrawal_lockup_years': 3,  # Cannot withdraw capital for 3 years
        'notes': 'Must repay WEF withdrawals before buy-in allowed'
    },

    # ------------------------------------------------------------------------
    # FURTHER EDUCATION (Weiterbildungskosten)
    # ------------------------------------------------------------------------
    'education': {
        'maximum': 12000,  # Federal and cantonal max
        'minimum_age': 20,  # Must be 20+ years old
        'requires_secondary_education': True,  # Must have completed secondary education
        'zh_pauschal_no_proof': 500,  # Zürich allows CHF 500 without proof
        'proof_required': True,  # Above CHF 500 in ZH
        'excludes': [
            'Hobby courses',
            'Leisure courses',
            'Sports courses',
            'Wellness courses',
            'Driving lessons',
            'First aid courses (unless job-required)'
        ]
    },

    # ------------------------------------------------------------------------
    # CHARITABLE DONATIONS (Freiwillige Zuwendungen)
    # ------------------------------------------------------------------------
    'charitable': {
        'minimum': 100,  # Minimum donation to deduct
        'maximum_rate': 0.20,  # Max 20% of net income
        'proof_required': True,  # Donation receipts required
        'organization_requirements': 'Must be Swiss tax-exempt organization',
        'excludes': [
            'Cultural associations',
            'Sports clubs',
            'Political parties (separate category)'
        ]
    },

    # ------------------------------------------------------------------------
    # POLITICAL PARTY DONATIONS (Beitrag an politische Parteien)
    # ------------------------------------------------------------------------
    'political_donations': {
        'federal_max': 10100,
        'zh_max': 10000,
        'proof_required': True,
        'party_requirements': 'Party must be registered in official party register'
    },

    # ------------------------------------------------------------------------
    # MEDICAL EXPENSES (Krankheitskosten)
    # ------------------------------------------------------------------------
    'medical': {
        'threshold_rate': 0.05,  # Must exceed 5% of net income
        'zh_threshold_rate': 0.05,  # Zürich also 5%
        'includes': [
            'Health insurance franchise',
            'Health insurance deductible',
            'Non-KVG covered therapies (with medical prescription)',
            'Dental treatments (medical)'
        ],
        'excludes': [
            'Preventive measures',
            'Cosmetic treatments',
            'Wellness treatments'
        ],
        'proof_required': True
    },

    # ------------------------------------------------------------------------
    # SUPPORT PAYMENTS (Unterstützungsabzug)
    # ------------------------------------------------------------------------
    'support_payments': {
        'federal_min': 6500,
        'zh_min': 2700,
        'requirements': [
            'Recipient must have health/financial difficulties',
            'Cannot be spouse or children',
            'Must provide bank transfer proof',
            'May need medical certificate',
            'Must prove financial need'
        ],
        'notes': 'Very high hurdles - restrictive application'
    }
}

# ============================================================================
# SOCIAL SECURITY RATES 2025
# ============================================================================

SOCIAL_SECURITY_RATES = {
    'ahv_iv_eo': {
        'rate': 0.053,  # 5.3% employee portion (10.6% total with employer)
        'description': 'Old age, disability, loss of income insurance',
        'max_income': None  # No ceiling
    },
    'alv': {
        'rate': 0.011,  # 1.1% unemployment insurance (2.2% total)
        'max_income': 148200,  # 2025 ceiling
        'additional_rate_above_ceiling': 0.005  # Additional 0.5% above ceiling
    },
    'nbu': {
        'rate': 0.007,  # ~0.7% non-occupational accident (varies by employer)
        'description': 'Non-occupational accident insurance',
        'max_income': None,
        'notes': 'Rate varies by employer and risk category'
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_max_commuting_deduction(canton='ZH', transport_type='public'):
    """Get maximum commuting deduction"""
    if canton == 'ZH':
        return DEDUCTION_LIMITS_2025['commuting']['zh_cantonal_max']
    return DEDUCTION_LIMITS_2025['commuting']['federal_max']


def get_max_insurance_deduction(civil_status='single', has_pillar2=True, num_children=0, level='federal'):
    """Get maximum insurance premium deduction"""
    key = f"{'single' if civil_status == 'single' else 'married'}_{'with' if has_pillar2 else 'without'}_pillar2"
    base = DEDUCTION_LIMITS_2025['insurance'][key][level]

    child_addition = 0
    if num_children > 0:
        per_child = DEDUCTION_LIMITS_2025['insurance'][f'per_child_{level}']
        child_addition = num_children * per_child

    return base + child_addition


def get_pillar_3a_limit(has_pillar2=True, net_income=0):
    """Get maximum Pillar 3a contribution limit"""
    if has_pillar2:
        return DEDUCTION_LIMITS_2025['pillar_3a']['with_pillar2']
    else:
        # 20% of net income, max CHF 36,288
        max_without = DEDUCTION_LIMITS_2025['pillar_3a']['without_pillar2_max']
        calculated = net_income * DEDUCTION_LIMITS_2025['pillar_3a']['without_pillar2_rate']
        return min(calculated, max_without)
