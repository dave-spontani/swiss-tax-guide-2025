"""Optimization models for Swiss Tax Analyzer"""

from dataclasses import dataclass
from typing import List
from enum import Enum


class OptimizationType(Enum):
    """Types of optimization suggestions"""
    INCREASE_DEDUCTION = "increase_deduction"
    UTILIZE_PAUSCHAL = "utilize_pauschal"
    PILLAR_3A = "maximize_pillar_3a"
    EDUCATION = "use_education_deduction"
    CHARITABLE = "charitable_giving"
    COMMUTING = "optimize_commuting"
    PILLAR_2_BUYBACK = "pillar_2_buyback"


@dataclass
class OptimizationSuggestion:
    """Individual optimization recommendation"""
    suggestion_type: OptimizationType
    title: str
    description: str
    current_deduction: float
    recommended_deduction: float
    potential_savings: float
    effort_level: str  # "Easy", "Moderate", "Requires Documentation"
    action_items: List[str]
    priority: int  # 1 = highest priority

    @property
    def additional_deduction(self) -> float:
        """Calculate additional deduction needed"""
        return self.recommended_deduction - self.current_deduction
