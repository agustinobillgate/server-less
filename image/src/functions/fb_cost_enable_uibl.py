from functions.additional_functions import *
import decimal
from datetime import date
from functions.fb_cost_fill_grid_listbl import fb_cost_fill_grid_listbl
from models import Hoteldpt, Htparam, Waehrung

def fb_cost_enable_uibl(sorttype:int, dept:int, price_type:int):
    d_bezeich = ""
    double_currency = False
    exchg_rate = 0
    amount = 0
    grid_list_list = []
    hoteldpt = htparam = waehrung = None

    grid_list = None

    grid_list_list, Grid_list = create_model("Grid_list", {"artnr":int, "subgroup":int, "bezeich":str, "artnrrezept":int, "unitprice":decimal, "recipecost":decimal, "cpercentage":decimal, "recomcost":decimal, "recomprice":decimal, "next__unit__price":decimal, "next__2nd__price":decimal, "changeddate":date, "users":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal d_bezeich, double_currency, exchg_rate, amount, grid_list_list, hoteldpt, htparam, waehrung


        nonlocal grid_list
        nonlocal grid_list_list
        return {"d_bezeich": d_bezeich, "double_currency": double_currency, "exchg_rate": exchg_rate, "amount": amount, "grid-list": grid_list_list}

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()
    d_bezeich = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam:
        double_currency = htparam.flogical

    if double_currency:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit
    amount, grid_list_list = get_output(fb_cost_fill_grid_listbl(double_currency, sorttype, dept, exchg_rate, price_type))

    return generate_output()