import numpy as np
from typing import Tuple
from dataclasses import dataclass

from src.income_statement import IncomeStatement
from src.balance_sheet import BalanceSheet
from src.operations import Operations


@dataclass
class Inputs:
    """ Model inputs on which to run sensitivities """

    lifts_per_truck_day: float = None
    avg_tonnes_per_m3: float = None
    revenue_per_m3: float = None
    num_customers: float = None


class Model:
    def __init__(self) -> None:
        self.income_statement = IncomeStatement()
        self.balance_sheet = BalanceSheet()
        self.operations = Operations()
        self.inputs = Inputs()

    def current_roic(self) -> float:
        return self.income_statement.nopat() / self.balance_sheet.invested_capital()

    def initialize_inputs(self) -> None:
        """ These inputs are primary drivers of the model and possible levers for the business"""
        self.inputs.lifts_per_truck_day = self.operations.lifts_per_truck_day()
        self.inputs.avg_tonnes_per_m3 = self.operations.avg_tonnes_per_m3()
        self.inputs.revenue_per_m3 = (
            self.income_statement.revenue.operating_revenue
            / self.operations.productivity.total_m3_collected
        )
        self.inputs.num_customers = self.operations.productivity.num_customers

    def total_demand(self) -> float:
        return self.inputs.num_customers * self.operations.m3_per_customer()

    # Allocate non-driver labor cost to truck-days (dispatch, cleaning, etc.)
    def other_labor_cost_per_truck_day(self) -> float:
        total_driver_cost = (
            self.operations.productivity.avg_num_trucks
            * self.operations.driver_cost_per_truck_day()
            * self.operations.productivity.working_days_per_year
        )
        remaining_labor_cost = (
            self.income_statement.opex.labor_subcontract - total_driver_cost
        )
        return (
            remaining_labor_cost
            / self.operations.productivity.avg_num_trucks
            / self.operations.productivity.working_days_per_year
        )

    def other_opex_per_truck_day(self) -> float:
        """Assuming here that the "other operating costs" generally scale with number of trucks"""
        return (
            self.income_statement.opex.other_opex
            / self.operations.productivity.avg_num_trucks
            / self.operations.productivity.working_days_per_year
            - self.operations.maintenance_cost_per_truck_day()
            - self.operations.fuel_cost_per_truck_day()
        )

    def trucks_required(self) -> int:
        daily_demand = (
            self.total_demand() / self.operations.productivity.working_days_per_year
        )
        trucks_required = np.ceil(
            daily_demand
            / (self.operations.avg_vol_per_lift() * self.inputs.lifts_per_truck_day)
        )
        return trucks_required

    def truck_value_and_depreciation(self) -> float:
        truck_cost = 250000
        useful_life = 10
        salvage_value = 25000
        depreciation_per_year = (truck_cost - salvage_value) / useful_life
        # for now calculate for first year post asset purchase
        net_value = truck_cost - depreciation_per_year
        new_trucks_required = (
            self.trucks_required() - self.operations.productivity.avg_num_trucks
        )
        return (
            net_value * new_trucks_required,
            depreciation_per_year * new_trucks_required,
        )

    def collection_cost_per_truck_day(self) -> float:
        driver_cost = self.operations.driver_cost_per_truck_day()
        other_labor = self.other_labor_cost_per_truck_day()
        maintenance = self.operations.maintenance_cost_per_truck_day()
        fuel = self.operations.fuel_cost_per_truck_day()
        other = self.other_opex_per_truck_day()
        return driver_cost + other_labor + maintenance + fuel + other

    def new_collection_cost(self) -> float:
        return (
            self.trucks_required()
            * self.collection_cost_per_truck_day()
            * self.operations.productivity.working_days_per_year
        )

    def cost_per_tonne(self) -> float:
        return (
            self.income_statement.opex.disposal
            / self.operations.productivity.total_tonnes_disposed
        )

    def new_disposal_cost(self) -> float:
        tonnes = self.inputs.avg_tonnes_per_m3 * self.total_demand()
        return tonnes * self.cost_per_tonne()

    def new_operating_cost(self) -> float:
        return (
            self.new_collection_cost()
            + self.new_disposal_cost()
            + self.income_statement.opex.sga
            + self.income_statement.opex.other_inc_exp
            + self.income_statement.opex.management_fees
            + self.income_statement.opex.non_rec_items
        )

    def new_revenue(self) -> float:
        return self.total_demand() * self.inputs.revenue_per_m3

    def new_ebitda(self) -> float:
        return self.new_revenue() - self.new_operating_cost()

    def new_ebit(self) -> float:
        _, new_dep = self.truck_value_and_depreciation()
        return self.new_ebitda() - (self.income_statement.total_da() + new_dep)

    def new_nopat(self, tax_rate=0.21) -> float:
        return self.new_ebit() * (1 - tax_rate)

    def new_ic(self) -> float:
        new_fixed_assets, _ = self.truck_value_and_depreciation()
        return self.balance_sheet.invested_capital() + new_fixed_assets

    def new_roic(self) -> float:
        return self.new_nopat() / self.new_ic()

