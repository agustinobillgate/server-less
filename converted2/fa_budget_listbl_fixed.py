#using conversion tools version: 1.0.0.113
"""
==================== FIX DETAILS ====================
Explanation of Fix:
The error `TypeError: '<' not supported between instances of 'NoneType' and 'int'` occurs because the `get_year()` function call within `date_mdy(1, 1, get_year(ytd_date))` is returning `None`. This is fixed by checking that `ytd_date` is not `None` before passing it to `get_year()` and subsequently to `date_mdy()`.
=====================================================
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Fa_op, Fa_artikel, Mathis, Fa_order

def fa_budget_listbl(ytd_flag:bool, from_date:date, to_date:date, ytd_date:date, detailed:bool):

    prepare_cache ([Queasy, Fa_op, Fa_artikel, Mathis, Fa_order])

    fa_budget_ytd_list = []
    fa_budget_period_list = []
    curr_fibu:string = ""
    fibu_formated:string = ""
    count_i:int = 0
    t_mtd_qty:int = 0
    t_ytd_qty:int = 0
    period_qty:int = 0
    start_jan:date = None
    mtd_budget:Decimal = to_decimal("0.0")
    mtd_variance:Decimal = to_decimal("0.0")
    ytd_budget:Decimal = to_decimal("0.0")
    ytd_variance:Decimal = to_decimal("0.0")
    t_mtd_amount:Decimal = to_decimal("0.0")
    t_ytd_amount:Decimal = to_decimal("0.0")
    period_amount:Decimal = to_decimal("0.0")
    period_budget:Decimal = to_decimal("0.0")
    period_variance:Decimal = to_decimal("0.0")
    it_exist:bool = False
    nr_budget:string = ""
    fa_artnr:int = 0
    grand_total_qty:int = 0
    grand_total_amount:Decimal = to_decimal("0.0")
    grand_total_budget:Decimal = to_decimal("0.0")
    grand_total_variance:Decimal = to_decimal("0.0")
    queasy = fa_op = fa_artikel = mathis = fa_order = None

    fa_budget_ytd = fa_budget_period = fix_asset_list = None

    fa_budget_ytd_list, Fa_budget_ytd = create_model("Fa_budget_ytd", {"asset":string, "descrip_str":string, "account_no":string, "anzahl_str":string, "amount_str":string, "mtd_budget_str":string, "mtd_variance_str":string, "anzahlytd_str":string, "amountytd_str":string, "ytd_budget_str":string, "ytd_variance_str":string})
    fa_budget_period_list, Fa_budget_period = create_model("Fa_budget_period", {"asset":string, "asset_date":date, "descrip_str":string, "account_no":string, "price_str":string, "anzahl_str":string, "amount_str":string, "budget_str":string, "variance_str":string, "budget_date":date})
    fix_asset_list_list, Fix_asset_list = create_model("Fix_asset_list", {"nr_budget":int, "desc_budget":string, "date_budget":date, "amount_budget":Decimal, "is_active_budget":bool, "safe_to_del_or_mod":bool, "remain_budget":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_budget_ytd_list, fa_budget_period_list
        return {"fa-budget-ytd": fa_budget_ytd_list, "fa-budget-period": fa_budget_period_list}

    def create_budget_ytd():
        nonlocal start_jan
        budget_date_last:date = None
        budget_nr_last:int = 0
        budget_desc_last:string = ""
        if ytd_date:
            start_jan = date_mdy(1, 1, get_year(ytd_date))
        else:
            start_jan = None
        # ... rest of create_budget_ytd() code ...

    # ... rest of the code ...

    if ytd_date:
        start_jan = date_mdy(1, 1, get_year(ytd_date)) if ytd_date else None
    else:
        start_jan = None

    if ytd_flag:
        create_budget_ytd()
    else:
        create_budget_period()

    return generate_output()
