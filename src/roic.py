# Calculate ROIC
def roic(nopat: float, ic: float) -> float:
    return nopat / ic


# IS Items
def nopat(pretax_profit: float, tax_rate: float) -> float:
    return pretax_profit * (1 - tax_rate)


def pretax_profit(
    ebit: float,
    landfill_time_adj: float,
    interest_intercompany: float,
    interest_exp: float,
    interest_inc: float,
    equity_earnings: float,
    fx_adj_div: float,
) -> float:
    return ebit - (
        landfill_time_adj
        + interest_intercompany
        + interest_exp
        + interest_inc
        + equity_earnings
        + fx_adj_div
    )


def ebit(ebitda: float, depreciation: float, intang_amort: float) -> float:
    return ebitda - (depreciation + intang_amort)


def ebitda(
    operating_rev: float,
    labor_subcontract: float,
    disposal: float,
    other_opex: float,
    sga: float,
    other_inc_exp: float,
    management_fee: float,
    non_rec_items: float,
) -> float:
    return operating_rev - (
        labor_subcontract
        + disposal
        + other_opex
        + sga
        + other_inc_exp
        + management_fee
        + non_rec_items
    )


# Balance Sheet Items
def invested_capital(
    current_assets: float,
    current_liabilities: float,
    other_operating_assets: float,
    intang_assets: float,
    cash: float,
) -> float:
    return (
        (current_assets - current_liabilities)
        + other_operating_assets
        + intang_assets
        - cash
    )


if __name__ == "__main__":
    # EBITDA
    OPERATING_REV = 39778917
    LABOR_SUBCONTRACT = 5988550
    DISPOSAL = 6485195
    OTHER_OP = 11788263
    SGA = 2540440
    OTHER_INC_EXP = -320642
    MANAGEMENT_FEE = 1536075
    NON_REC_ITEMS = 0

    exp_ebitda = 11761036
    calc_ebitda = round(
        ebitda(
            OPERATING_REV,
            LABOR_SUBCONTRACT,
            DISPOSAL,
            OTHER_OP,
            SGA,
            OTHER_INC_EXP,
            MANAGEMENT_FEE,
            NON_REC_ITEMS,
        )
    )

    assert abs(exp_ebitda - calc_ebitda) <= 1

    # EBIT
    DEPRECIATION = 4685376
    INTANG_AMORT = 79591

    exp_ebit = 6996070
    calc_ebit = round(ebit(calc_ebitda, DEPRECIATION, INTANG_AMORT))
    assert abs(exp_ebit - calc_ebit) <= 1

    # PRETAX
    LANDFILL_TIME_ADJ = -80826
    INTEREST_INTERCOMPANY = -1357111
    INTEREST_EXP = 157928
    INTEREST_INC = -13328
    EQUITY_EARNINGS = -579288
    FX_ADJ_DIV = -23

    exp_pretax = 8868716
    calc_pretax = round(
        pretax_profit(
            calc_ebit,
            LANDFILL_TIME_ADJ,
            INTEREST_INTERCOMPANY,
            INTEREST_EXP,
            INTEREST_INC,
            EQUITY_EARNINGS,
            FX_ADJ_DIV,
        )
    )

    TAX_RATE = 0.21
    exp_nopat = 7006285
    calc_nopat = round(nopat(calc_pretax, TAX_RATE))
    print(calc_nopat)
    assert abs(exp_nopat - calc_nopat) <= 1

