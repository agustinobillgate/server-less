#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fb_cost_fill_grid_listbl import fb_cost_fill_grid_listbl
from models import Hoteldpt, Htparam, Waehrung

def fb_cost_enable_uibl(sorttype:int, dept:int, price_type:int):

    prepare_cache ([Hoteldpt, Htparam, Waehrung])

    d_bezeich = ""
    double_currency = False
    exchg_rate = to_decimal("0.0")
    amount = to_decimal("0.0")
    grid_list_list = []
    hoteldpt = htparam = waehrung = None

    grid_list = None

    grid_list_list, Grid_list = create_model("Grid_list", {"artnr":int, "subgroup":int, "bezeich":string, "artnrrezept":int, "unitprice":Decimal, "recipecost":Decimal, "cpercentage":Decimal, "recomcost":Decimal, "recomprice":Decimal, "next__unit__price":Decimal, "next__2nd__price":Decimal, "changeddate":date, "users":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal d_bezeich, double_currency, exchg_rate, amount, grid_list_list, hoteldpt, htparam, waehrung
        nonlocal sorttype, dept, price_type


        nonlocal grid_list
        nonlocal grid_list_list

        return {"d_bezeich": d_bezeich, "double_currency": double_currency, "exchg_rate": exchg_rate, "amount": amount, "grid-list": grid_list_list}

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})
    d_bezeich = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam:
        double_currency = htparam.flogical

    if double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    amount, grid_list_list = get_output(fb_cost_fill_grid_listbl(double_currency, sorttype, dept, exchg_rate, price_type))

    return generate_output()