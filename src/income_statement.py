from src.data import original_revenue, original_expenses


class Revenue:
    def __init__(self, operating_revenue: float) -> None:
        self.operating_revenue = operating_revenue

    def total(self) -> float:
        return self.operating_revenue


class OpEx:
    def __init__(
        self,
        labor_subcontract: float,
        disposal: float,
        other_opex: float,
        sga: float,
        other_inc_exp: float,
        management_fees: float,
        non_rec_items: float,
    ) -> None:
        self.labor_subcontract = labor_subcontract
        self.disposal = disposal
        self.other_opex = other_opex
        self.sga = sga
        self.other_inc_exp = other_inc_exp
        self.management_fees = management_fees
        self.non_rec_items = non_rec_items

    def total(self) -> float:
        return sum(
            [
                self.labor_subcontract,
                self.disposal,
                self.other_opex,
                self.sga,
                self.other_inc_exp,
                self.management_fees,
                self.non_rec_items,
            ]
        )


class DA:
    def __init__(self, depreciation: float, amortization: float) -> None:
        self.depreciation = depreciation
        self.amortization = amortization

    def total(self) -> float:
        return self.depreciation + self.amortization


class IncomeStatement:
    def __init__(self, revenue: Revenue, opex: OpEx, da: DA) -> None:
        self.revenue = revenue
        self.opex = opex
        self.da = da

    def ebitda(self) -> float:
        return self.revenue.total() - self.opex.total()

    def ebit(self) -> float:
        return self.ebitda() - self.da.total()

    def nopat(self, tax_rate=0.21) -> float:
        return self.ebit() * (1 - tax_rate)


def construct_income_statement() -> IncomeStatement:
    data_rev = original_revenue()
    data_opex, data_da = original_expenses()

    rev = Revenue(**data_rev)
    opex = OpEx(**data_opex)
    da = DA(**data_da)

    income_statement = IncomeStatement(rev, opex, da)

    return income_statement
