from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import H_rezept, H_rezlin, Bediener, Res_history

def chg_rezeipt_chg_rezlin_webbl(s_rezlin_h_recid:int, h_rezept_recid:int, qty:decimal, lostfact:decimal, user_init:str):
    artnrlager = 0
    vlog:bool = False
    h_rezept = h_rezlin = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal artnrlager, vlog, h_rezept, h_rezlin, bediener, res_history
        nonlocal s_rezlin_h_recid, h_rezept_recid, qty, lostfact, user_init


        return {"artnrlager": artnrlager}


    h_rezept = db_session.query(H_rezept).filter(
             (H_rezept._recid == h_rezept_recid)).first()

    h_rezlin = db_session.query(H_rezlin).filter(
             (H_rezlin._recid == s_rezlin_h_recid)).first()

    if h_rezlin.menge != qty or h_rezlin.lostfact != lostfact:
        vlog = True

    if vlog:

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()
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
    h_rezlin.menge =  to_decimal(qty)
    h_rezlin.lostfact =  to_decimal(lostfact)


    h_rezept.datummod = get_current_date()
    artnrlager = h_rezlin.artnrlager

    return generate_output()