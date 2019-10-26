from typing import Tuple, Dict

# helper to correct values on different scale
def times_1000(input_dict: Dict) -> Dict:
    return {key: value * 1000 for key, value in input_dict.items()}


def original_assets() -> Tuple[Dict, Dict, Dict]:
    """ Return the assets per exhibit"""
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

    return (
        times_1000(current_assets),
        times_1000(fixed_assets),
        times_1000(intangible_assets),
    )


def original_liabilities() -> Tuple[Dict, Dict]:
    """Return liabilities"""
    current_liabilities = {
        "trade_payables": 1278.88384,
        "accruals": 375.64208,
        "accrued_income_tax": 0,
        "deferred_income": 2066.5976,
        "financial_instruments": 0,
    }
    long_term_debt = {"term_debt": 1200.52368}

    return (times_1000(current_liabilities), times_1000(long_term_debt))


def original_equity() -> Dict:

    equity = {
        "retained_earnings": 55879.86976,
        "reserves": 0,
        "intercompany": -34488.62672,
    }
    return times_1000(equity)


def original_revenue() -> Dict:
    return {"operating_revenue": 39778916.847903}


def original_expenses() -> Tuple[Dict, Dict]:
    opex = {
        "labor_subcontract": 5988550.3346616,
        "disposal": 6485195.3164922,
        "other_op": 11788263.327227,
        "sga": 2540439.5069915,
        "other_inc_exp": -320642.23237,
        "management_fees": 1536074.53672,
        "non_rec_items": 0,
    }

    da = {"depreciation": 4685375.9208466, "amortization": 79591.293499997}

    return opex, da


def original_operations() -> Tuple[Dict, Dict, Dict]:
    productivity = {
        "avg_num_trucks": 78,
        "total_lifts": 375528,
        "total_m3_collected": 1078787,
        "avg_km_per_truck_per_year": 42971.331458261,
        "total_tonnes_disposed": 97928,
        "working_days_per_year": 330,
        "num_customers": 22519,
    }

    truck = {
        "capacity": 45,
        "fuel_econ_km_l": 1.19,
        "fuel_cost_per_l": 1.95,
        "maintenance_per_truck_per_year": 27764.2831578947,
    }

    labor = {"driver_hourly_wage": 15.21, "hours_per_shift": 10}

    return productivity, truck, labor
