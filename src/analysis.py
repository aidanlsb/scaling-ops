from src.model import Model


def lpt_sensitivity(lpt: float) -> float:
    m = Model()
    m.initialize_inputs()
    m.inputs.lifts_per_truck_day = lpt
    return m.new_roic()


def density_sensitivity(dens_increase: float) -> float:
    m = Model()
    m.initialize_inputs()
    m.inputs.avg_tonnes_per_m3 *= 1 + dens_increase
    return m.new_roic()


def growth_effect(cust_increase: float) -> float:
    m = Model()
    m.initialize_inputs()
    m.inputs.num_customers *= 1 + cust_increase
    return m.new_roic()


if __name__ == "__main__":
    roic = growth_effect(0.1)
    print(roic)
