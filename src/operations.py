from dataclasses import dataclass


class Operations:
    def __init__(self) -> None:
        self.productivity = Productivity()
        self.truck = Truck()
        self.labor = Labor()

    def driver_cost_per_shift(self):
        return self.labor.driver_hourly_wage * self.labor.hours_per_shift


@dataclass
class Productivity:
    avg_num_trucks: float = 78
    total_lifts: int = 375528
    total_m3_collected: float = 1078787
    avg_km_per_truck_per_year: float = 42971.331458261
    total_tonnes_disposed: float = 97928
    working_days_per_year: int = 330
    num_customers: int = 22519
    avg_density: float = 0.0907767756622898


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

