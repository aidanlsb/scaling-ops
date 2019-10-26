"""Classes used to construct the balance sheet"""
from src.data import original_assets, original_liabilities, original_equity

# Assets
class CurrentAssets:
    def __init__(
        self,
        cash: float,
        accounts_receivable: float,
        bad_debts_provision: float,
        properties_intended_for_sale: float,
        other_receivables: float,
        prepayments: float,
        inventory: float,
        contract_costs_incurred: float,
        financial_instruments: float,
        short_term_investments: float,
    ) -> None:
        self.cash = cash
        self.accounts_receivable = accounts_receivable
        self.bad_debts_provision = bad_debts_provision
        self.properties_intended_for_sale = properties_intended_for_sale
        self.other_receivables = other_receivables
        self.prepayments = prepayments
        self.inventory = inventory
        self.contract_costs_incurred = contract_costs_incurred
        self.financial_instruments = financial_instruments
        self.short_term_investments = short_term_investments

    def total(self) -> float:
        return sum(
            [
                self.cash,
                self.accounts_receivable,
                self.bad_debts_provision,
                self.properties_intended_for_sale,
                self.other_receivables,
                self.prepayments,
                self.inventory,
                self.contract_costs_incurred,
                self.financial_instruments,
                self.short_term_investments,
            ]
        )


class FixedAssets:
    def __init__(
        self,
        fixed_assets_at_cost: float,
        depreciation: float,
        of_which_fleet: float,
        of_which_pe: float,
        of_which_other: float,
    ) -> None:

        self.fixed_assets_at_cost = fixed_assets_at_cost
        self.depreciation = depreciation
        self.of_which_fleet = of_which_fleet
        self.of_which_pe = of_which_pe
        self.of_which_other = of_which_other

    def total(self) -> float:
        return self.fixed_assets_at_cost + self.depreciation


class IntangibleAssets:
    def __init__(self, goodwill: float, amortisation: float) -> None:
        self.goodwill = goodwill
        self.amortisation = amortisation

    def total(self) -> float:
        return self.goodwill + self.amortisation


class Assets:
    def __init__(
        self,
        current_assets: CurrentAssets,
        fixed_assets: FixedAssets,
        intangible_assets: IntangibleAssets,
    ) -> None:
        self.current_assets = current_assets
        self.fixed_assets = fixed_assets
        self.intangible_assets = intangible_assets

    def total(self) -> float:
        return (
            self.current_assets.total()
            + self.fixed_assets.total()
            + self.intangible_assets.total()
        )


# Liabilities
class CurrentLiabilities:
    def __init__(
        self,
        trade_payables: float,
        accruals: float,
        accrued_income_tax: float,
        deferred_income: float,
        financial_instruments: float,
    ) -> None:
        self.trade_payables = trade_payables
        self.accruals = accruals
        self.accrued_income_tax = accrued_income_tax
        self.deferred_income = deferred_income
        self.financial_instruments = financial_instruments

    def total(self) -> float:
        return sum(
            [
                self.trade_payables,
                self.accruals,
                self.accrued_income_tax,
                self.deferred_income,
                self.financial_instruments,
            ]
        )


class LongTermDebt:
    def __init__(self, term_debt: float) -> None:
        self.term_debt = term_debt

    def total(self) -> float:
        return self.term_debt


class Liabilities:
    def __init__(
        self, current_liabilities: CurrentLiabilities, long_term_debt: LongTermDebt
    ) -> None:
        self.current_liabilities = current_liabilities
        self.long_term_debt = long_term_debt

    def total(self) -> float:
        return self.current_liabilities.total() + self.long_term_debt.total()


# Equity
class Equity:
    def __init__(
        self, retained_earnings: float, reserves: float, intercompany: float
    ) -> None:
        self.retained_earnings = retained_earnings
        self.reserves = reserves
        self.intercompany = intercompany

    def total(self) -> float:
        return sum([self.retained_earnings, self.reserves, self.intercompany])


class BalanceSheet:
    def __init__(
        self, assets: Assets, liabilities: Liabilities, equity: Equity
    ) -> None:
        self.assets = assets
        self.liabilities = liabilities
        self.equity = equity

    def balance(self) -> bool:
        """Assets equals liabilities plus equity (within a dollar)"""
        return abs(
            round(self.assets.total())
            - round((self.liabilities.total() + self.equity.total()))
        )

    def invested_capital(self) -> float:
        return (
            self.assets.current_assets.total()
            - self.liabilities.current_liabilities.total()
            + self.assets.fixed_assets.total()
            + self.assets.intangible_assets.total()
            - self.assets.current_assets.cash
        )


def construct_balance_sheet() -> BalanceSheet:
    # data
    data_ca, data_fa, data_ia = original_assets()
    data_cl, data_ltd = original_liabilities()
    data_eq = original_equity()

    # Assets
    ca = CurrentAssets(**data_ca)
    fa = FixedAssets(**data_fa)
    ia = IntangibleAssets(**data_ia)
    assets = Assets(ca, fa, ia)

    # Liabilities
    cl = CurrentLiabilities(**data_cl)
    ltd = LongTermDebt(**data_ltd)
    liabilities = Liabilities(cl, ltd)

    # Equity
    equity = Equity(**data_eq)

    # Assemble
    balance_sheet = BalanceSheet(assets, liabilities, equity)
    return balance_sheet
