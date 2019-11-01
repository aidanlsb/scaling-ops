import pandas as pd
from typing import Tuple

from src.income_statement import IncomeStatement
from src.balance_sheet import BalanceSheet
from src.operations import Operations


class Model:
    def __init__(
        self,
    ) -> None:
        self.income_statement = IncomeStatement()
        self.balance_sheet = BalanceSheet()
        self.operations = Operations()

        # Drivers - Revenue Side

        # Drivers - Cost side
        self.

    def roic(self) -> float:
        return self.income_statement.nopat() / self.balance_sheet.invested_capital()

    def decompose_revenue(self) -> Tuple[float]:
        """Break out revenue into drivers"""
        # rev = P*Q
        rev_per_m3 = (
            self.income_statement.revenue.operating_revenue
            / self.operations.productivity.total_m3_collected
        )

        # Q = # customers * M3/customers
        m3_per_cust = (
            self.operations.productivity.total_m3_collected
            / self.operations.productivity.num_customers
        )

        # return the drivers
        return rev_per_m3, m3_per_cust

    def decompose_opex(self) -> Tuple[float]:
        """Get to cost-per-lift that depends on lifts-per-shift"""

        # start with total demand

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
            - maintenance_per_shift
        )

        # lifts per shift
        lifts_per_shift = self.operations.productivity.lifts_per_shift()

        driver_labor_cost_per_lift = driver_labor_cost_per_shift / lifts_per_shift
        other_labor_cost_per_lift = other_labor_cost_per_shift / lifts_per_shift
        fuel_cost_per_lift = fuel_cost_per_shift / lifts_per_shift
        maintenance_per_lift = maintenance_per_shift / lifts_per_shift
        other_opex_per_lift = other_opex_per_shift / lifts_per_shift

        # disposal
        disposal_cost_per_tonne = (
            self.income_statement.opex.disposal
            / self.operations.productivity.total_tonnes_disposed
        )
        tonnes_per_lift = (
            self.operations.productivity.total_tonnes_disposed
            / self.operations.productivity.total_lifts
        )
        avg_density = self.operations.productivity.avg_density
        m3_per_lift = tonnes_per_lift / avg_density
        customer_utilization = self.operations.capacity_utilization()
        m3_serviced_per_lift = m3_per_lift / customer_utilization

        return (
            lifts_per_shift,
            driver_labor_cost_per_lift,
            other_labor_cost_per_lift,
            fuel_cost_per_lift,
            maintenance_per_lift,
            other_opex_per_lift,
            disposal_cost_per_tonne,
            avg_density,
            customer_utilization,
            m3_serviced_per_lift,
        )


def construct_model() -> Model:
    income_statement = construct_income_statement()
    balance_sheet = construct_balance_sheet()
    operations = construct_operations()

    model = Model(income_statement, balance_sheet, operations)
    return model

