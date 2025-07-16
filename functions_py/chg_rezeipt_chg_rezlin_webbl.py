#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, H_rezlin, Bediener, Res_history

def chg_rezeipt_chg_rezlin_webbl(s_rezlin_h_recid:int, h_rezept_recid:int, qty:Decimal, lostfact:Decimal, user_init:string):

    prepare_cache ([H_rezept, H_rezlin, Bediener, Res_history])

    artnrlager = 0
    vlog:bool = False
    h_rezept = h_rezlin = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artnrlager, vlog, h_rezept, h_rezlin, bediener, res_history
        nonlocal s_rezlin_h_recid, h_rezept_recid, qty, lostfact, user_init

        return {"artnrlager": artnrlager}


    h_rezept = get_cache (H_rezept, {"_recid": [(eq, h_rezept_recid)]})
    if h_rezept is None:
        return generate_output()

    h_rezlin = get_cache (H_rezlin, {"_recid": [(eq, s_rezlin_h_recid)]})
    if h_rezlin is None:
        return generate_output()

    if h_rezlin.menge != qty or h_rezlin.lostfact != lostfact:
        vlog = True

    if vlog:

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Change Recipe"
        res_history.aenderung = "Modify Recipe Item " + to_string(h_rezept.artnrrezept) +\
                "(" + substring(h_rezept.bezeich, 0, 24) + ")" + " => "

        if h_rezlin.menge != qty:
            res_history.aenderung = res_history.aenderung + "qty " + to_string(h_rezlin.menge) + " to " + to_string(qty) + ";"

        elif h_rezlin.lostfact != lostfact:
            res_history.aenderung = res_history.aenderung + "Loss Factor " + to_string(h_rezlin.lostfact) + " to " + to_string(lostfact) + ";"
    pass
    h_rezlin.menge =  to_decimal(qty)
    h_rezlin.lostfact =  to_decimal(lostfact)


    pass
    pass
    h_rezept.datummod = get_current_date()
    pass
    artnrlager = h_rezlin.artnrlager

    return generate_output()