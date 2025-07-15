#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit

def pchase_stockin_btn_sretourbl(q2_list_lief_nr:int, q2_list_docu_nr:string):
    avail_l_kredit = False
    l_kredit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_kredit, l_kredit
        nonlocal q2_list_lief_nr, q2_list_docu_nr

        return {"avail_l_kredit": avail_l_kredit}


    l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, q2_list_lief_nr)],"name": [(eq, q2_list_docu_nr)],"zahlkonto": [(gt, 0)]})

    if l_kredit:
        avail_l_kredit = True

    return generate_output()