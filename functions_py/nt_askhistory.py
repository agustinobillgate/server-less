#using conversion tools version: 1.0.0.117

# =========================================
# Rulita, 23-10-2025 
# Issue : 
# - New compile program
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Res_line, Reservation, Htparam, Interface

def nt_askhistory():

    prepare_cache ([Guest, Res_line, Htparam, Interface])

    params:string = ""
    ci_date:date = None
    bdatestr:string = ""
    it_exists:bool = False
    guest = res_line = reservation = htparam = interface = None

    gast = resline1 = reser = None

    Gast = create_buffer("Gast",Guest)
    Resline1 = create_buffer("Resline1",Res_line)
    Reser = create_buffer("Reser",Reservation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal params, ci_date, bdatestr, it_exists, guest, res_line, reservation, htparam, interface
        nonlocal gast, resline1, reser


        nonlocal gast, resline1, reser

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    ci_date = htparam.fdate

    resline1_obj_list = {}
    resline1 = Res_line()
    gast = Guest()
    for resline1.gastnrmember, resline1._recid, gast.geburtdatum1, gast.vorname1, gast.name, gast.nation1, gast._recid in db_session.query(Resline1.gastnrmember, Resline1._recid, Gast.geburtdatum1, Gast.vorname1, Gast.name, Gast.nation1, Gast._recid).join(Gast,(Gast.gastnr == Resline1.gastnrmember) & (Gast.aufenthalte == 0)).filter(
             (Resline1.active_flag == 1) & (Resline1.resstatus != 12) & (Resline1.ankunft == ci_date) & (Resline1.l_zuordnung[inc_value(2)] == 0)).order_by(Resline1.resnr, Resline1.reslinnr).all():
        if resline1_obj_list.get(resline1._recid):
            continue
        else:
            resline1_obj_list[resline1._recid] = True

        if gast.geburtdatum1 == None:
            bdatestr = ""
        else:
            bdatestr = to_string(get_month(gast.geburtdatum1) , "99") + "/" + to_string(get_day(gast.geburtdatum1) , "99") + "/" + to_string(get_year(gast.geburtdatum1) , "9999")
        params = "_GASTNR:" + to_string(resline1.gastnrmember) + "," + "_FIRSTNAME:" + gast.vorname1 + "," + "_FAMNAME:" + gast.name + "," + "_BDATE:" + bdatestr + "," + "_NAT:" + gast.nation1
        interface = Interface()
        db_session.add(interface)

        interface.key = 11
        interface.int_time = 0
        interface.intdate = get_current_date()
        interface.parameters = params
        it_exists = True

    if it_exists:
        interface = Interface()
        db_session.add(interface)

        interface.key = 11
        interface.int_time = 0
        interface.intdate = get_current_date()
        interface.parameters = "_END"

    return generate_output()