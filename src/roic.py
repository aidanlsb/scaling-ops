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

    def total_labor_cost(self) -> float:
        """
        total labor cost for waste collection is cost per shift * number of shifts in a year
        number of shifts in a year is assumed to be number of trucks * days worked in a year
        """
        return (
            self.operations.productivity.avg_num_trucks
            * self.operations.productivity.working_days_per_year
            * self.operations.labor.cost_per_shift()
        )


def construct_model() -> Model:
    income_statement = construct_income_statement()
    balance_sheet = construct_balance_sheet()
    operations = construct_operations()

    model = Model(income_statement, balance_sheet, operations)
    return model
