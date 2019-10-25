from typing import Dict


class IncomeStatement:
    def __init__(
        self,
        operating_rev: float,
        labor_subcontract: float,
        disposal: float,
        other_op: float,
        sga: float,
        other_inc_exp: float,
        management_fee: float,
        non_rec_items: float,
        depreciation: float,
        intang_amort: float,
        landfill_time_adj: float,
        interest_intercompany: float,
        interest_exp: float,
        interest_inc: float,
        equity_earnings: float,
        fx_adj_div: float,
    ) -> None:
        self.operating_rev = operating_rev
        self.labor_subcontract = labor_subcontract
        self.disposal = disposal
        self.other_op = other_op
        self.sga = sga
        self.other_inc_exp = other_inc_exp
        self.management_fee = management_fee
        self.non_rec_items = non_rec_items
        self.depreciation = depreciation
        self.intang_amort = intang_amort
        self.landfill_time_adj = landfill_time_adj
        self.interest_intercompany = interest_intercompany
        self.interest_exp = interest_exp
        self.interest_inc = interest_inc
        self.equity_earnings = equity_earnings
        self.fx_adj_div = fx_adj_div

    def calc_opex(self) -> float:
        return sum(
            [
                self.labor_subcontract,
                self.disposal,
                self.other_op,
                self.sga,
                self.other_inc_exp,
                self.management_fee,
                self.non_rec_items,
            ]
        )

    def calc_ebitda(self) -> float:
        opex = self.calc_opex()
        return self.operating_rev - opex

    def calc_ebit(self) -> float:
        ebitda = self.calc_ebitda()
        return ebitda - (self.depreciation + self.intang_amort)

    def calc_nopat(self, tax_rate=0.21) -> float:
        ebit = self.calc_ebit()
        return ebit * (1 - tax_rate)


def current_is() -> Dict:
    return {
        "operating_rev": 39778917,
        "labor_subcontract": 5988550,
        "disposal": 6485195,
        "other_op": 11788263,
        "sga": 2540440,
        "other_inc_exp": -320642,
        "management_fee": 1536075,
        "non_rec_items": 0,
        "depreciation": 4685376,
        "intang_amort": 79591,
        "landfill_time_adj": -80826,
        "interest_intercompany": -1357111,
        "interest_exp": 157928,
        "interest_inc": -13328,
        "equity_earnings": -579288,
        "fx_adj_div": -23,
    }


if __name__ == "__main__":
    curr_is = current_is()
    i_s = IncomeStatement(**curr_is)
    print(i_s.calc_nopat())
