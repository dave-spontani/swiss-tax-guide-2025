"""
Data models for Swiss tax calculations
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class UserProfile:
    """
    User profile containing all information needed for tax calculation.
    """
    # Personal
    marital_status: str = 'single'  # 'single', 'married', 'separated', 'divorced'
    num_children: int = 0
    children_ages: List[int] = field(default_factory=list)
    religious_affiliation: str = 'none'  # 'none', 'reformed', 'catholic', 'christian-catholic'

    # Employment
    employment_type: str = 'employed'  # 'employed', 'self_employed', 'both', 'retired', 'not_working'
    net_salary: float = 0.0
    has_side_income: bool = False
    side_income_amount: float = 0.0

    # Employment details (for automatic deductions)
    commutes_to_work: bool = True
    bikes_to_work: bool = False  # CHF 700 pauschal if True
    uses_public_transport_car: bool = False  # Can claim actual costs
    works_away_from_home: bool = True
    employer_meal_subsidy: bool = False

    # ========== SPOUSE-SPECIFIC EMPLOYMENT (FOR MARRIED COUPLES) ==========
    # Spouse 1 (primary person - used for singles OR first person if married)
    spouse1_employment_type: str = 'employed'
    spouse1_net_salary: float = 0.0
    spouse1_has_side_income: bool = False
    spouse1_side_income_amount: float = 0.0

    # Spouse 1 commuting
    spouse1_bikes_to_work: bool = False
    spouse1_uses_public_transport_car: bool = False
    spouse1_actual_commuting_costs: float = 0.0

    # Spouse 1 meals
    spouse1_works_away_from_home: bool = True
    spouse1_employer_meal_subsidy: bool = False

    # Spouse 2 (second person - only used if married)
    spouse2_employment_type: str = 'not_working'
    spouse2_net_salary: float = 0.0
    spouse2_has_side_income: bool = False
    spouse2_side_income_amount: float = 0.0

    # Spouse 2 commuting
    spouse2_bikes_to_work: bool = False
    spouse2_uses_public_transport_car: bool = False
    spouse2_actual_commuting_costs: float = 0.0

    # Spouse 2 meals
    spouse2_works_away_from_home: bool = False
    spouse2_employer_meal_subsidy: bool = False

    # Assets
    owns_property: bool = False
    property_age: Optional[int] = None
    eigenmietwert: Optional[float] = None
    has_securities: bool = False
    securities_value: Optional[float] = None
    total_wealth: float = 0.0

    # Special circumstances
    is_disabled: bool = False
    supports_others: bool = False
    pays_alimony: bool = False
    both_spouses_work: bool = False  # For dual income deduction

    # Location
    municipality: str = 'Zürich'
    gemeinde_steuerfuss: int = 119  # Default: Zürich

    # Optional deduction choices
    claim_actual_commuting: bool = False
    actual_commuting_costs: float = 0.0
    claim_actual_professional: bool = False
    actual_professional_costs: float = 0.0
    claim_actual_property_maintenance: bool = False
    actual_property_maintenance_costs: float = 0.0


@dataclass
class DeductionResult:
    """
    Detailed breakdown of all deductions.
    """
    # Automatic deductions (no receipts needed)
    commuting_pauschal: float = 0.0
    meal_costs_pauschal: float = 0.0
    professional_expenses: float = 0.0
    side_income_deduction: float = 0.0
    child_deductions: float = 0.0
    property_maintenance: float = 0.0
    asset_management: float = 0.0
    insurance_premiums: float = 0.0
    dual_income_deduction: float = 0.0
    total_automatic: float = 0.0

    # Optional deductions (require documentation)
    pillar_3a: float = 0.0
    pillar_2_buyins: float = 0.0
    ahv_contributions: float = 0.0
    mortgage_interest: float = 0.0
    other_debt_interest: float = 0.0
    medical_costs: float = 0.0
    medical_costs_deductible: float = 0.0  # After 5% threshold
    childcare_costs: float = 0.0
    donations: float = 0.0
    political_contributions: float = 0.0
    alimony_payments: float = 0.0
    support_payments: float = 0.0
    total_optional: float = 0.0

    # Total deductions
    total_deductions: float = 0.0

    def calculate_totals(self):
        """Calculate total deductions."""
        self.total_automatic = (
            self.commuting_pauschal +
            self.meal_costs_pauschal +
            self.professional_expenses +
            self.side_income_deduction +
            self.child_deductions +
            self.property_maintenance +
            self.asset_management +
            self.insurance_premiums +
            self.dual_income_deduction
        )

        self.total_optional = (
            self.pillar_3a +
            self.pillar_2_buyins +
            self.ahv_contributions +
            self.mortgage_interest +
            self.other_debt_interest +
            self.medical_costs_deductible +
            self.childcare_costs +
            self.donations +
            self.political_contributions +
            self.alimony_payments +
            self.support_payments
        )

        self.total_deductions = self.total_automatic + self.total_optional


@dataclass
class TaxResult:
    """
    Complete tax calculation result.
    """
    # Input
    gross_income: float = 0.0
    total_deductions: float = 0.0
    taxable_income: float = 0.0

    # Federal tax
    federal_tax: float = 0.0
    federal_effective_rate: float = 0.0
    federal_marginal_rate: float = 0.0
    federal_bracket_index: int = 0

    # Cantonal tax (Zurich)
    einfache_staatssteuer: float = 0.0
    cantonal_tax: float = 0.0               # einfache × cantonal_steuerfuss
    municipal_tax: float = 0.0              # einfache × gemeinde_steuerfuss
    personalsteuer: float = 0.0             # CHF 24 flat personal tax
    total_cantonal_municipal: float = 0.0
    cantonal_effective_rate: float = 0.0
    cantonal_marginal_rate: float = 0.0
    cantonal_bracket_index: int = 0

    # Optional taxes
    church_tax: float = 0.0
    church_effective_rate: float = 0.0
    wealth_tax: float = 0.0
    wealth_effective_rate: float = 0.0

    # Total
    total_tax: float = 0.0
    total_effective_rate: float = 0.0

    # Breakdown data for display
    federal_breakdown: List[Dict] = field(default_factory=list)
    cantonal_breakdown: List[Dict] = field(default_factory=list)

    # Progress in current bracket
    progress_in_bracket: float = 0.0
    amount_to_next_bracket: float = 0.0

    def calculate_totals(self):
        """Calculate total taxes and effective rates.

        Note: Total tax excludes federal tax as it's paid separately to the federal government.
        Total includes only cantonal, municipal, personal, church, and wealth taxes (Zurich taxes).
        """
        self.total_cantonal_municipal = self.cantonal_tax + self.municipal_tax
        # Total excludes federal tax (paid separately to federal government)
        self.total_tax = (
            self.cantonal_tax +
            self.municipal_tax +
            self.personalsteuer +
            self.church_tax +
            self.wealth_tax
        )

        if self.gross_income > 0:
            self.total_effective_rate = (self.total_tax / self.gross_income) * 100
            self.federal_effective_rate = (self.federal_tax / self.gross_income) * 100
            self.cantonal_effective_rate = (self.total_cantonal_municipal / self.gross_income) * 100
            if self.church_tax > 0:
                self.church_effective_rate = (self.church_tax / self.gross_income) * 100


@dataclass
class ComparisonResult:
    """
    Comparison of tax scenarios (before deductions, after automatic, after all).
    """
    # Scenario 1: Before ANY deductions
    gross_income: float = 0.0
    tax_before_deductions: TaxResult = field(default_factory=TaxResult)

    # Scenario 2: After AUTOMATIC deductions
    automatic_deductions: float = 0.0
    tax_after_automatic: TaxResult = field(default_factory=TaxResult)
    savings_from_automatic: float = 0.0

    # Scenario 3: After ALL deductions
    total_deductions: float = 0.0
    tax_after_all_deductions: TaxResult = field(default_factory=TaxResult)
    savings_from_optional: float = 0.0
    total_savings: float = 0.0
    total_savings_percent: float = 0.0

    def calculate_savings(self):
        """Calculate savings from deductions."""
        self.savings_from_automatic = (
            self.tax_before_deductions.total_tax -
            self.tax_after_automatic.total_tax
        )

        self.savings_from_optional = (
            self.tax_after_automatic.total_tax -
            self.tax_after_all_deductions.total_tax
        )

        self.total_savings = (
            self.tax_before_deductions.total_tax -
            self.tax_after_all_deductions.total_tax
        )

        if self.tax_before_deductions.total_tax > 0:
            self.total_savings_percent = (
                self.total_savings / self.tax_before_deductions.total_tax * 100
            )
