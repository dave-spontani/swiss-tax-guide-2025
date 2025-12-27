"""
Swiss Tax Calculator Service

Core tax calculation engine for Swiss federal, cantonal, and municipal taxes.
Implements progressive tax rate calculations for the three-tier Swiss system.
"""

from typing import Dict, List
from models.user_profile import UserProfile
from models.deduction import Deduction
from models.tax_calculation import TaxBreakdown, CalculationStep
from config.tax_rates_2025 import (
    get_federal_tax_rates,
    get_zh_cantonal_rates,
    get_zh_cantonal_multiplier
)
from config.deduction_limits import SOCIAL_SECURITY_RATES


class SwissTaxCalculator:
    """
    Core tax calculation engine for Swiss federal, cantonal, and municipal taxes
    """

    def __init__(self, tax_year: int = 2025):
        self.tax_year = tax_year
        self.federal_rates = get_federal_tax_rates()
        self.zh_cantonal_rates = get_zh_cantonal_rates()
        self.cantonal_multiplier = get_zh_cantonal_multiplier()

    def calculate_social_security(self, gross_salary: float) -> Dict[str, float]:
        """
        Calculate social security contributions (AHV/IV/ALV/NBU)
        These are fully deductible from gross income

        Args:
            gross_salary: Annual gross salary in CHF

        Returns:
            Dictionary with breakdown of social security contributions
        """
        # AHV/IV/EO: 5.3% (employee portion)
        ahv_iv_eo = gross_salary * SOCIAL_SECURITY_RATES['ahv_iv_eo']['rate']

        # ALV (unemployment): 1.1% up to CHF 148,200
        alv_ceiling = SOCIAL_SECURITY_RATES['alv']['max_income']
        alv_base = min(gross_salary, alv_ceiling)
        alv = alv_base * SOCIAL_SECURITY_RATES['alv']['rate']

        # Additional ALV above ceiling (0.5%)
        if gross_salary > alv_ceiling:
            alv += (gross_salary - alv_ceiling) * SOCIAL_SECURITY_RATES['alv']['additional_rate_above_ceiling']

        # NBU (non-occupational accident): ~0.7% (varies by employer)
        nbu = gross_salary * SOCIAL_SECURITY_RATES['nbu']['rate']

        total = ahv_iv_eo + alv + nbu

        return {
            'ahv_iv_eo': ahv_iv_eo,
            'alv': alv,
            'nbu': nbu,
            'total': total
        }

    def _apply_progressive_rates(self, income: float, rate_table: List[Dict]) -> float:
        """
        Apply progressive tax rates from rate table

        Args:
            income: Taxable income
            rate_table: List of tax brackets with thresholds, rates, and base taxes

        Returns:
            Calculated tax amount
        """
        if income <= 0:
            return 0.0

        # Find the applicable bracket
        for i in range(len(rate_table) - 1, -1, -1):
            bracket = rate_table[i]
            if income >= bracket['threshold']:
                # Calculate tax: base tax + (excess over threshold × marginal rate)
                excess = income - bracket['threshold']
                tax = bracket['base_tax'] + (excess * bracket['rate'])
                return tax

        # Income is below first threshold
        return 0.0

    def _get_marginal_rate(self, income: float, rate_table: List[Dict]) -> float:
        """
        Get marginal tax rate for given income

        Args:
            income: Taxable income
            rate_table: List of tax brackets

        Returns:
            Marginal tax rate as percentage
        """
        if income <= 0:
            return 0.0

        for i in range(len(rate_table) - 1, -1, -1):
            bracket = rate_table[i]
            if income >= bracket['threshold']:
                return bracket['rate'] * 100  # Convert to percentage

        return 0.0

    def calculate_federal_tax(self, taxable_income: float) -> Dict[str, float]:
        """
        Calculate progressive federal tax using 2025 rates

        Args:
            taxable_income: Income after all deductions

        Returns:
            Dictionary with tax amount, marginal rate, and effective rate
        """
        if taxable_income <= 0:
            return {'tax': 0, 'marginal_rate': 0, 'effective_rate': 0}

        tax = self._apply_progressive_rates(taxable_income, self.federal_rates)
        marginal_rate = self._get_marginal_rate(taxable_income, self.federal_rates)
        effective_rate = (tax / taxable_income * 100) if taxable_income > 0 else 0

        return {
            'tax': tax,
            'marginal_rate': marginal_rate,
            'effective_rate': effective_rate
        }

    def calculate_cantonal_tax(self, taxable_income: float,
                                municipal_multiplier: float) -> Dict[str, float]:
        """
        Calculate Zürich cantonal and municipal taxes

        Municipal tax = Cantonal base tax × municipal multiplier
        Cantonal tax = Cantonal base tax × cantonal multiplier (0.98)

        Args:
            taxable_income: Income after all deductions
            municipal_multiplier: Municipal tax multiplier (e.g., 1.19 for Zürich City)

        Returns:
            Dictionary with cantonal tax, municipal tax, and totals
        """
        if taxable_income <= 0:
            return {
                'base_tax': 0,
                'cantonal_tax': 0,
                'municipal_tax': 0,
                'total': 0
            }

        # Calculate base cantonal tax using progressive rates
        base_cantonal_tax = self._apply_progressive_rates(
            taxable_income,
            self.zh_cantonal_rates
        )

        # Apply cantonal multiplier (0.98 for Zürich)
        cantonal_tax = base_cantonal_tax * self.cantonal_multiplier

        # Calculate municipal tax using municipal multiplier
        municipal_tax = base_cantonal_tax * municipal_multiplier

        # Total cantonal + municipal
        total = cantonal_tax + municipal_tax

        return {
            'base_tax': base_cantonal_tax,
            'cantonal_tax': cantonal_tax,
            'municipal_tax': municipal_tax,
            'total': total
        }

    def calculate_complete_breakdown(self,
                                      user_profile: UserProfile,
                                      deductions: List[Deduction]) -> TaxBreakdown:
        """
        Complete tax calculation with full breakdown

        Args:
            user_profile: User's profile information
            deductions: List of applicable deductions

        Returns:
            TaxBreakdown object with complete calculation details
        """
        steps = []
        gross = user_profile.gross_salary

        # Step 1: Gross salary
        steps.append(CalculationStep(
            step_number=1,
            title="Gross Annual Salary",
            description="Your annual gross salary before any deductions",
            amount=gross,
            formula=f"CHF {gross:,.2f}"
        ))

        # Step 2: Social security deductions
        social_security = self.calculate_social_security(gross)
        adjusted_income = gross - social_security['total']

        steps.append(CalculationStep(
            step_number=2,
            title="Social Security Contributions",
            description=f"AHV/IV/EO: CHF {social_security['ahv_iv_eo']:,.2f} | "
                        f"ALV: CHF {social_security['alv']:,.2f} | "
                        f"NBU: CHF {social_security['nbu']:,.2f}",
            amount=-social_security['total'],
            formula=f"CHF {gross:,.2f} - CHF {social_security['total']:,.2f}"
        ))

        steps.append(CalculationStep(
            step_number=3,
            title="Adjusted Income",
            description="Gross salary minus social security contributions",
            amount=adjusted_income,
            formula=f"CHF {adjusted_income:,.2f}"
        ))

        # Step 3: Apply deductions
        total_deductions = sum(d.amount for d in deductions)

        steps.append(CalculationStep(
            step_number=4,
            title="Total Deductions",
            description=f"{len(deductions)} deduction(s) applied",
            amount=-total_deductions,
            formula=f"Sum of all deductions"
        ))

        # Taxable income (same for federal and cantonal in this simplified model)
        taxable_income = max(0, adjusted_income - total_deductions)

        steps.append(CalculationStep(
            step_number=5,
            title="Taxable Income",
            description="Income after all deductions - this is what gets taxed",
            amount=taxable_income,
            formula=f"CHF {adjusted_income:,.2f} - CHF {total_deductions:,.2f}"
        ))

        # Step 4: Calculate federal tax
        federal_result = self.calculate_federal_tax(taxable_income)

        steps.append(CalculationStep(
            step_number=6,
            title="Federal Tax",
            description=f"Progressive rate | Effective rate: {federal_result['effective_rate']:.2f}% | "
                        f"Marginal rate: {federal_result['marginal_rate']:.2f}%",
            amount=federal_result['tax'],
            formula=f"Applied to CHF {taxable_income:,.2f}"
        ))

        # Step 5: Calculate cantonal/municipal tax
        cantonal_result = self.calculate_cantonal_tax(
            taxable_income,
            user_profile.municipality_multiplier
        )

        steps.append(CalculationStep(
            step_number=7,
            title="Cantonal Tax (Zürich)",
            description=f"Base tax × cantonal multiplier ({self.cantonal_multiplier})",
            amount=cantonal_result['cantonal_tax'],
            formula=f"CHF {cantonal_result['base_tax']:,.2f} × {self.cantonal_multiplier}"
        ))

        steps.append(CalculationStep(
            step_number=8,
            title=f"Municipal Tax ({user_profile.municipality})",
            description=f"Base tax × municipal multiplier ({user_profile.municipality_multiplier})",
            amount=cantonal_result['municipal_tax'],
            formula=f"CHF {cantonal_result['base_tax']:,.2f} × {user_profile.municipality_multiplier}"
        ))

        # Total tax
        total_tax = federal_result['tax'] + cantonal_result['total']

        steps.append(CalculationStep(
            step_number=9,
            title="Total Tax Burden",
            description="Federal + Cantonal + Municipal",
            amount=total_tax,
            formula=f"CHF {federal_result['tax']:,.2f} + CHF {cantonal_result['cantonal_tax']:,.2f} + "
                    f"CHF {cantonal_result['municipal_tax']:,.2f}"
        ))

        # Net income
        net_annual = gross - social_security['total'] - total_tax

        steps.append(CalculationStep(
            step_number=10,
            title="Net Annual Income",
            description="Take-home pay after taxes and social security",
            amount=net_annual,
            formula=f"CHF {gross:,.2f} - CHF {social_security['total']:,.2f} - CHF {total_tax:,.2f}"
        ))

        # Calculate overall effective tax rate
        overall_effective_rate = (total_tax / gross * 100) if gross > 0 else 0

        # Build TaxBreakdown object
        return TaxBreakdown(
            gross_salary=gross,
            social_security_deductions=social_security['total'],
            adjusted_income=adjusted_income,
            total_deductions=total_deductions,
            deduction_details=deductions,
            taxable_income_federal=taxable_income,
            taxable_income_cantonal=taxable_income,
            federal_tax=federal_result['tax'],
            cantonal_tax=cantonal_result['cantonal_tax'],
            municipal_tax=cantonal_result['municipal_tax'],
            total_tax=total_tax,
            effective_tax_rate=overall_effective_rate,
            marginal_tax_rate=federal_result['marginal_rate'],
            net_annual_income=net_annual,
            net_monthly_income=net_annual / 12,
            calculation_steps=steps
        )

    def calculate_tax_savings(self,
                             user_profile: UserProfile,
                             base_deductions: List[Deduction],
                             additional_deduction: Deduction) -> Dict[str, float]:
        """
        Calculate tax savings from an additional deduction

        Args:
            user_profile: User's profile
            base_deductions: Current deductions
            additional_deduction: Additional deduction to test

        Returns:
            Dictionary with savings breakdown
        """
        # Calculate tax without additional deduction
        tax_without = self.calculate_complete_breakdown(user_profile, base_deductions)

        # Calculate tax with additional deduction
        all_deductions = base_deductions + [additional_deduction]
        tax_with = self.calculate_complete_breakdown(user_profile, all_deductions)

        # Calculate savings
        federal_savings = tax_without.federal_tax - tax_with.federal_tax
        cantonal_savings = tax_without.cantonal_tax - tax_with.cantonal_tax
        municipal_savings = tax_without.municipal_tax - tax_with.municipal_tax
        total_savings = federal_savings + cantonal_savings + municipal_savings

        savings_rate = (total_savings / additional_deduction.amount * 100) if additional_deduction.amount > 0 else 0

        return {
            'federal_savings': federal_savings,
            'cantonal_savings': cantonal_savings,
            'municipal_savings': municipal_savings,
            'total_savings': total_savings,
            'savings_rate': savings_rate
        }
