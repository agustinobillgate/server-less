#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Waehrung

def ts_multicash_cal_payamountbl(bezeich:string, exrate:Decimal, amt:Decimal):
    art_exrate = to_decimal("0.0")
    amount = to_decimal("0.0")
    paid = to_decimal("0.0")
    lpaid = to_decimal("0.0")
    change = to_decimal("0.0")
    lchange = to_decimal("0.0")
    waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_exrate, amount, paid, lpaid, change, lchange, waehrung
        nonlocal bezeich, exrate, amt

        return {"art_exrate": art_exrate, "amount": amount, "paid": paid, "lpaid": lpaid, "change": change, "lchange": lchange}


    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, bezeich)]})
    art_exrate =  to_decimal(exrate)
    amount = to_decimal(round(amt / exrate , 2))
    paid =  - to_decimal(amount)
    lpaid =  - to_decimal(amt)
    change =  to_decimal("0")
    lchange =  to_decimal("0")

    return generate_output()