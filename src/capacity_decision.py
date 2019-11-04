from itertools import accumulate, repeat, islice
from functools import partial
from src.model import Model

# trucks required to meet given level of demand assuming lifts per truck don't change
def calc_trucks_required(num_customers: float) -> int:
    model = Model()
    model.inputs.num_customers = num_customers
    return model.trucks_required()


def lost_revenue(num_customers: float, num_trucks: int) -> float:
    model = Model()
    model.inputs.num_customers = num_customers
    total_demand = model.total_demand()
    total_capacity = (
        num_trucks
        * model.inputs.lifts_per_truck_day
        * model.operations.avg_vol_per_lift()
        * model.operations.productivity.working_days_per_year
    )
    demand_met = min(total_demand, total_capacity)
    demand_unmet = total_demand - demand_met
    return demand_unmet * model.inputs.revenue_per_m3


truck_cost = model.inputs.truck_cost
salvage_value = model.inputs.truck_salvage_value
useful_life = model.inputs.truck_useful_life


def growth_forecast(base, horizon, growth_rate):
    return [base * (1 + growth_rate) ** y for y in range(1, horizon + 1)]


growth_five_year = partial(growth_forecast, base_demand, 5)

# calculate number of trucks required to meet a given level of demand


# calculate the contribution for utilized trucks (less labor cost)


if __name__ == "__main__":
    f = growth_five_year(0.1)
    print(f)
