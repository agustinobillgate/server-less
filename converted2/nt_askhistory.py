from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, Res_line, Reservation, Htparam, Interface

def nt_askhistory():
    params:str = ""
    ci_date:date = None
    bdatestr:str = ""
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


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    resline1_obj_list = []
    for resline1, gast in db_session.query(Resline1, Gast).join(Gast,(Gast.gastnr == Resline1.gastnrmember) & (Gast.aufenthalte == 0)).filter(
             (Resline1.active_flag == 1) & (Resline1.resstatus != 12) & (Resline1.ankunft == ci_date) & (Resline1.l_zuordnung[inc_value(2)] == 0)).order_by(Resline1.resnr, Resline1.reslinnr).all():
        if resline1._recid in resline1_obj_list:
            continue
        else:
            resline1_obj_list.append(resline1._recid)

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