import numpy as np
from dataclasses import dataclass


class Operations:
    def __init__(self) -> None:
        self.productivity = Productivity()
        self.truck = Truck()
        self.labor = Labor()

    def lifts_per_truck_day(self) -> float:
        return (
            self.productivity.total_lifts
            / self.productivity.working_days_per_year
            / self.productivity.avg_num_trucks
        )

    def m3_per_customer(self) -> float:
        return self.productivity.total_m3_collected / self.productivity.num_customers

    def avg_vol_per_lift(self) -> float:
        return self.productivity.total_m3_collected / self.productivity.total_lifts

    def avg_tonnes_per_m3(self) -> float:
        return (
            self.productivity.total_tonnes_disposed
            / self.productivity.total_m3_collected
        )

    def driver_cost_per_truck_day(self) -> float:
        return self.labor.driver_hourly_wage * self.labor.hours_per_shift

    def fuel_cost_per_truck_day(self) -> float:
        km_daily = (
            self.productivity.avg_km_per_truck_per_year
            / self.productivity.working_days_per_year
        )
        liters_daily = km_daily / self.truck.fuel_econ_km_l
        return liters_daily * self.truck.fuel_cost_per_l

    def maintenance_cost_per_truck_day(self) -> float:
        cost_per_km = (
            self.truck.maintenance_per_truck_per_year
            / self.productivity.avg_km_per_truck_per_year
        )
        km_daily = (
            self.productivity.avg_km_per_truck_per_year
            / self.productivity.working_days_per_year
        )
        return cost_per_km * km_daily


@dataclass
class Productivity:
    avg_num_trucks: float = 78
    total_lifts: int = 375528
    total_m3_collected: float = 1078787
    avg_km_per_truck_per_year: float = 42971.331458261
    total_tonnes_disposed: float = 97928
    working_days_per_year: int = 330
    num_customers: int = 22519


@dataclass
class Truck:
    capacity: float = 45
    fuel_econ_km_l: float = 1.19
    fuel_cost_per_l: float = 1.95
    maintenance_per_truck_per_year: float = 27764.2831578947


@dataclass
class Labor:
    driver_hourly_wage: float = 15.21
    hours_per_shift: float = 10

