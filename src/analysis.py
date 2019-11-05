import pandas as pd
import altair as alt
from pathlib import Path

from src.model import Model

# Root path for navigation
ROOT = str(Path(__file__).parents[1])


def save_chart(chart: alt.Chart, title: str) -> None:
    charts_path = ROOT + "/charts/"
    chart.save(charts_path + title + ".png", format="png", scale_factor=2.0)


def gen_data() -> pd.DataFrame:
    model = Model()
    # assume their performance slips
    model.inputs.lifts_per_truck_day = 10
    current_customers = model.inputs.num_customers
    customers_3x = current_customers * 3
    n_customers = range(current_customers, customers_3x, 500)
    roics = []
    for n in n_customers:
        model.inputs.num_customers = n
        model.set_trucks()
        r = model.new_roic()
        roics.append(r)

    return pd.DataFrame({"customers": n_customers, "ROIC": roics})


def make_line_chart(df, x, y, title) -> alt.Chart:
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(x=x, y=y)
        .properties(title=title, height=200, width=400)
    )
    return chart


def gen_heatmap_data() -> pd.DataFrame:
    model = Model()
    curr_lpt = int(model.inputs.lifts_per_truck_day * 1000)
    curr_price = int(model.inputs.revenue_per_m3)
    lpt_range = range(curr_lpt - 1000, curr_lpt + 1001, 100)
    price_range = range(curr_price - 5, curr_price + 6, 1)
    roics = []
    prices = []
    lpts = []
    for l in lpt_range:
        for p in price_range:
            model.inputs.lifts_per_truck_day = l / 1000
            model.inputs.revenue_per_m3 = p
            model.set_trucks()
            r = model.new_roic()
            roics.append(r)
            prices.append(p)
            lpts.append(l / 1000)
    df = pd.DataFrame(
        {"roic": roics, "price_per_m3": prices, "lifts_per_truck": lpts}
    ).assign(roic_str=lambda x: x["roic"].apply(lambda y: "{:.1%}".format(y)))
    return df


def make_heatmap(df) -> alt.Chart:
    chart = (
        alt.Chart(df)
        .mark_rect()
        .encode(x="lifts_per_truck:O", y="price_per_m3:O", color="roic")
        .properties(title="ROIC Sensitivity to Lifts per Truck and Price per m3")
    )

    text = (
        alt.Chart(df)
        .mark_text(baseline="middle", fontSize=9)
        .encode(text="roic_str", x="lifts_per_truck:O", y="price_per_m3:O")
    )

    return (chart + text).properties(width=650, height=400)


def make_disposal_data() -> pd.DataFrame:
    model = Model()
    cost_per_tonne = model.cost_per_tonne()


if __name__ == "__main__":
    df = gen_data()
    chart = make_line_chart(
        df,
        "customers",
        "ROIC",
        "ROIC and Customer Growth with Efficiency Deterioration",
    )
    save_chart(chart, "ROIC_and_growth - deteriorate")

    # hm_df = gen_heatmap_data()
    # heatmap = make_heatmap(hm_df)
    # save_chart(heatmap, "Heatmap.png")
