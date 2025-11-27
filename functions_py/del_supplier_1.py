#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr, L_kredit, L_op, L_lieferant, Bediener, Res_history

def del_supplier_1(lief_nr:int, user_init:string):

    prepare_cache ([Bediener, Res_history])

    error_code = 0
    l_orderhdr = l_kredit = l_op = l_lieferant = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, l_orderhdr, l_kredit, l_op, l_lieferant, bediener, res_history
        nonlocal lief_nr, user_init

        return {"error_code": error_code}


    l_orderhdr = get_cache (L_orderhdr, {"lief_nr": [(eq, lief_nr)]})

    if l_orderhdr:
        error_code = 1

        return generate_output()

    l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, lief_nr)],"zahlkonto": [(eq, 0)]})

    if l_kredit:
        error_code = 2

        return generate_output()

    l_op = get_cache (L_op, {"lief_nr": [(eq, lief_nr)],"op_art": [(eq, 1)]})

    if l_op:
        error_code = 3

        return generate_output()

    if error_code == 0:
        l_lieferant = db_session.query(L_lieferant).filter(L_lieferant.lief_nr == lief_nr).with_for_update().first()

        if l_lieferant:
            db_session.delete(l_lieferant)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Delete Supplier - Supplier No : " + to_string(lief_nr)
        res_history.action = "Delete"


        pass
        pass

    return generate_output()