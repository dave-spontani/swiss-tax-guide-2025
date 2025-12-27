"""
Municipality data for Swiss cantons

Contains municipal tax multipliers (Steuerfuss) for different municipalities.
The multiplier is applied to the cantonal tax to calculate municipal tax.

Municipal Tax = Cantonal Base Tax × Municipal Multiplier
"""

# ============================================================================
# ZÜRICH CANTON MUNICIPALITIES
# ============================================================================

ZURICH_MUNICIPALITIES = {
    'Zürich': {
        'multiplier': 1.19,  # 119%
        'name_de': 'Zürich',
        'name_en': 'Zurich City',
        'population': 434000,
        'notes': 'Largest city, higher taxes but comprehensive services'
    },
    'Winterthur': {
        'multiplier': 1.25,
        'name_de': 'Winterthur',
        'name_en': 'Winterthur',
        'population': 115000,
        'notes': 'Second largest city in canton'
    },
    'Uster': {
        'multiplier': 1.09,
        'name_de': 'Uster',
        'name_en': 'Uster',
        'population': 35000
    },
    'Dübendorf': {
        'multiplier': 1.06,
        'name_de': 'Dübendorf',
        'name_en': 'Dübendorf',
        'population': 29000
    },
    'Dietikon': {
        'multiplier': 1.13,
        'name_de': 'Dietikon',
        'name_en': 'Dietikon',
        'population': 27000
    },
    'Wetzikon': {
        'multiplier': 1.07,
        'name_de': 'Wetzikon',
        'name_en': 'Wetzikon',
        'population': 25000
    },
    'Kilchberg': {
        'multiplier': 0.80,
        'name_de': 'Kilchberg',
        'name_en': 'Kilchberg',
        'population': 8000,
        'notes': 'One of lowest tax municipalities'
    },
    'Herrliberg': {
        'multiplier': 0.72,
        'name_de': 'Herrliberg',
        'name_en': 'Herrliberg',
        'population': 6000,
        'notes': 'Very low tax municipality'
    },
    'Meilen': {
        'multiplier': 0.85,
        'name_de': 'Meilen',
        'name_en': 'Meilen',
        'population': 14000
    },
    'Zollikon': {
        'multiplier': 0.84,
        'name_de': 'Zollikon',
        'name_en': 'Zollikon',
        'population': 13000,
        'notes': 'Affluent lakeside municipality'
    }
}

# Default municipality
DEFAULT_MUNICIPALITY = 'Zürich'

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_municipality_multiplier(municipality_name: str, canton: str = 'ZH') -> float:
    """
    Get municipal tax multiplier for a given municipality

    Args:
        municipality_name: Name of the municipality
        canton: Canton code (currently only 'ZH' supported)

    Returns:
        Municipal tax multiplier (e.g., 1.19 for Zürich City)
    """
    if canton == 'ZH':
        municipality = ZURICH_MUNICIPALITIES.get(municipality_name)
        if municipality:
            return municipality['multiplier']
        # Default to Zürich if not found
        return ZURICH_MUNICIPALITIES[DEFAULT_MUNICIPALITY]['multiplier']

    # Default multiplier if canton not supported
    return 1.0


def get_all_zh_municipalities():
    """Get list of all Zürich municipalities with their data"""
    return ZURICH_MUNICIPALITIES


def get_municipality_names(canton: str = 'ZH'):
    """Get list of municipality names for a canton"""
    if canton == 'ZH':
        return list(ZURICH_MUNICIPALITIES.keys())
    return []


def get_municipality_info(municipality_name: str, canton: str = 'ZH'):
    """Get full information about a municipality"""
    if canton == 'ZH':
        return ZURICH_MUNICIPALITIES.get(municipality_name)
    return None
