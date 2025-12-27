"""
Deduction Validator Service

Validates and calculates deductions based on user inputs and profile.
Handles automatic/pauschal deductions and proof-required deductions.
"""

from typing import List, Tuple
from models.user_profile import UserProfile
from models.deduction import Deduction, DeductionCategory, ProofRequirement
from config.deduction_limits import (
    DEDUCTION_LIMITS_2025,
    get_max_commuting_deduction,
    get_max_insurance_deduction,
    get_pillar_3a_limit
)


class DeductionValidator:
    """
    Validates and calculates deductions based on user inputs and profile
    """

    def __init__(self, tax_year: int = 2025):
        self.tax_year = tax_year
        self.limits = DEDUCTION_LIMITS_2025

    def calculate_professional_expenses(self, net_salary: float) -> Deduction:
        """
        Calculate professional expenses pauschal deduction

        This is automatic and requires no proof. Includes tools, software,
        professional literature, work clothes, etc.

        Args:
            net_salary: Net salary after social security deductions

        Returns:
            Deduction for professional expenses
        """
        # 3% of net salary, minimum CHF 2,000, maximum CHF 4,000
        amount = net_salary * self.limits['professional_expenses']['rate']
        amount = max(self.limits['professional_expenses']['minimum'], amount)
        amount = min(self.limits['professional_expenses']['maximum'], amount)

        return Deduction(
            category=DeductionCategory.PROFESSIONAL,
            amount=amount,
            description=f"Professional expenses (pauschal: 3% of salary, min CHF 2,000, max CHF 4,000)",
            is_automatic=True,
            notes="No proof required. Includes: tools, software, literature, work clothes, "
                  "professional memberships, home office (if not claimed separately)"
        )

    def calculate_meal_expenses(self,
                                has_canteen_subsidy: bool,
                                employment_percentage: float = 100.0) -> Deduction:
        """
        Calculate meal expense pauschal deduction

        Args:
            has_canteen_subsidy: Whether employee has canteen or meal subsidy
            employment_percentage: Employment percentage (100 = full-time)

        Returns:
            Deduction for meal expenses
        """
        # Base amount depends on subsidy
        if has_canteen_subsidy:
            base_amount = self.limits['meals']['with_subsidy']
            daily_rate = self.limits['meals']['per_day_with_subsidy']
        else:
            base_amount = self.limits['meals']['without_subsidy']
            daily_rate = self.limits['meals']['per_day_without_subsidy']

        # Adjust for part-time employment
        amount = base_amount * (employment_percentage / 100)

        return Deduction(
            category=DeductionCategory.MEALS,
            amount=amount,
            description=f"Meal expenses (CHF {daily_rate}/day pauschal, "
                        f"{'with' if has_canteen_subsidy else 'without'} canteen subsidy)",
            is_automatic=True,
            notes=f"No proof required. Based on {employment_percentage}% employment. "
                  f"Assumes you cannot eat lunch at home."
        )

    def calculate_commuting_deduction(self,
                                     transport_type: str,
                                     annual_cost: float = 0,
                                     distance_km: float = 0,
                                     days_per_year: int = 220,
                                     canton: str = 'ZH') -> Deduction:
        """
        Calculate commuting cost deduction

        Args:
            transport_type: 'public_transport', 'bicycle', 'car', or 'motorcycle'
            annual_cost: Annual cost for public transport (e.g., GA subscription)
            distance_km: One-way distance in km (for car/motorcycle calculation)
            days_per_year: Working days per year
            canton: Canton code

        Returns:
            Deduction for commuting costs
        """
        if transport_type == "public_transport":
            # Full 2nd class costs deductible up to limits
            federal_max = self.limits['commuting']['federal_max']
            cantonal_max = get_max_commuting_deduction(canton, 'public')

            # Use cantonal limit (higher)
            actual_amount = min(annual_cost, cantonal_max)

            return Deduction(
                category=DeductionCategory.COMMUTING,
                amount=actual_amount,
                description=f"Public transport costs (2nd class): CHF {annual_cost:,.2f}/year",
                is_automatic=False,
                notes=f"Federal limit: CHF {federal_max:,.0f} | "
                      f"Zürich cantonal limit: CHF {cantonal_max:,.0f}. "
                      f"Requires receipts/GA subscription proof."
            )

        elif transport_type == "bicycle":
            # Pauschal CHF 700
            amount = self.limits['commuting']['bicycle_pauschal']

            return Deduction(
                category=DeductionCategory.COMMUTING,
                amount=amount,
                description="Bicycle/small motorcycle commuting (pauschal)",
                is_automatic=True,
                notes="No proof required - automatic pauschal deduction of CHF 700"
            )

        elif transport_type == "car":
            # CHF 0.70 per km, requires justification
            total_km = distance_km * 2 * days_per_year  # Round trip
            calculated_amount = total_km * self.limits['commuting']['car_rate_per_km']

            # Apply limits
            cantonal_max = get_max_commuting_deduction(canton, 'public')
            actual_amount = min(calculated_amount, cantonal_max)

            return Deduction(
                category=DeductionCategory.COMMUTING,
                amount=actual_amount,
                description=f"Car commuting: {distance_km} km × 2 × {days_per_year} days × CHF 0.70/km",
                is_automatic=False,
                notes="Requires employer confirmation or proof that public transport is not reasonable "
                      "(time savings > 1 hour, health reasons, or no public transport available). "
                      "Very strict application!"
            )

        return Deduction(
            category=DeductionCategory.COMMUTING,
            amount=0,
            description="No commuting deduction",
            is_automatic=True,
            notes=""
        )

    def calculate_insurance_deduction(self,
                                     annual_premiums: float,
                                     premium_subsidies: float,
                                     user_profile: UserProfile) -> Deduction:
        """
        Calculate insurance premium deduction

        Includes health insurance, accident insurance, life insurance (Säule 3b),
        and savings interest.

        Args:
            annual_premiums: Total annual insurance premiums paid
            premium_subsidies: Premium subsidies received (Prämienverbilligung)
            user_profile: User profile

        Returns:
            Deduction for insurance premiums
        """
        # Get maximum deduction for federal level
        civil_status = 'single' if user_profile.civil_status.value == 'single' else 'married'
        max_federal = get_max_insurance_deduction(
            civil_status=civil_status,
            has_pillar2=user_profile.has_pillar2,
            num_children=user_profile.num_children,
            level='federal'
        )

        # Premiums minus subsidies
        net_premiums = max(0, annual_premiums - premium_subsidies)

        # Apply limit
        actual_amount = min(net_premiums, max_federal)

        return Deduction(
            category=DeductionCategory.INSURANCE,
            amount=actual_amount,
            description=f"Insurance premiums (health, accident, life insurance Säule 3b)",
            is_automatic=False,
            notes=f"Maximum deduction: CHF {max_federal:,.0f}. "
                  f"Must subtract premium subsidies (Prämienverbilligung). "
                  f"In practice, often fully used by health insurance premiums alone."
        )

    def validate_pillar3a_contribution(self,
                                      contribution: float,
                                      user_profile: UserProfile) -> Tuple[bool, str, float, Deduction]:
        """
        Validate Pillar 3a contribution against 2025 limits

        Args:
            contribution: Proposed Pillar 3a contribution
            user_profile: User profile

        Returns:
            Tuple of (is_valid, message, max_allowed, Deduction object)
        """
        max_amount = get_pillar_3a_limit(
            has_pillar2=user_profile.has_pillar2,
            net_income=user_profile.gross_salary
        )

        if contribution > max_amount:
            return (
                False,
                f"Contribution exceeds 2025 limit of CHF {max_amount:,.2f}",
                max_amount,
                None
            )

        if contribution < 0:
            return (
                False,
                "Contribution must be non-negative",
                max_amount,
                None
            )

        deduction = Deduction(
            category=DeductionCategory.PILLAR_3A,
            amount=contribution,
            description=f"Pillar 3a contribution (max CHF {max_amount:,.2f} in 2025)",
            is_automatic=False,
            notes="Requires official contribution certificate (Einzahlungsbestätigung). "
                  "Fully deductible. Must have AHV-liable income."
        )

        return (True, "Valid contribution", max_amount, deduction)

    def calculate_education_deduction(self,
                                     education_costs: float,
                                     has_proof: bool = False) -> Tuple[bool, str, Deduction]:
        """
        Calculate further education deduction

        Args:
            education_costs: Annual education costs
            has_proof: Whether user has receipts/proof

        Returns:
            Tuple of (is_valid, message, Deduction object)
        """
        max_amount = self.limits['education']['maximum']
        zh_pauschal = self.limits['education']['zh_pauschal_no_proof']

        if education_costs <= 0:
            return (True, "No education costs", None)

        # In Zürich, up to CHF 500 without proof
        if education_costs <= zh_pauschal:
            deduction = Deduction(
                category=DeductionCategory.EDUCATION,
                amount=education_costs,
                description=f"Further education costs (no proof required up to CHF {zh_pauschal})",
                is_automatic=False,
                notes="In Zürich, up to CHF 500 requires no proof. "
                      "Must be 20+ years old with completed secondary education."
            )
            return (True, "Valid deduction (no proof needed)", deduction)

        # Above CHF 500 requires proof
        if not has_proof:
            return (
                False,
                f"Costs above CHF {zh_pauschal} require receipts/proof",
                None
            )

        # Apply maximum limit
        actual_amount = min(education_costs, max_amount)

        deduction = Deduction(
            category=DeductionCategory.EDUCATION,
            amount=actual_amount,
            description=f"Further education costs (with proof, max CHF {max_amount:,.0f})",
            is_automatic=False,
            notes=f"Maximum CHF {max_amount:,.0f}. Excludes hobby courses, sports, wellness. "
                  "Requires receipts and proof of educational nature."
        )

        return (True, "Valid deduction", deduction)

    def calculate_charitable_deduction(self,
                                       donation_amount: float,
                                       net_income: float) -> Tuple[bool, str, Deduction]:
        """
        Calculate charitable donation deduction

        Args:
            donation_amount: Total annual donations
            net_income: Net income for percentage calculation

        Returns:
            Tuple of (is_valid, message, Deduction object)
        """
        min_amount = self.limits['charitable']['minimum']
        max_rate = self.limits['charitable']['maximum_rate']
        max_amount = net_income * max_rate

        if donation_amount < min_amount:
            return (
                False,
                f"Minimum donation for deduction is CHF {min_amount}",
                None
            )

        if donation_amount > max_amount:
            return (
                False,
                f"Donation exceeds maximum of {max_rate * 100}% of net income (CHF {max_amount:,.2f})",
                None
            )

        deduction = Deduction(
            category=DeductionCategory.CHARITABLE,
            amount=donation_amount,
            description=f"Charitable donations (min CHF {min_amount}, max {max_rate * 100}% of net income)",
            is_automatic=False,
            notes="Must be to Swiss tax-exempt organizations. Requires donation receipts. "
                  "Excludes cultural/sports clubs."
        )

        return (True, "Valid deduction", deduction)

    def calculate_political_donation_deduction(self,
                                               donation_amount: float) -> Tuple[bool, str, Deduction]:
        """
        Calculate political party donation deduction

        Args:
            donation_amount: Total annual political donations

        Returns:
            Tuple of (is_valid, message, Deduction object)
        """
        federal_max = self.limits['political_donations']['federal_max']
        zh_max = self.limits['political_donations']['zh_max']

        # Use lower of federal and cantonal limits
        max_amount = min(federal_max, zh_max)

        if donation_amount <= 0:
            return (True, "No political donations", None)

        if donation_amount > max_amount:
            return (
                False,
                f"Donation exceeds maximum of CHF {max_amount:,.0f} "
                f"(Federal: CHF {federal_max:,.0f}, Zürich: CHF {zh_max:,.0f})",
                None
            )

        deduction = Deduction(
            category=DeductionCategory.POLITICAL,
            amount=donation_amount,
            description=f"Political party donations (max CHF {max_amount:,.0f})",
            is_automatic=False,
            notes="Party must be registered in official party register. Requires receipts."
        )

        return (True, "Valid deduction", deduction)

    def get_all_automatic_deductions(self,
                                    user_profile: UserProfile,
                                    has_canteen_subsidy: bool = False) -> List[Deduction]:
        """
        Get all automatic/pauschal deductions that don't require proof

        Args:
            user_profile: User profile
            has_canteen_subsidy: Whether user has canteen subsidy

        Returns:
            List of automatic deductions
        """
        deductions = []

        # Professional expenses (always automatic)
        net_salary = user_profile.gross_salary  # Simplified - should subtract social security
        prof_deduction = self.calculate_professional_expenses(net_salary)
        deductions.append(prof_deduction)

        # Meal expenses (automatic)
        meal_deduction = self.calculate_meal_expenses(
            has_canteen_subsidy,
            user_profile.employment_percentage
        )
        deductions.append(meal_deduction)

        return deductions
