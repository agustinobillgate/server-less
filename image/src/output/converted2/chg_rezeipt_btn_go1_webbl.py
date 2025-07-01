#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, Bediener, Res_history, Queasy

def chg_rezeipt_btn_go1_webbl(rec_id:int, katnr:int, portion:int, h_bezeich:string, katbezeich:string, user_init:string, cost_percent:Decimal, poten_sell_price:Decimal):

    prepare_cache ([H_rezept, Bediener, Res_history, Queasy])

    vlog:bool = False
    h_artnr:int = 0
    h_rezept = bediener = res_history = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal vlog, h_artnr, h_rezept, bediener, res_history, queasy
        nonlocal rec_id, katnr, portion, h_bezeich, katbezeich, user_init, cost_percent, poten_sell_price

        return {}


    h_rezept = get_cache (H_rezept, {"_recid": [(eq, rec_id)]})
    h_artnr = h_rezept.artnrrezept
    pass

    if h_rezept.kategorie != katnr or h_rezept.portion != portion or to_string(h_bezeich, "x(24)") != substring(h_rezept.bezeich, 0, 24):
        vlog = True

    if vlog:

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Change Recipe"
        res_history.aenderung = "Modify Recipe " + to_string(h_rezept.artnrrezept) +\
                "(" + substring(h_rezept.bezeich, 0, 24) + ")" + " => "

        if h_rezept.kategorie != katnr:
            res_history.aenderung = res_history.aenderung + "CatNo " + to_string(h_rezept.kategorie) + " to " + to_string(katnr) + ";"

        elif h_rezept.portion != portion:
            res_history.aenderung = res_history.aenderung + "portion " + to_string(h_rezept.portion) + " to " + to_string(portion) + ";"

        elif to_string(h_bezeich, "x(24)") != substring(h_rezept.bezeich, 0, 24):
            res_history.aenderung = res_history.aenderung + "Description " + substring(h_rezept.bezeich, 0, 24) + " to " + to_string(h_bezeich, "x(24)") + ";"
    h_rezept.portion = portion
    h_rezept.datummod = get_current_date()

    if katnr != h_rezept.kategorie or to_string(h_bezeich, "x(24)") != substring(h_rezept.bezeich, 0, 24):
        h_rezept.kategorie = katnr
        h_rezept.bezeich = to_string(h_bezeich, "x(24)") + katbezeich
    pass

    queasy = get_cache (Queasy, {"key": [(eq, 252)],"number1": [(eq, h_artnr)]})

    if queasy:
        queasy.deci1 =  to_decimal(cost_percent)
        queasy.deci2 =  to_decimal(poten_sell_price)


        pass
        pass
    else:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 252
        queasy.number1 = h_artnr
        queasy.date1 = get_current_date()
        queasy.deci1 =  to_decimal(cost_percent)
        queasy.deci2 =  to_decimal(poten_sell_price)


        pass

    return generate_output()