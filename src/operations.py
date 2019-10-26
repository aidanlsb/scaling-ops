from src.data import original_operations


class Productivity:
    def __init__(
        self,
        avg_num_trucks: int,
        total_lifts: int,
        total_m3_collected: int,
        avg_km_per_truck_per_year: float,
        total_tonnes_disposed: float,
        working_days_per_year: int,
        num_customers: int,
    ) -> None:
        self.avg_num_trucks = avg_num_trucks
        self.total_lifts = total_lifts
        self.total_m3_collected = total_m3_collected
        self.avg_km_per_truck_per_year = avg_km_per_truck_per_year
        self.total_tonnes_disposed = total_tonnes_disposed
        self.working_days_per_year = working_days_per_year
        self.num_customers = num_customers

    def avg_density(self) -> float:
        return self.total_tonnes_disposed / self.total_m3_collected

    def lifts_per_truck(self) -> float:
        return self.total_lifts / self.avg_num_trucks


class Truck:
    def __init__(
        self,
        capacity: float,
        fuel_econ_km_l: float,
        fuel_cost_per_l: float,
        maintenance_per_truck_per_year: float,
    ) -> None:
        self.capacity = capacity
        self.fuel_econ_km_l = fuel_econ_km_l
        self.fuel_cost_per_l = fuel_cost_per_l
        self.maintenance_per_truck_per_year = maintenance_per_truck_per_year


class Labor:
    def __init__(self, driver_hourly_wage: float, hours_per_shift: float) -> None:
        self.driver_hourly_wage = driver_hourly_wage
        self.hours_per_shift = hours_per_shift

    def cost_per_shift(self) -> float:
        return self.driver_hourly_wage * self.hours_per_shift


class Operations:
    def __init__(self, productivity: Productivity, truck: Truck, labor: Labor) -> None:
        self.productivity = productivity
        self.truck = truck
        self.labor = labor

    def total_shifts(self) -> float:
        return (
            self.productivity.working_days_per_year * self.productivity.avg_num_trucks
        )

    def lifts_per_shift(self) -> float:
        return self.productivity.total_lifts / self.total_shifts()


def construct_operations() -> Operations:
    # data
    data_productivity, data_truck, data_labor = original_operations()

    productivity = Productivity(**data_productivity)
    truck = Truck(**data_truck)
    labor = Labor(**data_labor)

    operations = Operations(productivity, truck, labor)
    return operations
