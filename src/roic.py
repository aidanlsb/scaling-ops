from src.income_statement import IncomeStatement, construct_income_statement
from src.balance_sheet import BalanceSheet, construct_balance_sheet
from src.operations import Operations, construct_operations


class Model:
    def __init__(
        self,
        income_statement: IncomeStatement,
        balance_sheet: BalanceSheet,
        operations: Operations,
    ) -> None:
        self.income_statement = income_statement
        self.balance_sheet = balance_sheet
        self.operations = operations

    def roic(self) -> float:
        nopat = self.income_statement.nopat()
        invested_capital = self.balance_sheet.invested_capital()
        return nopat / invested_capital

    def revenue_per_lift(self) -> float:
        return (
            self.income_statement.revenue.operating_revenue
            / self.operations.productivity.total_lifts
        )

    """Need to complete"""

    def cost_per_lift(self) -> float:
        return


def construct_model() -> Model:
    income_statement = construct_income_statement()
    balance_sheet = construct_balance_sheet()
    operations = construct_operations()

    model = Model(income_statement, balance_sheet, operations)
    return model
