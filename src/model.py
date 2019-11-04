import numpy as np
from typing import Tuple
from dataclasses import dataclass

from src.income_statement import IncomeStatement
from src.balance_sheet import BalanceSheet
from src.operations import Operations


@dataclass
class Inputs:
    """ Model inputs on which to run sensitivities """

    # Levers
    lifts_per_truck_day: float = None
    avg_tonnes_per_m3: float = None
    revenue_per_m3: float = None
    num_customers: float = None
    trucks_total: int = None

    # assumptions
    allocation_to_collection_unit: float = 0.75
    revenue_landfill: float = None
    truck_cost: float = 250000
    truck_useful_life: float = 10
    truck_salvage_value: float = 25000
    trucks_per_depot: int = 20
    employees_per_depot: int = 5
    depot_overhead_pct = 0.2


class Model:
    def __init__(self) -> None:
        # data provided
        self.income_statement = IncomeStatement()
        self.balance_sheet = BalanceSheet()
        self.operations = Operations()

        # Separate container for levers
        self.inputs = Inputs()
        self.initialize_inputs()

    def initialize_inputs(self) -> None:
        """Initialize the main model drivers using existing data"""
        self.inputs.lifts_per_truck_day = self.operations.lifts_per_truck_day()
        self.inputs.avg_tonnes_per_m3 = self.operations.avg_tonnes_per_m3()
        self.inputs.revenue_per_m3 = (
            self.income_statement.revenue.operating_revenue
            * self.inputs.allocation_to_collection_unit
            / self.operations.productivity.total_m3_collected
        )
        self.inputs.num_customers = self.operations.productivity.num_customers
        # assume that the firm gets the exact trucks needed - will adjust this for the capacity decision modeling
        self.inputs.trucks_total = self.trucks_required()

    def revenue_landfill(self) -> float:
        return self.income_statement.revenue.operating_revenue * (
            1 - self.inputs.allocation_to_collection_unit
        )

    def current_roic(self) -> float:
        """Baseline ROIC"""
        return self.income_statement.nopat() / self.balance_sheet.invested_capital()

    def total_demand(self) -> float:
        """Calculate total demand in volume"""
        return self.inputs.num_customers * self.operations.m3_per_customer()

    def depot_labor_cost_per_truck_day(self) -> float:
        depots_needed = np.ceil(
            self.operations.productivity.avg_num_trucks / self.inputs.trucks_per_depot
        )
        depot_employees = depots_needed * self.inputs.employees_per_depot
        # assume depot employees are paid the same as drivers
        depot_labor_cost = depot_employees * self.operations.driver_cost_per_truck_day()
        return depot_labor_cost / self.operations.productivity.avg_num_trucks

    def depot_overhead_per_truck_day(self) -> float:
        return self.inputs.depot_overhead_pct * self.depot_labor_cost_per_truck_day()

    def landfill_labor_cost(self) -> float:
        """Allocated non-driver labor cost to truck-days as well (dispatch, etc.)"""
        total_driver_cost = (
            self.operations.productivity.avg_num_trucks
            * self.operations.driver_cost_per_truck_day()
            * self.operations.productivity.working_days_per_year
        )

        depot_employee_cost = (
            self.depot_labor_cost_per_truck_day()
            * self.operations.productivity.avg_num_trucks
            * self.operations.productivity.working_days_per_year
        )

        return self.income_statement.opex.labor_subcontract - (
            total_driver_cost + depot_employee_cost
        )

    def other_opex_remaining(self) -> float:
        """ Calculate the portion of "other operating expense" that is attributable to the landfill business
        This should not vary based on inputs other than depot assumptions
        """
        return (
            self.income_statement.opex.other_opex
            - (
                self.operations.maintenance_cost_per_truck_day()
                * self.operations.productivity.avg_num_trucks
                * self.operations.productivity.working_days_per_year
            )
            - (
                self.operations.fuel_cost_per_truck_day()
                * self.operations.productivity.avg_num_trucks
                * self.operations.productivity.working_days_per_year
            )
            - (
                self.depot_overhead_per_truck_day()
                * self.operations.productivity.avg_num_trucks
                * self.operations.productivity.working_days_per_year
            )
        )

    def other_opex_landfill(self) -> float:
        return self.other_opex_remaining() * (
            1 - self.inputs.allocation_to_collection_unit
        )

    def other_opex_collections_per_truck_day(self) -> float:
        return (
            (self.other_opex_remaining() - self.other_opex_landfill())
            / self.operations.productivity.avg_num_trucks
            / self.operations.productivity.working_days_per_year
        )

    def trucks_required(self) -> int:
        """Calculate the trucks required to service the demand given current lifts per truck"""
        daily_demand = (
            self.total_demand() / self.operations.productivity.working_days_per_year
        )
        trucks_required = np.ceil(
            daily_demand
            / (self.operations.avg_vol_per_lift() * self.inputs.lifts_per_truck_day)
        )
        return trucks_required

    def truck_value_and_depreciation(self) -> float:
        """Need to calculate net asset value and associated depreciation for trucks"""
        depreciation_per_year = (
            self.inputs.truck_cost - self.inputs.truck_salvage_value
        ) / self.inputs.truck_useful_life
        # for now calculate for first year post asset purchase
        net_value = self.inputs.truck_cost - depreciation_per_year
        new_trucks_added = (
            self.inputs.trucks_total - self.operations.productivity.avg_num_trucks
        )
        return (net_value * new_trucks_added, depreciation_per_year * new_trucks_added)

    def cost_per_tonne(self) -> float:
        return (
            self.income_statement.opex.disposal
            / self.operations.productivity.total_tonnes_disposed
        )

    def new_disposal_cost(self) -> float:
        tonnes = self.inputs.avg_tonnes_per_m3 * self.total_demand()
        return tonnes * self.cost_per_tonne()

    def new_labor_subcontract(self) -> float:
        driver_labor = (
            self.operations.driver_cost_per_truck_day()
            * self.inputs.trucks_total
            * self.operations.productivity.working_days_per_year
        )
        depot_labor = (
            self.depot_labor_cost_per_truck_day()
            * self.inputs.trucks_total
            * self.operations.productivity.working_days_per_year
        )
        landfill_labor = self.landfill_labor_cost()
        return driver_labor + depot_labor + landfill_labor

    def new_other_operating_cost(self) -> float:
        fuel = (
            self.operations.fuel_cost_per_truck_day()
            * self.inputs.trucks_total
            * self.operations.productivity.working_days_per_year
        )
        maintenance = (
            self.operations.maintenance_cost_per_truck_day()
            * self.inputs.trucks_total
            * self.operations.productivity.working_days_per_year
        )

        depot_overhead = (
            self.depot_overhead_per_truck_day()
            * self.inputs.trucks_total
            * self.operations.productivity.working_days_per_year
        )
        other_opex = (
            self.other_opex_collections_per_truck_day()
            * self.inputs.trucks_total
            * self.operations.productivity.working_days_per_year
            + self.other_opex_landfill()
        )

        return fuel + maintenance + depot_overhead + other_opex

    def new_operating_cost(self) -> float:
        return (
            self.new_collection_cost()
            + self.new_disposal_cost()
            + self.landfill_labor_cost()
            + self.other_opex_landfill()
            + self.income_statement.opex.sga
            + self.income_statement.opex.other_inc_exp
            + self.income_statement.opex.management_fees
            + self.income_statement.opex.non_rec_items
        )

    def new_revenue(self) -> float:
        revenue_collections = self.total_demand() * self.inputs.revenue_per_m3
        return revenue_collections + self.revenue_landfill()

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

