#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit, L_ophdr, L_lager

def po_retour_btn_help_scheinbl(l_orderhdr_docu_nr:string, l_orderhdr_lief_nr:int, docu_nr:string, lscheinnr:string):

    prepare_cache ([L_ophdr, L_lager])

    curr_lager = 0
    lager_bezeich = ""
    err_code = 0
    l_kredit = l_ophdr = l_lager = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_lager, lager_bezeich, err_code, l_kredit, l_ophdr, l_lager
        nonlocal l_orderhdr_docu_nr, l_orderhdr_lief_nr, docu_nr, lscheinnr

        return {"curr_lager": curr_lager, "lager_bezeich": lager_bezeich, "err_code": err_code}


    l_kredit = get_cache (L_kredit, {"name": [(eq, l_orderhdr_docu_nr)],"lief_nr": [(eq, l_orderhdr_lief_nr)],"zahlkonto": [(gt, 0)]})

    if l_kredit:
        err_code = 1

        return generate_output()

    l_ophdr = get_cache (L_ophdr, {"docu_nr": [(eq, docu_nr)],"lscheinnr": [(eq, lscheinnr)]})
    curr_lager = l_ophdr.lager_nr

    l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_lager)]})
    lager_bezeich = l_lager.bezeich

    return generate_output()