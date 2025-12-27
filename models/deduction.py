"""Deduction models for Swiss Tax Analyzer"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class DeductionCategory(Enum):
    """Categories of tax deductions"""
    COMMUTING = "commuting"
    MEALS = "meals"
    PROFESSIONAL = "professional_expenses"
    INSURANCE = "insurance_premiums"
    PILLAR_3A = "pillar_3a"
    PILLAR_2_BUYBACK = "pillar_2_buyback"
    EDUCATION = "further_education"
    CHARITABLE = "charitable_donations"
    POLITICAL = "political_donations"


class ProofRequirement(Enum):
    """Proof requirements for deductions"""
    NO_PROOF = "no_proof_needed"  # Pauschal deductions
    PROOF_REQUIRED = "proof_required"
    EMPLOYER_CONFIRMATION = "employer_confirmation_needed"


@dataclass
class DeductionLimit:
    """Limits for specific deduction categories"""
    category: DeductionCategory
    federal_max: Optional[float]
    cantonal_max: Optional[float]
    min_amount: Optional[float] = None
    is_pauschal: bool = False
    proof_requirement: ProofRequirement = ProofRequirement.PROOF_REQUIRED
    description: str = ""


@dataclass
class Deduction:
    """Individual deduction instance"""
    category: DeductionCategory
    amount: float
    description: str
    is_automatic: bool = False  # Auto-calculated pauschal deductions
    federal_savings: float = 0.0  # Tax saved at federal level
    cantonal_savings: float = 0.0  # Tax saved at cantonal level
    municipal_savings: float = 0.0  # Tax saved at municipal level
    total_savings: float = 0.0
    notes: str = ""  # User notes or calculation details

    def __post_init__(self):
        """Calculate total savings"""
        self.total_savings = self.federal_savings + self.cantonal_savings + self.municipal_savings
