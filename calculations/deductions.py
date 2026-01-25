"""
Tax Deduction Calculations
Automatic and optional deductions based on user profile and inputs
"""
from models.tax_data import UserProfile, DeductionResult
from models.constants import (
    COMMUTING_PAUSCHAL,
    COMMUTING_MAX_FEDERAL,
    COMMUTING_MAX_CANTONAL,
    MEAL_COSTS_WITH_SUBSIDY,
    MEAL_COSTS_WITHOUT_SUBSIDY,
    PROFESSIONAL_EXPENSES_RATE,
    PROFESSIONAL_EXPENSES_MAX,
    SIDE_INCOME_DEDUCTION_MIN,
    SIDE_INCOME_DEDUCTION_RATE,
    SIDE_INCOME_DEDUCTION_MAX,
    CHILD_DEDUCTION_ZH,
    PROPERTY_MAINTENANCE_PAUSCHAL,
    ASSET_MANAGEMENT_RATE,
    ASSET_MANAGEMENT_MAX,
    INSURANCE_LIMITS_ZH,
    DUAL_INCOME_DEDUCTION_ZH,
    PILLAR_3A_MAX_EMPLOYED,
    PILLAR_3A_MAX_SELF_EMPLOYED,
    CHILDCARE_MAX,
    DEBT_INTEREST_MAX,
    DONATIONS_MAX_RATE,
    POLITICAL_CONTRIB_MAX_SINGLE,
    POLITICAL_CONTRIB_MAX_MARRIED,
    MEDICAL_COSTS_DEDUCTIBLE_RATE
)


def calculate_automatic_deductions(profile: UserProfile) -> DeductionResult:
    """
    Calculate automatic deductions based on user profile.
    These are deductions that don't require receipts (pauschal).

    For married couples, calculates employment deductions per spouse separately and sums them.

    Args:
        profile: User profile with all personal information

    Returns:
        DeductionResult with automatic deductions filled in
    """
    result = DeductionResult()

    if profile.marital_status == 'married':
        # === MARRIED COUPLES: Calculate per-spouse deductions ===

        # === SPOUSE 1 DEDUCTIONS ===

        # Commuting (spouse 1)
        commuting1 = 0.0
        if profile.spouse1_employment_type in ['employed', 'both']:
            if profile.spouse1_bikes_to_work:
                commuting1 += COMMUTING_PAUSCHAL  # CHF 700 biking deduction
            if profile.spouse1_uses_public_transport_car:
                commuting1 += profile.spouse1_actual_commuting_costs

        # Meals (spouse 1)
        meals1 = 0.0
        if profile.spouse1_employment_type in ['employed', 'both'] and profile.spouse1_works_away_from_home:
            if profile.spouse1_employer_meal_subsidy:
                meals1 = MEAL_COSTS_WITH_SUBSIDY
            else:
                meals1 = MEAL_COSTS_WITHOUT_SUBSIDY

        # Professional expenses (spouse 1)
        professional1 = 0.0
        if profile.spouse1_employment_type in ['employed', 'both'] and profile.spouse1_net_salary > 0:
            professional1 = min(
                profile.spouse1_net_salary * PROFESSIONAL_EXPENSES_RATE,
                PROFESSIONAL_EXPENSES_MAX
            )

        # Side income deduction (spouse 1)
        side_income1 = 0.0
        if profile.spouse1_has_side_income and profile.spouse1_side_income_amount > 0:
            calculated = profile.spouse1_side_income_amount * SIDE_INCOME_DEDUCTION_RATE
            side_income1 = max(SIDE_INCOME_DEDUCTION_MIN, min(calculated, SIDE_INCOME_DEDUCTION_MAX))

        # === SPOUSE 2 DEDUCTIONS ===

        # Commuting (spouse 2)
        commuting2 = 0.0
        if profile.spouse2_employment_type in ['employed', 'both']:
            if profile.spouse2_bikes_to_work:
                commuting2 += COMMUTING_PAUSCHAL
            if profile.spouse2_uses_public_transport_car:
                commuting2 += profile.spouse2_actual_commuting_costs

        # Meals (spouse 2)
        meals2 = 0.0
        if profile.spouse2_employment_type in ['employed', 'both'] and profile.spouse2_works_away_from_home:
            if profile.spouse2_employer_meal_subsidy:
                meals2 = MEAL_COSTS_WITH_SUBSIDY
            else:
                meals2 = MEAL_COSTS_WITHOUT_SUBSIDY

        # Professional expenses (spouse 2)
        professional2 = 0.0
        if profile.spouse2_employment_type in ['employed', 'both'] and profile.spouse2_net_salary > 0:
            professional2 = min(
                profile.spouse2_net_salary * PROFESSIONAL_EXPENSES_RATE,
                PROFESSIONAL_EXPENSES_MAX
            )

        # Side income deduction (spouse 2)
        side_income2 = 0.0
        if profile.spouse2_has_side_income and profile.spouse2_side_income_amount > 0:
            calculated = profile.spouse2_side_income_amount * SIDE_INCOME_DEDUCTION_RATE
            side_income2 = max(SIDE_INCOME_DEDUCTION_MIN, min(calculated, SIDE_INCOME_DEDUCTION_MAX))

        # === COMBINE SPOUSE DEDUCTIONS ===
        result.commuting_pauschal = commuting1 + commuting2
        result.meal_costs_pauschal = meals1 + meals2
        result.professional_expenses = professional1 + professional2
        result.side_income_deduction = side_income1 + side_income2

        # Dual income deduction (both must work)
        both_work = (
            profile.spouse1_employment_type in ['employed', 'self_employed', 'both'] and
            profile.spouse2_employment_type in ['employed', 'self_employed', 'both']
        )
        if both_work:
            result.dual_income_deduction = DUAL_INCOME_DEDUCTION_ZH

    else:
        # === SINGLE PERSON: Use existing logic (backward compatible) ===

        # Commuting (if employed and commutes)
        if profile.employment_type in ['employed', 'both']:
            commuting_total = 0.0

            # Bike commuting: CHF 700 pauschal (no receipts)
            if profile.bikes_to_work:
                commuting_total += COMMUTING_PAUSCHAL

            # Public transport/car: actual costs (with receipts)
            if profile.uses_public_transport_car:
                commuting_total += profile.actual_commuting_costs

            result.commuting_pauschal = commuting_total

        # Meals (if employed and works away from home)
        if profile.employment_type in ['employed', 'both'] and profile.works_away_from_home:
            if profile.employer_meal_subsidy:
                result.meal_costs_pauschal = MEAL_COSTS_WITH_SUBSIDY
            else:
                result.meal_costs_pauschal = MEAL_COSTS_WITHOUT_SUBSIDY

        # Professional expenses (3% of net salary, max CHF 4,000)
        if profile.employment_type in ['employed', 'both'] and profile.net_salary > 0:
            if profile.claim_actual_professional:
                result.professional_expenses = profile.actual_professional_costs
            else:
                result.professional_expenses = min(
                    profile.net_salary * PROFESSIONAL_EXPENSES_RATE,
                    PROFESSIONAL_EXPENSES_MAX
                )

        # Side income deduction (Nebenerwerb)
        # Formula: max(800, min(0.20 × side_income, 2400))
        if profile.has_side_income and profile.side_income_amount > 0:
            calculated_deduction = profile.side_income_amount * SIDE_INCOME_DEDUCTION_RATE
            result.side_income_deduction = max(
                SIDE_INCOME_DEDUCTION_MIN,
                min(calculated_deduction, SIDE_INCOME_DEDUCTION_MAX)
            )

    # === COMMON DEDUCTIONS (SAME FOR BOTH SINGLE AND MARRIED) ===

    # Child deductions (CHF 9,000 per child in ZH)
    result.child_deductions = profile.num_children * CHILD_DEDUCTION_ZH

    # Property maintenance (20% pauschal in ZH)
    if profile.owns_property and profile.eigenmietwert:
        if profile.claim_actual_property_maintenance:
            result.property_maintenance = profile.actual_property_maintenance_costs
        else:
            result.property_maintenance = profile.eigenmietwert * PROPERTY_MAINTENANCE_PAUSCHAL

    # Asset management (3‰ pauschal in ZH, max CHF 6,000)
    if profile.has_securities and profile.securities_value:
        asset_mgmt = profile.securities_value * ASSET_MANAGEMENT_RATE
        result.asset_management = min(asset_mgmt, ASSET_MANAGEMENT_MAX)

    # Calculate total automatic
    result.calculate_totals()

    return result


def calculate_insurance_premium_limit(profile: UserProfile) -> float:
    """
    Calculate insurance premium deduction limit based on marital status and pension situation.

    Args:
        profile: User profile

    Returns:
        Maximum deductible insurance premium amount
    """
    # Determine if person has pension (Pillar 2)
    # For simplicity, assume employed/self-employed have pension, others don't
    has_pension = profile.employment_type in ['employed', 'self_employed', 'both']

    if profile.marital_status == 'married':
        if has_pension:
            base_limit = INSURANCE_LIMITS_ZH['married_with_pension']
        else:
            base_limit = INSURANCE_LIMITS_ZH['married_without_pension']
    else:
        if has_pension:
            base_limit = INSURANCE_LIMITS_ZH['single_with_pension']
        else:
            base_limit = INSURANCE_LIMITS_ZH['single_without_pension']

    # Add per-child limit
    child_limit = profile.num_children * INSURANCE_LIMITS_ZH['per_child']

    return base_limit + child_limit


def validate_pillar_3a(amount: float, profile: UserProfile, employment_type: str = None) -> dict:
    """
    Validate Pillar 3a contribution amount.

    Args:
        amount: Pillar 3a contribution
        profile: User profile
        employment_type: Optional override for employment type (for married couples).
                        If provided, uses this instead of profile.employment_type.

    Returns:
        Dictionary with validation result and max limit
    """
    # Use provided employment_type or fall back to profile.employment_type
    emp_type = employment_type if employment_type is not None else profile.employment_type

    if emp_type == 'self_employed':
        max_limit = PILLAR_3A_MAX_SELF_EMPLOYED
    else:
        max_limit = PILLAR_3A_MAX_EMPLOYED

    is_valid = amount <= max_limit
    remaining = max_limit - amount if amount <= max_limit else 0

    return {
        'is_valid': is_valid,
        'max_limit': max_limit,
        'remaining': remaining,
        'amount': min(amount, max_limit)  # Cap at maximum
    }


def validate_childcare_costs(amount: float, profile: UserProfile) -> dict:
    """
    Validate childcare cost deduction.

    Args:
        amount: Childcare costs
        profile: User profile

    Returns:
        Dictionary with validation result
    """
    # Childcare only applies if both parents work (or single parent works)
    # and children under 14
    eligible = False
    reason = ""

    if profile.marital_status == 'married':
        if not profile.both_spouses_work:
            reason = "Both spouses must be working for childcare deduction"
        elif profile.num_children == 0:
            reason = "No children for childcare deduction"
        else:
            # Check if any children under 14
            has_young_children = any(age < 14 for age in profile.children_ages) if profile.children_ages else True
            if has_young_children:
                eligible = True
            else:
                reason = "Children must be under 14 for childcare deduction"
    else:
        # Single parent working
        if profile.employment_type in ['employed', 'self_employed', 'both']:
            if profile.num_children > 0:
                has_young_children = any(age < 14 for age in profile.children_ages) if profile.children_ages else True
                if has_young_children:
                    eligible = True
                else:
                    reason = "Children must be under 14 for childcare deduction"
            else:
                reason = "No children for childcare deduction"
        else:
            reason = "Must be working for childcare deduction"

    is_valid = amount <= CHILDCARE_MAX
    deductible_amount = min(amount, CHILDCARE_MAX) if eligible else 0

    return {
        'eligible': eligible,
        'is_valid': is_valid,
        'max_limit': CHILDCARE_MAX,
        'deductible_amount': deductible_amount,
        'reason': reason if not eligible else ""
    }


def validate_medical_costs(total_medical: float, income: float) -> dict:
    """
    Validate medical cost deduction (5% threshold in Zurich).

    Args:
        total_medical: Total medical costs
        income: Gross income

    Returns:
        Dictionary with deductible amount
    """
    threshold = income * MEDICAL_COSTS_DEDUCTIBLE_RATE
    deductible = max(0, total_medical - threshold)

    return {
        'total_medical': total_medical,
        'threshold': threshold,
        'deductible': deductible,
        'below_threshold': total_medical < threshold
    }


def validate_donations(amount: float, income: float) -> dict:
    """
    Validate donation deduction (max 20% of income).

    Args:
        amount: Donation amount
        income: Gross income

    Returns:
        Dictionary with validation result
    """
    max_limit = income * DONATIONS_MAX_RATE
    is_valid = amount <= max_limit
    deductible = min(amount, max_limit)

    return {
        'is_valid': is_valid,
        'max_limit': max_limit,
        'deductible': deductible
    }


def validate_political_contributions(amount: float, profile: UserProfile) -> dict:
    """
    Validate political party contribution deduction.

    Args:
        amount: Contribution amount
        profile: User profile

    Returns:
        Dictionary with validation result
    """
    if profile.marital_status == 'married':
        max_limit = POLITICAL_CONTRIB_MAX_MARRIED
    else:
        max_limit = POLITICAL_CONTRIB_MAX_SINGLE

    is_valid = amount <= max_limit
    deductible = min(amount, max_limit)

    return {
        'is_valid': is_valid,
        'max_limit': max_limit,
        'deductible': deductible
    }


def validate_debt_interest(amount: float, investment_income: float = 0) -> dict:
    """
    Validate debt interest deduction (max CHF 50,000 + investment income).

    Args:
        amount: Debt interest amount
        investment_income: Investment income (dividends, interest, etc.)

    Returns:
        Dictionary with validation result
    """
    max_limit = DEBT_INTEREST_MAX + investment_income
    is_valid = amount <= max_limit
    deductible = min(amount, max_limit)

    return {
        'is_valid': is_valid,
        'max_limit': max_limit,
        'deductible': deductible
    }


def get_adjusted_deductions_for_tax_type(deductions: DeductionResult, tax_type: str,
                                         total_to_adjust: float = None) -> float:
    """
    Calculate total deductions with appropriate commuting cost caps for federal vs cantonal tax.

    Swiss tax law has different limits for commuting costs:
    - Federal tax (DBG): Max CHF 3,200
    - Cantonal tax (Staatssteuer): Max CHF 5,000

    Args:
        deductions: DeductionResult with all deductions
        tax_type: 'federal' or 'cantonal'
        total_to_adjust: Optional total deductions to adjust (if not provided, uses deductions.total_deductions)

    Returns:
        Total deductions with appropriate commuting cost cap applied
    """
    # Use provided total or fall back to total_deductions
    total = total_to_adjust if total_to_adjust is not None else deductions.total_deductions

    # Get the raw commuting cost (before any caps)
    raw_commuting = deductions.commuting_pauschal

    # Apply the appropriate cap based on tax type
    if tax_type == 'federal':
        capped_commuting = min(raw_commuting, COMMUTING_MAX_FEDERAL)
    elif tax_type == 'cantonal':
        capped_commuting = min(raw_commuting, COMMUTING_MAX_CANTONAL)
    else:
        raise ValueError(f"Invalid tax_type: {tax_type}. Must be 'federal' or 'cantonal'")

    # Adjust total: remove raw commuting, add capped commuting
    adjusted_total = total - raw_commuting + capped_commuting

    return adjusted_total
