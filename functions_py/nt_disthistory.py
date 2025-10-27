#using conversion tools version: 1.0.0.117

# =========================================
# Rulita, 23-10-2025 
# Issue : 
# - New compile program
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.entschl_str70 import entschl_str70
from models import Guest, Res_line, Reservation, Htparam, Paramtext, Interface

def nt_disthistory():

    prepare_cache ([Res_line, Htparam, Paramtext, Interface])

    params:string = ""
    ci_date:date = None
    bdatestr:string = ""
    cistr:string = ""
    costr:string = ""
    fstr:string = ""
    tstr:string = ""
    htl_no:string = ""
    cardnum:string = ""
    cardtype:int = 0
    it_exists:bool = False
    guest = res_line = reservation = htparam = paramtext = interface = None

    gast = resline1 = reser = None

    Gast = create_buffer("Gast",Guest)
    Resline1 = create_buffer("Resline1",Res_line)
    Reser = create_buffer("Reser",Reservation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal params, ci_date, bdatestr, cistr, costr, fstr, tstr, htl_no, cardnum, cardtype, it_exists, guest, res_line, reservation, htparam, paramtext, interface
        nonlocal gast, resline1, reser


        nonlocal gast, resline1, reser

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    ci_date = htparam.fdate

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext:
        htl_no = get_output(entschl_str70("do-it", paramtext.ptexte))

    resline1_obj_list = {}
    for resline1, gast in db_session.query(Resline1, Gast).join(Gast,(Gast.gastnr == Resline1.gastnrmember) & (Gast.aufenthalte >= 2)).filter(
             (Resline1.active_flag == 2) & (Resline1.resstatus == 8) & (Resline1.abreise == ci_date)).order_by(Resline1.resnr, Resline1.reslinnr).all():
        if resline1_obj_list.get(resline1._recid):
            continue
        else:
            resline1_obj_list[resline1._recid] = True


        params = to_string(resline1.gastnrmember)
        interface = Interface()
        db_session.add(interface)

        interface.key = 12
        interface.int_time = 0
        interface.intdate = get_current_date()
        interface.parameters = params
        interface.resnr = resline1.resnr
        interface.reslinnr = resline1.reslinnr
        it_exists = True

    if it_exists:
        interface = Interface()
        db_session.add(interface)

        interface.key = 12
        interface.int_time = 0
        interface.intdate = get_current_date()
        interface.parameters = "_END"

    return generate_output()