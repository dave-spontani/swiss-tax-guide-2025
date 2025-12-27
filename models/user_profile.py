"""User profile data model for Swiss Tax Analyzer"""

from dataclasses import dataclass
from enum import Enum


class CivilStatus(Enum):
    """Civil status options"""
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"


class Canton(Enum):
    """Swiss cantons"""
    ZURICH = "ZH"
    # Expandable for future cantons


@dataclass
class UserProfile:
    """Core user profile for tax calculation"""

    # Personal details
    civil_status: CivilStatus
    canton: Canton
    municipality: str  # e.g., "Zürich"
    municipality_multiplier: float  # e.g., 1.19 for Zürich City

    # Employment details
    gross_salary: float
    has_pillar2: bool = True  # Assumes enrolled in 2nd pillar pension

    # Family status (for future expansion)
    num_children: int = 0

    # Employment type
    employment_percentage: float = 100.0  # Full-time default

    def __post_init__(self):
        """Validate inputs"""
        if self.gross_salary < 0:
            raise ValueError("Gross salary must be non-negative")
        if not 0 < self.employment_percentage <= 100:
            raise ValueError("Employment percentage must be between 0 and 100")
        if self.municipality_multiplier < 0:
            raise ValueError("Municipality multiplier must be non-negative")
