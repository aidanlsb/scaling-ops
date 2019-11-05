import numpy as np
import pandas as pd
import altair as alt
from itertools import accumulate, repeat, islice
from functools import partial
from scipy.optimize import minimize

from src.model import Model
from src.analysis import save_chart


def base_demand() -> float:
    model = Model()
    return model.operations.productivity.num_customers


def calc_cost(new_trucks: int) -> float:
    model = Model()
    return new_trucks * model.inputs.truck_cost


def calc_operating_income(new_trucks: int, num_customers: float) -> float:
    # initialize the model
    model = Model()
    model.inputs.num_customers = num_customers

    # get total trucks, demand, and the trucks needed to serve it
    model.inputs.trucks_total = (
        model.operations.productivity.avg_num_trucks + new_trucks
    )
    trucks_utilized = min([model.trucks_required(), model.inputs.trucks_total])

    available_capacity_per_truck = (
        model.inputs.lifts_per_truck_day
        * model.operations.avg_vol_per_lift()
        * model.operations.productivity.working_days_per_year
    )

    # what demand is met
    served_demand = model.demand_served()
    revenue = served_demand * model.inputs.revenue_per_m3
    disposal_cost = model.new_disposal_cost()

    # depot related costs
    depot_overhead = model.depot_overhead_cost(
        model.inputs.trucks_total
    )  # assume each depot incurs OH
    depot_labor = model.depot_labor_cost(
        trucks_utilized
    )  # but only "active" ones incur labor cost

    # driver costs
    driver_labor = model.driver_labor_cost(trucks_utilized)

    # fuel and maintenance
    fuel = model.fuel_cost(trucks_utilized)
    maintenance = model.maintenance_cost(trucks_utilized)

    return (
        revenue
        - disposal_cost
        - depot_overhead
        - depot_labor
        - driver_labor
        - fuel
        - maintenance
    )


def growth_forecast(base, horizon, growth_rate):
    return [base * (1 + growth_rate) ** y for y in range(1, horizon + 1)]


growth_five_year = partial(growth_forecast, base_demand(), 5)


def calc_profits(new_trucks: int, growth_rate: float, discount_rate: float) -> float:
    demand = growth_five_year(growth_rate)
    profits = [calc_operating_income(new_trucks, di) for di in demand]
    discounted_profits = [
        p / ((1 + discount_rate) ** (i + 1)) for i, p in enumerate(profits)
    ]
    return sum(discounted_profits)


def expected_profits(new_trucks: int, discount_rate: float) -> float:
    cost = calc_cost(new_trucks)
    growth_rates = [0.05, 0.1, 0.15]
    probabilities = [1 / 3, 1 / 3, 1 / 3]
    all_profits = [calc_profits(new_trucks, g, discount_rate) for g in growth_rates]
    pweighted = [p * profit for p, profit in zip(probabilities, all_profits)]
    return sum(pweighted) - cost


def make_data() -> pd.DataFrame:
    num_trucks = range(0, 158 - 78, 2)
    num_trucks_long = []
    discount_rates = [0, 0.05, 0.1, 0.15, 0.2]
    discount_rates_long = []
    profits = []
    for dr in discount_rates:
        for nt in num_trucks:
            p = expected_profits(nt, dr)
            profits.append(p)
            discount_rates_long.append(dr)
            num_trucks_long.append(nt)

    df = pd.DataFrame(
        {
            "num_trucks": num_trucks_long,
            "discount_rate": discount_rates_long,
            "expected_profit": profits,
        }
    )
    return df


def make_chart(df) -> alt.Chart:
    chart_base = (
        alt.Chart(df)
        .mark_line()
        .encode(x="num_trucks", y="expected_profit", color="discount_rate:N")
        .properties(title="Optimal Truck Capacity by Discount Rate")
    )

    df_vline = pd.DataFrame({"num_trucks": [22]})
    chart_line = alt.Chart(df_vline).mark_rule().encode(x="num_trucks")
    return chart_base + chart_line


if __name__ == "__main__":
    df = make_data()
    chart = make_chart(df)
    save_chart(chart, "capacity_chart.png")
