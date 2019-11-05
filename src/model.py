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
    ppe_pct_depot = 0.1
    revenue_landfill: float = None
    truck_cost: float = 200000
    truck_useful_life: float = 5
    truck_salvage_value: float = 25000
    trucks_per_depot: int = 20
    employees_per_depot: int = 10
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

    def set_trucks(self) -> None:
        # assume that the firm gets the exact trucks needed - will adjust this for the capacity decision modeling
        self.inputs.trucks_total = self.trucks_required()

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

    def total_demand(self) -> float:
        """Calculate total demand in volume"""
        return self.inputs.num_customers * self.operations.m3_per_customer()

    """
    Calculate components of labor & subcontractor expense
    """

    def driver_labor_cost(self, num_trucks: int) -> float:
        return (
            self.operations.driver_cost_per_truck_day()
            * self.operations.productivity.working_days_per_year
            * num_trucks
        )

    def depot_labor_cost(self, num_trucks: int) -> float:
        """ Calculate the depot labor cost based on number of trucks and assumptions """
        depots_needed = np.ceil(num_trucks / self.inputs.trucks_per_depot)
        total_depot_employees = self.inputs.employees_per_depot * depots_needed
        return (
            total_depot_employees
            * self.operations.productivity.working_days_per_year
            * self.operations.driver_cost_per_truck_day()
        )

    def landfill_labor_cost(self) -> float:
        # total driver cost using data given (not inputs)
        driver_labor_cost = self.driver_labor_cost(
            self.operations.productivity.avg_num_trucks
        )
        # total depot employee cost using data given (not inputs)
        depot_labor_cost = self.depot_labor_cost(
            self.operations.productivity.avg_num_trucks
        )

        # assume that landfill is the remaining portion
        return self.income_statement.opex.labor_subcontract - (
            driver_labor_cost + depot_labor_cost
        )

    def new_labor_subcontract(self) -> float:
        """ Calculate the new labor expense using the per-day 
        values for depot and drivers, and the lump sum for landfill
        """
        driver_labor_cost = self.driver_labor_cost(self.inputs.trucks_total)
        depot_labor_cost = self.depot_labor_cost(self.inputs.trucks_total)
        landfill_labor_cost = self.landfill_labor_cost()
        return driver_labor_cost + depot_labor_cost + landfill_labor_cost

    """
    Calculate the disposal cost
    """

    def cost_per_tonne(self) -> float:
        return (
            self.income_statement.opex.disposal
            / self.operations.productivity.total_tonnes_disposed
        )

    def new_disposal_cost(self) -> float:
        tonnes = (
            self.inputs.avg_tonnes_per_m3 * self.demand_served()
        )  # will need to adjust this to demand served
        return tonnes * self.cost_per_tonne()

    """
    Calculate the other operating costs
    """

    def depot_overhead_cost(self, num_trucks: int) -> float:
        return self.inputs.depot_overhead_pct * self.depot_labor_cost(num_trucks)

    def maintenance_cost(self, num_trucks: int) -> float:
        return self.operations.truck.maintenance_per_truck_per_year * num_trucks

    def fuel_cost(self, num_trucks: int) -> float:
        return (
            self.operations.productivity.avg_km_per_truck_per_year
            / self.operations.truck.fuel_econ_km_l
            * self.operations.truck.fuel_cost_per_l
            * num_trucks
        )

    def other_opex_remaining(self) -> float:
        """ Calculate the portion of "other operating expense" that is attributable to the landfill business
        This should not vary based on inputs other than depot assumptions
        """
        return (
            self.income_statement.opex.other_opex
            - self.depot_overhead_cost(self.operations.productivity.avg_num_trucks)
            - self.maintenance_cost(self.operations.productivity.avg_num_trucks)
            - self.fuel_cost(self.operations.productivity.avg_num_trucks)
        )

    def new_other_operating_cost(self) -> float:
        fuel = self.fuel_cost(self.inputs.trucks_total)
        maintenance = self.maintenance_cost(self.inputs.trucks_total)
        depot_overhead = self.depot_overhead_cost(self.inputs.trucks_total)
        other_opex_landfill = self.other_opex_remaining()
        return fuel + maintenance + depot_overhead + other_opex_landfill

    def new_sga(self) -> float:
        """SG&A presumably grows with the business, assume grows at 75% the rate of demand"""
        increase_factor = (
            self.total_demand() / self.operations.productivity.total_m3_collected - 1
        )
        increase_factor *= 0.75
        return self.income_statement.opex.sga * (1 + increase_factor)

    """ Put pieces together to get opex based on inputs """

    def new_operating_cost(self) -> float:
        return (
            self.new_labor_subcontract()
            + self.new_disposal_cost()
            + self.new_other_operating_cost()
            + self.new_sga()
            + self.income_statement.opex.other_inc_exp
            + self.income_statement.opex.management_fees
            + self.income_statement.opex.non_rec_items
        )

    """ Calculate depreciation based on fleet size """

    def non_fleet_depreciation(self) -> float:
        fleet_dep = (
            (self.inputs.truck_cost - self.inputs.truck_salvage_value)
            / self.inputs.truck_useful_life
            * self.operations.productivity.avg_num_trucks
        )
        return self.income_statement.da.depreciation - fleet_dep

    def depreciation_exp_per_truck(self) -> float:
        return (
            self.inputs.truck_cost - self.inputs.truck_salvage_value
        ) / self.inputs.truck_useful_life

    def new_depreciation(self) -> float:
        return self.non_fleet_depreciation() + self.depreciation_exp_per_truck() * max(
            [self.inputs.trucks_total, self.operations.productivity.avg_num_trucks]
        )

    def new_fixed_assets(self) -> float:
        """ Adjust existing fixed asset base to account for changes in number of trucks & depots
        Scale up existing fixed assets by the ratio of new trucks to old trucks
        """
        old_depot_ppe = (
            self.balance_sheet.assets.of_which_pe * self.inputs.ppe_pct_depot
        )
        old_fleet_net_value = self.balance_sheet.assets.of_which_fleet

        adjustment_factor = (
            self.inputs.trucks_total / self.operations.productivity.avg_num_trucks - 1
        )
        incremental_depot = old_depot_ppe * adjustment_factor
        incremental_fleet = old_fleet_net_value * adjustment_factor
        return incremental_fleet + incremental_fleet

    def revenue_landfill(self) -> float:
        """ Pull out the revenue attributable to the landfill operations """
        return self.income_statement.revenue.operating_revenue * (
            1 - self.inputs.allocation_to_collection_unit
        )

    def current_roic(self) -> float:
        """Baseline ROIC"""
        return self.income_statement.nopat() / self.balance_sheet.invested_capital()

    def demand_served(self) -> float:
        fleet_capacity_accessible = (
            self.inputs.trucks_total
            * self.inputs.lifts_per_truck_day
            * self.operations.avg_vol_per_lift()
            * self.operations.productivity.working_days_per_year
        )
        demand_served = min([self.total_demand(), fleet_capacity_accessible])
        return demand_served

    def new_revenue(self) -> float:
        """ Assume that lifts-per-truck (or per-truck capacity utilization) doesn't change in response to demand"""
        revenue_collections = self.demand_served() * self.inputs.revenue_per_m3
        return revenue_collections + self.revenue_landfill()

    def new_ebitda(self) -> float:
        return self.new_revenue() - self.new_operating_cost()

    def new_ebit(self) -> float:
        return self.new_ebitda() - (
            self.income_statement.da.amortization + self.new_depreciation()
        )

    def new_nopat(self, tax_rate=0.21) -> float:
        return self.new_ebit() * (1 - tax_rate)

    def new_ic(self) -> float:
        return self.balance_sheet.invested_capital() + self.new_fixed_assets()

    def new_roic(self) -> float:
        return self.new_nopat() / self.new_ic()

