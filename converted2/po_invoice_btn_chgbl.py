#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_kredit

def po_invoice_btn_chgbl(s_list_s_recid:int):

    prepare_cache ([L_op])

    err_code = 0
    l_op = l_kredit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_op, l_kredit
        nonlocal s_list_s_recid

        return {"err_code": err_code}


    l_op = get_cache (L_op, {"_recid": [(eq, s_list_s_recid)]})

    if l_op:

        l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, l_op.lief_nr)],"name": [(eq, l_op.docu_nr)],"lscheinnr": [(eq, l_op.lscheinnr)],"opart": [(ge, 1)],"zahlkonto": [(gt, 0)]})

        if l_kredit:
            err_code = 1

            return generate_output()

    return generate_output()