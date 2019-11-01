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
        """Assets equals liabilities plus equity (within a dollar)"""
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
    cash = 9.6432
    accounts_receivable = 3021.78736
    bad_debts_provision = -23.06192
    properties_intended_for_sale = 0
    other_receivables = 157.71968
    prepayments = 88.10512
    inventory = 36.29712
    contract_costs_incurred = 0
    financial_instruments = 0
    short_term_investments = 0

    # Fixed assets
    fixed_assets_at_cost = 25283.98976
    depreciation = -13039.2168
    of_which_fleet = 2932.3288526946
    of_which_pe = 6158.4905906587
    of_which_other = 3152.9535166467

    # Intangible
    goodwill = 15709.84464
    amortization = -4924.30976


@dataclass
class Liabilities:
    trade_payables = 1278.88384
    accruals = 375.64208
    accrued_income_tax = 0
    deferred_income = 2066.5976
    financial_instruments = 0
    long_term_debt = 1200.52368


@dataclass
class Equity:
    retained_earnings = 55879.86976
    reserves = 0
    intercompany = -34488.62672

