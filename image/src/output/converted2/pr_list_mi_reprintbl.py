#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htpint import htpint
from models import L_order, Brief, Htparam

def pr_list_mi_reprintbl(pvilanguage:int, list_str0:string):

    prepare_cache ([L_order, Htparam])

    briefnr = 0
    printer_nr = 0
    l_od_docu_nr = ""
    msg_str = ""
    avail_l_od = False
    lvcarea:string = "prepare-fo-parxls"
    l_order = brief = htparam = None

    l_od = None

    L_od = create_buffer("L_od",L_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal briefnr, printer_nr, l_od_docu_nr, msg_str, avail_l_od, lvcarea, l_order, brief, htparam
        nonlocal pvilanguage, list_str0
        nonlocal l_od


        nonlocal l_od

        return {"briefnr": briefnr, "printer_nr": printer_nr, "l_od_docu_nr": l_od_docu_nr, "msg_str": msg_str, "avail_l_od": avail_l_od}

    briefnr = get_output(htpint(687))

    brief = get_cache (Brief, {"briefnr": [(eq, briefnr)]})

    if not brief:
        msg_str = msg_str + translateExtended ("Letter Number not found : ", lvcarea, "") + to_string(briefnr) + "."

        return generate_output()

    l_od = get_cache (L_order, {"docu_nr": [(eq, trim(list_str0))]})

    if l_od:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 220)]})
        printer_nr = htparam.finteger
        l_od_docu_nr = l_od.docu_nr
        avail_l_od = True

    return generate_output()