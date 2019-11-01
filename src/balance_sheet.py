"""Classes used to construct the balance sheet"""
from dataclasses import dataclass


class BalanceSheet:
    def __init__(self) -> None:
        self.assets = Assets()
        self.liabilities = Liabilities()
        self.equity = Equity()

    def current_assets(self) -> float:
        return sum(
            [
                self.assets.cash,
                self.assets.accounts_receivable,
                self.assets.bad_debts_provision,
                self.assets.properties_intended_for_sale,
                self.assets.other_receivables,
                self.assets.prepayments,
                self.assets.inventory,
                self.assets.contract_costs_incurred,
                self.assets.financial_instruments,
                self.assets.short_term_investments,
            ]
        )

    def fixed_assets(self) -> float:
        return self.assets.fixed_assets_at_cost + self.assets.depreciation

    def intangible_assets(self) -> float:
        return self.assets.goodwill + self.assets.amortization

    def total_assets(self) -> float:
        return self.current_assets() + self.fixed_assets() + self.intangible_assets()

    def current_liabilities(self) -> float:
        return sum(
            [
                self.liabilities.trade_payables,
                self.liabilities.accruals,
                self.liabilities.accrued_income_tax,
                self.liabilities.deferred_income,
                self.liabilities.financial_instruments,
            ]
        )

    def total_liabilities(self) -> float:
        return self.current_liabilities() + self.liabilities.long_term_debt

    def total_equity(self) -> float:
        return (
            self.equity.retained_earnings
            + self.equity.reserves
            + self.equity.intercompany
        )

    def balance(self) -> bool:
        return abs(
            round(self.total_assets())
            - round((self.total_liabilities() + self.total_equity()))
        )

    def invested_capital(self) -> float:
        return self.total_assets() - self.current_liabilities()


# Assets
@dataclass
class Assets:
    # Current assets
    cash = 9.6432 * 1000
    accounts_receivable = 3021.78736 * 1000
    bad_debts_provision = -23.06192 * 1000
    properties_intended_for_sale = 0 * 1000
    other_receivables = 157.71968 * 1000
    prepayments = 88.10512 * 1000
    inventory = 36.29712 * 1000
    contract_costs_incurred = 0 * 1000
    financial_instruments = 0 * 1000
    short_term_investments = 0 * 1000

    # Fixed assets
    fixed_assets_at_cost = 25283.98976 * 1000
    depreciation = -13039.2168 * 1000
    of_which_fleet = 2932.3288526946 * 1000
    of_which_pe = 6158.4905906587 * 1000
    of_which_other = 3152.9535166467 * 1000

    # Intangible
    goodwill = 15709.84464 * 1000
    amortization = -4924.30976 * 1000


@dataclass
class Liabilities:
    trade_payables = 1278.88384 * 1000
    accruals = 375.64208 * 1000
    accrued_income_tax = 0
    deferred_income = 2066.5976 * 1000
    financial_instruments = 0
    long_term_debt = 1200.52368 * 1000


@dataclass
class Equity:
    retained_earnings = 55879.86976 * 1000
    reserves = 0
    intercompany = -34488.62672 * 1000

