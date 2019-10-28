from typing import Tuple

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

    def decompose_revenue(self) -> Tuple[float]:
        """Break out revenue into drivers"""

        # rev = P*Q
        revenue_per_m3 = self.revenue_per_m3()
        total_m3_collected = self.operations.productivity.total_m3_collected

        # Q = # lifts * Q/lift
        num_lifts = self.operations.productivity.total_lifts
        m3_per_lift = self.operations.productivity.m3_per_lift()

        # Number of lifts = # customers * lifts/customer
        num_cust = self.operations.productivity.num_customers
        lifts_per_cust = num_lifts / num_cust

        # return the drivers
        return num_cust, lifts_per_cust, m3_per_lift, revenue_per_m3

    def decompose_opex(self) -> Tuple[float]:

        # labor
        labor_exp = self.income_statement.opex.labor_subcontract
        driver_labor_exp = self.operations.driver_labor_cost()
        other_labor_exp = labor_exp - driver_labor_exp

        # other operating
        other_opex = self.income_statement.opex.other_opex

        fuel_cost = self.operations.total_fuel_cost()
        maintenance = self.operations.total_maintenance_cost()

        remaining_other_opex = other_opex - (fuel_cost + maintenance)
        # depreciation

        return remaining_other_opex, fuel_cost, maintenance

    def disposal_per_lift(self) -> float:
        return (
            self.income_statement.opex.disposal
            / self.operations.productivity.total_lifts
        )

    def revenue_per_m3(self) -> float:
        return (
            self.income_statement.revenue.operating_revenue
            / self.operations.productivity.total_m3_collected
        )

    def disposal_cost_per_tonne(self) -> float:
        return (
            self.income_statement.opex.disposal
            / self.operations.productivity.total_tonnes_disposed
        )

    def revenue_per_tonne(self) -> float:
        return (
            self.income_statement.revenue.operating_revenue
            / self.operations.productivity.total_tonnes_disposed
        )


def construct_model() -> Model:
    income_statement = construct_income_statement()
    balance_sheet = construct_balance_sheet()
    operations = construct_operations()

    model = Model(income_statement, balance_sheet, operations)
    return model

