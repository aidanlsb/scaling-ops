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
        avg_density: float,
    ) -> None:
        self.avg_num_trucks = avg_num_trucks
        self.total_lifts = total_lifts
        self.total_m3_collected = total_m3_collected
        self.avg_km_per_truck_per_year = avg_km_per_truck_per_year
        self.total_tonnes_disposed = total_tonnes_disposed
        self.working_days_per_year = working_days_per_year
        self.num_customers = num_customers
        self.avg_density = avg_density

    def lifts_per_truck(self) -> float:
        return self.total_lifts / self.avg_num_trucks

    def total_shifts(self, shifts_per_day=1) -> float:
        return self.working_days_per_year * self.avg_num_trucks * shifts_per_day

    def lifts_per_shift(self) -> float:
        return self.total_lifts / self.total_shifts()

    def m3_to_tonnes(self) -> float:
        return self.total_m3_collected * self.avg_density

    def m3_per_lift(self) -> float:
        return self.total_m3_collected / self.total_lifts


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

    def fuel_cost_per_shift(self) -> float:
        km_per_day = (
            self.productivity.avg_km_per_truck_per_year
            / self.productivity.working_days_per_year
        )
        liters_per_day = km_per_day / self.truck.fuel_econ_km_l
        return liters_per_day * self.truck.fuel_cost_per_l

    def maintenance_cost_per_shift(self) -> float:
        return (
            self.truck.maintenance_per_truck_per_year
            / self.productivity.working_days_per_year
        )

    def capacity_utilization(self) -> float:
        total_capacity = (
            self.truck.capacity
            * self.productivity.avg_num_trucks
            * self.productivity.working_days_per_year
        )
        return self.productivity.total_m3_collected / total_capacity


def construct_operations() -> Operations:
    # data
    data_productivity, data_truck, data_labor = original_operations()

    productivity = Productivity(**data_productivity)
    truck = Truck(**data_truck)
    labor = Labor(**data_labor)

    operations = Operations(productivity, truck, labor)
    return operations
