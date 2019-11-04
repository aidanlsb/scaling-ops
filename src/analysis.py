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
    current_customers = model.inputs.num_customers
    customers_3x = current_customers * 3
    n_customers = range(current_customers, customers_3x, 5000)
    roics = []
    for n in n_customers:
        model.inputs.num_customers = n
        r = model.new_roic()
        roics.append(r)

    return pd.DataFrame({"customers": n_customers, "ROIC": roics})


def make_line_chart(df, x, y, title) -> alt.Chart:
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(x=x, y=y)
        .properties(title=title, height=300, width=400)
    )
    return chart


if __name__ == "__main__":
    df = gen_data()
    chart = make_line_chart(df, "customers", "ROIC", "ROIC and Customer Growth")
    save_chart(chart, "ROIC_and_growth")
