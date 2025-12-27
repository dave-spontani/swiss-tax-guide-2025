"""
Application constants for Swiss Tax Analyzer
"""

# Application metadata
APP_NAME = "Swiss Tax Deduction Analyzer"
APP_VERSION = "1.0.0"
TAX_YEAR = 2025
APP_ICON = "🇨🇭"

# Default values
DEFAULT_CANTON = "ZH"
DEFAULT_MUNICIPALITY = "Zürich"
DEFAULT_EMPLOYMENT_PERCENTAGE = 100.0
DEFAULT_HAS_PILLAR2 = True
DEFAULT_WORK_DAYS_PER_YEAR = 220

# Color scheme for UI
COLOR_INCOME = "#28a745"  # Green
COLOR_DEDUCTION = "#007bff"  # Blue
COLOR_TAX = "#dc3545"  # Red
COLOR_SAVINGS = "#ffc107"  # Yellow/Gold
COLOR_NEUTRAL = "#6c757d"  # Gray

# Badge colors
BADGE_SUCCESS = "green"
BADGE_INFO = "blue"
BADGE_WARNING = "orange"
BADGE_DANGER = "red"

# Deduction categories display names
DEDUCTION_DISPLAY_NAMES = {
    "commuting": "Commuting Costs",
    "meals": "Meal Expenses",
    "professional_expenses": "Professional Expenses",
    "insurance_premiums": "Insurance Premiums",
    "pillar_3a": "Pillar 3a Contribution",
    "pillar_2_buyback": "Pillar 2 Buy-in",
    "further_education": "Further Education",
    "charitable_donations": "Charitable Donations",
    "political_donations": "Political Party Donations"
}

# Help text
HELP_TEXT = {
    "gross_salary": "Your annual gross salary before any deductions (Bruttolohn)",
    "employment_percentage": "100% for full-time, 50% for half-time, etc.",
    "has_pillar2": "Are you enrolled in a company pension fund (2nd pillar)?",
    "municipality": "Your municipality of residence determines the municipal tax rate",
    "commuting": "Costs of traveling between home and workplace",
    "meals": "Extra costs for eating lunch away from home during work",
    "professional_expenses": "Work-related expenses: tools, software, literature, work clothes",
    "insurance": "Health insurance, accident insurance, life insurance (Säule 3b)",
    "pillar_3a": "Private pension savings (3rd pillar a) - fully tax deductible",
    "education": "Costs for job-related further education and training",
    "charitable": "Donations to tax-exempt charitable organizations",
    "political": "Donations to registered political parties"
}

# Tooltips
TOOLTIPS = {
    "pauschal": "Automatic deduction requiring no proof (pauschal)",
    "proof_required": "Requires receipts or certificates as proof",
    "employer_confirmation": "Requires confirmation from employer",
    "tax_savings": "Amount of taxes saved by claiming this deduction",
    "effective_rate": "Total tax as percentage of gross salary",
    "marginal_rate": "Tax rate on your last franc of income"
}

# Navigation
TAB_ICONS = {
    "calculation": "📊",
    "checklist": "✅",
    "comparison": "💰",
    "optimization": "🎯",
    "export": "📄"
}

# Export templates
PDF_TITLE = "Swiss Tax Calculation Report"
PDF_SUBTITLE = f"Tax Year {TAX_YEAR}"
CSV_FILENAME_TEMPLATE = "tax_calculation_{year}_{timestamp}.csv"
PDF_FILENAME_TEMPLATE = "tax_report_{year}_{timestamp}.pdf"
