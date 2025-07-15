#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr, Queasy, Bediener, Res_history

def chg_po_update_l_orderhdr_1bl(rec_id:int, user_init:string):

    prepare_cache ([L_orderhdr, Queasy, Bediener, Res_history])

    gedruckt:date = None
    docu_nr:string = ""
    l_orderhdr = queasy = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gedruckt, docu_nr, l_orderhdr, queasy, bediener, res_history
        nonlocal rec_id, user_init

        return {}


    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})
    pass
    l_orderhdr.gedruckt = get_current_date()
    gedruckt = l_orderhdr.gedruckt
    docu_nr = l_orderhdr.docu_nr


    pass

    queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(rec_id))]})

    if not queasy:

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

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