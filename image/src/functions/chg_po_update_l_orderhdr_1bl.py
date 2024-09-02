from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_orderhdr, Queasy, Bediener, Res_history

def chg_po_update_l_orderhdr_1bl(rec_id:int, user_init:str):
    gedruckt:date = None
    docu_nr:str = ""
    l_orderhdr = queasy = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gedruckt, docu_nr, l_orderhdr, queasy, bediener, res_history


        return {}


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id)).first()

    l_orderhdr = db_session.query(L_orderhdr).first()
    l_orderhdr.gedruckt = get_current_date()
    gedruckt = l_orderhdr.gedruckt
    docu_nr = l_orderhdr.docu_nr

    l_orderhdr = db_session.query(L_orderhdr).first()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 214) &  (Queasy.char1 == to_string(rec_id))).first()

    if not queasy:

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 214
            queasy.char1 = to_string(rec_id)
            queasy.char2 = user_init
            queasy.char3 = bediener.username


            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Release PO, Date: " + to_string(gedruckt) + "Docu no: " + to_string(docu_nr)
            res_history.action = "Release PO"

    return generate_output()