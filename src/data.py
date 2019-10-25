from typing import Tuple, Dict

def original_assets() -> Tuple[Dict, Dict, Dict]:
    """ Return the assets per exhibit""""
    current_assets = {
        "cash": 9.6432,
        "accounts_receivable": 3021.78736,
        "bad_debts_provision": -23.06192,
        "properties_intended_for_sale": 0,
        "other_receivables": 157.71968,
        "prepayments": 88.10512,
        "inventory": 36.29712,
        "contract_costs_incurred": 0,
        "financial_instruments": 0,
        "short_term_investments": 0,
    }

    fixed_assets = {
        "fixed_assets_at_cost": 25283.98976,
        "depreciation": -13039.2168,
        "of_which_fleet": 2932.3288526946,
        "of_which_pe": 6158.4905906587,
        "of_which_other": 3152.9535166467,
    }

    intangible_assets = {"goodwill": 15709.84464, "amortisation": -4924.30976}

    return current_assets, fixed_assets, intangible_assets

def original_liabilities() -> Tuple[Dict, Dict]:
    current_liabilities = {
        "trade_payables": 1278.88384,
        "accruals": 375.64208,
        "accrued_income_tax": 0,
        "deferred_income": 2066.5976,
        "financial_instruments": 0
    }
    long_term_debt = {
        "term_debt": 1200.52368
    }

def original_revenue() -> Dict:
    return {"operating_revenue": 39778916.847903}



