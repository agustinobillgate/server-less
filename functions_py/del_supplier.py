#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr, L_kredit, L_op, L_lieferant

def del_supplier(lief_nr:int):
    error_code = 0
    l_orderhdr = l_kredit = l_op = l_lieferant = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, l_orderhdr, l_kredit, l_op, l_lieferant
        nonlocal lief_nr

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
        db_session.delete(l_lieferant)

    return generate_output()