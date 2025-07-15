#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_kredit

def supply_inlist_btn_insartbl(pvilanguage:int, str_list_billdate:date, str_list_lief_nr:int, str_list_docu_nr:string, str_list_lscheinnr:string):

    prepare_cache ([Htparam])

    msg_str = ""
    lvcarea:string = "supply-inlist"
    htparam = l_kredit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, htparam, l_kredit
        nonlocal pvilanguage, str_list_billdate, str_list_lief_nr, str_list_docu_nr, str_list_lscheinnr

        return {"msg_str": msg_str}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})

    if htparam.fdate != None and htparam.fdate > str_list_billdate:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("The receiving record(s) have been transfered to the G/L.", lvcarea, "") + chr_unicode(10) + translateExtended ("Inserting is no longer possible.", lvcarea, "")

        return generate_output()

    l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, str_list_lief_nr)],"name": [(eq, str_list_docu_nr)],"lscheinnr": [(eq, str_list_lscheinnr)],"opart": [(ge, 1)],"zahlkonto": [(gt, 0)]})

    if l_kredit:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("The A/P Payment record found.", lvcarea, "") + chr_unicode(10) + translateExtended ("Inserting is no longer possible.", lvcarea, "")

        return generate_output()

    return generate_output()