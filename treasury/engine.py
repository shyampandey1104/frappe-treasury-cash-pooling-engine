"""Global Corporate Treasury Multi-Entity Cash Pooling & SOFR Intercompany Loan Engine."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class TreasuryEntityAccount:
    entity_code: str  # e.g., PARENT_SG, SUB_INDIA, SUB_UAE
    bank_account_iban: str
    currency: str
    current_cash_balance: float
    target_operating_balance: float = 100000.0  # Maintain minimum operating buffer


@dataclass
class CashSweepTransaction:
    sweep_id: str
    from_entity: str
    to_entity: str
    currency: str
    swept_amount: float
    purpose: str  # ZERO_BALANCE_SWEEP, DEFICIT_FUNDING


@dataclass
class IntercompanyLoanSchedule:
    loan_id: str
    lender_entity: str
    borrower_entity: str
    principal_amount: float
    benchmark_rate_pct: float  # e.g., SOFR 5.30%
    arm_length_margin_pct: float  # Transfer pricing spread e.g., 1.50%
    effective_interest_rate_pct: float
    monthly_interest_accrual: float
    withholding_tax_pct: float  # TDS under Section 194A / 195
    net_interest_payable: float


class TreasuryCashPoolingEngine:
    """Manages cross-border cash sweep pooling and arm's-length intercompany loan pricing."""

    def execute_eod_cash_sweeps(
        self,
        master_pool_entity: str,
        subsidiary_accounts: List[TreasuryEntityAccount]
    ) -> List[CashSweepTransaction]:
        sweeps = []
        sweep_idx = 1

        for acc in subsidiary_accounts:
            variance = acc.current_cash_balance - acc.target_operating_balance
            if variance > 0:
                # Excess cash swept up to Master Pool
                sweeps.append(CashSweepTransaction(
                    sweep_id=f"SWEEP-{sweep_idx:04d}",
                    from_entity=acc.entity_code,
                    to_entity=master_pool_entity,
                    currency=acc.currency,
                    swept_amount=round(variance, 2),
                    purpose="ZERO_BALANCE_SWEEP"
                ))
                acc.current_cash_balance = acc.target_operating_balance
                sweep_idx += 1
            elif variance < 0:
                # Deficit funded down from Master Pool
                deficit = abs(variance)
                sweeps.append(CashSweepTransaction(
                    sweep_id=f"SWEEP-{sweep_idx:04d}",
                    from_entity=master_pool_entity,
                    to_entity=acc.entity_code,
                    currency=acc.currency,
                    swept_amount=round(deficit, 2),
                    purpose="DEFICIT_FUNDING"
                ))
                acc.current_cash_balance = acc.target_operating_balance
                sweep_idx += 1

        return sweeps

    def compute_intercompany_loan(
        self,
        loan_id: str,
        lender: str,
        borrower: str,
        principal: float,
        sofr_benchmark_pct: float = 5.25,
        spread_pct: float = 1.50,
        tds_withholding_pct: float = 10.0
    ) -> IntercompanyLoanSchedule:
        effective_rate = round(sofr_benchmark_pct + spread_pct, 2)
        annual_interest = (principal * effective_rate) / 100.0
        monthly_interest = round(annual_interest / 12.0, 2)
        tds_amount = round((monthly_interest * tds_withholding_pct) / 100.0, 2)
        net_interest = round(monthly_interest - tds_amount, 2)

        return IntercompanyLoanSchedule(
            loan_id=loan_id,
            lender_entity=lender,
            borrower_entity=borrower,
            principal_amount=principal,
            benchmark_rate_pct=sofr_benchmark_pct,
            arm_length_margin_pct=spread_pct,
            effective_interest_rate_pct=effective_rate,
            monthly_interest_accrual=monthly_interest,
            withholding_tax_pct=tds_withholding_pct,
            net_interest_payable=net_interest
        )
