import pandas as pd
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
        """Get to cost-per-lift that depends on lifts-per-shift"""

        # labor cost per lift is driver labor + other (dispatch, management, etc.)
        driver_labor_cost_per_shift = self.operations.labor.cost_per_shift()

        other_labor_cost_per_shift = (
            self.income_statement.opex.labor_subcontract
            / self.operations.productivity.total_shifts()
            - driver_labor_cost_per_shift
        )

        # other operating
        fuel_cost_per_shift = self.operations.fuel_cost_per_shift()
        maintenance_per_shift = self.operations.maintenance_cost_per_shift()
        other_opex_per_shift = (
            self.income_statement.opex.other_opex
            / self.operations.productivity.total_shifts()
            - fuel_cost_per_shift
            - maintenance_per_shift_per_shift
        )

        # lifts per shift
        lifts_per_shift = self.operations.productivity.lifts_per_shift()

        driver_labor_cost_per_lift = driver_labor_cost_per_shift / lifts_per_shift
        other_labor_cost_per_lift = other_labor_cost_per_shift / lifts_per_shift
        fuel_cost_per_lift = fuel_cost_per_shift / lifts_per_shift
        maintenance_per_lift = maintenance_per_shift / lifts_per_shift
        other_opex_per_lift = other_labor_cost_per_shift / lifts_per_shift

        # disposal
        disposal_cost_per_tonne = (
            self.income_statement.opex.disposal
            / self.operations.productivity.total_tonnes_disposed
        )
        disposal_cost_per_m3 = (
            disposal_cost_per_tonne / self.operations.productivity.avg_density
        )
        disposal_cost_per_lift = (
            disposal_cost_per_m3 * self.operations.productivity.m3_per_lift()
        )

        return (
            driver_labor_cost_per_lift,
            other_labor_cost_per_lift,
            fuel_cost_per_lift,
            maintenance_per_lift,
            other_opex_per_lift,
            disposal_cost_per_lift,
        )


def construct_model() -> Model:
    income_statement = construct_income_statement()
    balance_sheet = construct_balance_sheet()
    operations = construct_operations()

    model = Model(income_statement, balance_sheet, operations)
    return model

