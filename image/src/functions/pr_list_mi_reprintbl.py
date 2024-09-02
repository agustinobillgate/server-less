from functions.additional_functions import *
import decimal
from functions.htpint import htpint
from models import L_order, Brief, Htparam

def pr_list_mi_reprintbl(pvilanguage:int, list_str0:str):
    briefnr = 0
    printer_nr = 0
    l_od_docu_nr = ""
    msg_str = ""
    avail_l_od = False
    lvcarea:str = "prepare_fo_parxls"
    l_order = brief = htparam = None

    l_od = None

    L_od = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal briefnr, printer_nr, l_od_docu_nr, msg_str, avail_l_od, lvcarea, l_order, brief, htparam
        nonlocal l_od


        nonlocal l_od
        return {"briefnr": briefnr, "printer_nr": printer_nr, "l_od_docu_nr": l_od_docu_nr, "msg_str": msg_str, "avail_l_od": avail_l_od}

    briefnr = get_output(htpint(687))

    brief = db_session.query(Brief).filter(
            (briefnr == briefnr)).first()

    if not brief:
        msg_str = msg_str + translateExtended ("Letter Number not found : ", lvcarea, "") + to_string(briefnr) + "."

        return generate_output()

    l_od = db_session.query(L_od).filter(
            (L_od.docu_nr == trim(list_str0))).first()

    if l_od:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 220)).first()
        printer_nr = htparam.finteger
        l_od_docu_nr = l_od.docu_nr
        avail_l_od = True

    return generate_output()