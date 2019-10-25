class Item:
    def __init__(
        self,
        type:str, 
        desc:str, 
        amount: float
    ) -> None:
        self.desc = desc
        self.amount = amount
    
    def update(self, delta: float) -> None:
        self.amount += delta

    



class BalanceSheet:
    def __init__(
        self,
        cash: float,
        accounts_receivable: float,
        bad_debts_provision: float,
        properties_intended_for_sale: float,
        other_receivables: float,

        
    ) -> None:
