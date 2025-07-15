#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit

def po_list_btn_sretourbl(l_orderhdr_lief_nr:int, l_orderhdr_docu_nr:string):
    avail_l_kredit = False
    l_kredit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_kredit, l_kredit
        nonlocal l_orderhdr_lief_nr, l_orderhdr_docu_nr

        return {"avail_l_kredit": avail_l_kredit}


    l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, l_orderhdr_lief_nr)],"name": [(eq, l_orderhdr_docu_nr)],"zahlkonto": [(gt, 0)]})

    if l_kredit:
        avail_l_kredit = True

    return generate_output()