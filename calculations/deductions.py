"""
Tax Deduction Calculations
Automatic and optional deductions based on user profile and inputs
"""
from models.tax_data import UserProfile, DeductionResult
from models.constants import (
    COMMUTING_PAUSCHAL,
    MEAL_COSTS_WITH_SUBSIDY,
    MEAL_COSTS_WITHOUT_SUBSIDY,
    PROFESSIONAL_EXPENSES_RATE,
    PROFESSIONAL_EXPENSES_MAX,
    SIDE_INCOME_DEDUCTION,
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

    Args:
        profile: User profile with all personal information

    Returns:
        DeductionResult with automatic deductions filled in
    """
    result = DeductionResult()

    # Commuting (if employed and commutes)
    if profile.employment_type in ['employed', 'both'] and profile.commutes_to_work:
        if profile.claim_actual_commuting:
            result.commuting_pauschal = profile.actual_commuting_costs
        else:
            result.commuting_pauschal = COMMUTING_PAUSCHAL

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

    # Side income deduction
    if profile.has_side_income:
        result.side_income_deduction = SIDE_INCOME_DEDUCTION

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

    # Dual income (if married and both work)
    if profile.marital_status == 'married' and profile.both_spouses_work:
        result.dual_income_deduction = DUAL_INCOME_DEDUCTION_ZH

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


def validate_pillar_3a(amount: float, profile: UserProfile) -> dict:
    """
    Validate Pillar 3a contribution amount.

    Args:
        amount: Pillar 3a contribution
        profile: User profile

    Returns:
        Dictionary with validation result and max limit
    """
    if profile.employment_type == 'self_employed':
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
