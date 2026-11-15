import unittest
from treasury.engine import TreasuryCashPoolingEngine, TreasuryEntityAccount

class TestTreasuryCashPooling(unittest.TestCase):
    def test_eod_zero_balance_sweeping(self):
        engine = TreasuryCashPoolingEngine()
        sub1 = TreasuryEntityAccount(
            entity_code="SUB_INDIA",
            bank_account_iban="IN99102",
            currency="INR",
            current_cash_balance=450000.0,
            target_operating_balance=100000.0 # Excess 350,000
        )
        sub2 = TreasuryEntityAccount(
            entity_code="SUB_DUBAI",
            bank_account_iban="AE88101",
            currency="INR",
            current_cash_balance=40000.0,
            target_operating_balance=100000.0 # Deficit 60,000
        )

        sweeps = engine.execute_eod_cash_sweeps("PARENT_TREASURY_HQ", [sub1, sub2])
        self.assertEqual(len(sweeps), 2)
        self.assertEqual(sweeps[0].swept_amount, 350000.0)
        self.assertEqual(sweeps[0].purpose, "ZERO_BALANCE_SWEEP")
        self.assertEqual(sweeps[1].swept_amount, 60000.0)
        self.assertEqual(sweeps[1].purpose, "DEFICIT_FUNDING")

    def test_intercompany_sofr_loan(self):
        engine = TreasuryCashPoolingEngine()
        loan = engine.compute_intercompany_loan(
            loan_id="ICL-2026-01",
            lender="HOLDING_CORP_SG",
            borrower="OPERATING_CO_IN",
            principal=10000000.0, # ₹1 Crore
            sofr_benchmark_pct=5.0,
            spread_pct=1.5, # 6.5% effective
            tds_withholding_pct=10.0
        )
        self.assertEqual(loan.effective_interest_rate_pct, 6.5)
        # Annual = 650,000. Monthly = 54,166.67
        self.assertAlmostEqual(loan.monthly_interest_accrual, 54166.67, places=1)
        self.assertAlmostEqual(loan.net_interest_payable, 48750.00, places=1)

if __name__ == "__main__":
    unittest.main()
