from dataclasses import dataclass


class IncomeStatement:
    def __init__(self) -> None:
        self.revenue = Revenue()
        self.opex = OpEx()
        self.da = DA()

    def total_opex(self) -> float:
        return sum(
            [
                self.opex.labor_subcontract,
                self.opex.disposal,
                self.opex.other_opex,
                self.opex.sga,
                self.opex.other_inc_exp,
                self.opex.management_fees,
                self.opex.non_rec_items,
            ]
        )

    def total_da(self) -> float:
        return sum([self.da.depreciation, self.da.amortization])

    def ebitda(self) -> float:
        return self.revenue.operating_revenue - self.total_opex()

    def ebit(self) -> float:
        return self.ebitda() - self.total_da()

    def nopat(self, tax_rate=0.21) -> float:
        return self.ebit() * (1 - tax_rate)


@dataclass
class Revenue:
    operating_revenue: float = 39778916.847903


@dataclass
class OpEx:
    labor_subcontract = 5988550.3346616
    disposal = 6485195.3164922
    other_opex = 11788263.327227
    sga = 2540439.5069915
    other_inc_exp = -320642.23237
    management_fees = 1536074.53672
    non_rec_items = 0


@dataclass
class DA:
    depreciation = 4685375.9208466
    amortization = 79591.293499997

