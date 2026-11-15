# Frappe Global Corporate Treasury Cash Pooling Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FinTech](https://img.shields.io/badge/Treasury-Cash%20Sweeps%20%26%20SOFR-darkgreen.svg)](https://frappe.io)

Automated multi-entity liquidity cash management solving idle capital traps through Zero-Balance Account (ZBA) sweeps, notional cash pooling, and arm's length SOFR intercompany loans.

## Features
- **End-of-Day (EOD) Automated Cash Sweeps:** Automatically pools surplus subsidiary cash while topping up deficit operating accounts.
- **Transfer Pricing SOFR Loan Amortizer:** Dynamically indexes intercompany debt against SOFR benchmarks with statutory tax withholding (TDS).
- **Arm's Length Documentation:** Generates audit-ready transfer pricing evidence protecting against cross-border profit shifting inquiries.

## Tests
```bash
python3 -m unittest discover tests
```
