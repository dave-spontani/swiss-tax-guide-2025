"""Tax calculation models for Swiss Tax Analyzer"""

from dataclasses import dataclass, field
from typing import List
from models.deduction import Deduction


@dataclass
class CalculationStep:
    """Represents one step in the tax calculation"""
    step_number: int
    title: str
    description: str
    amount: float
    formula: str = ""  # Human-readable formula


@dataclass
class TaxBreakdown:
    """Detailed breakdown of tax calculation"""

    # Income progression
    gross_salary: float
    social_security_deductions: float  # AHV/IV/ALV/NBU
    adjusted_income: float

    # Deductions
    total_deductions: float
    deduction_details: List[Deduction] = field(default_factory=list)

    # Taxable income
    taxable_income_federal: float = 0.0
    taxable_income_cantonal: float = 0.0

    # Tax amounts
    federal_tax: float = 0.0
    cantonal_tax: float = 0.0
    municipal_tax: float = 0.0
    total_tax: float = 0.0

    # Effective rates
    effective_tax_rate: float = 0.0
    marginal_tax_rate: float = 0.0

    # Net income
    net_annual_income: float = 0.0
    net_monthly_income: float = 0.0

    # Calculation steps for display
    calculation_steps: List[CalculationStep] = field(default_factory=list)


@dataclass
class Pillar3aComparison:
    """Comparison with and without Pillar 3a contribution"""
    with_pillar3a: TaxBreakdown
    without_pillar3a: TaxBreakdown
    contribution_amount: float
    tax_savings: float
    net_cost: float  # Pillar 3a contribution minus tax savings
    roi_percentage: float  # Immediate return on investment

    def __post_init__(self):
        """Calculate comparison metrics"""
        self.tax_savings = self.without_pillar3a.total_tax - self.with_pillar3a.total_tax
        self.net_cost = self.contribution_amount - self.tax_savings
        self.roi_percentage = (self.tax_savings / self.contribution_amount * 100) if self.contribution_amount > 0 else 0
