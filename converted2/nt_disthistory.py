from functions.additional_functions import *
import decimal
from datetime import date
from functions.entschl_str70 import entschl_str70
from models import Guest, Res_line, Reservation, Htparam, Paramtext, Interface

def nt_disthistory():
    params:str = ""
    ci_date:date = None
    bdatestr:str = ""
    cistr:str = ""
    costr:str = ""
    fstr:str = ""
    tstr:str = ""
    htl_no:str = ""
    cardnum:str = ""
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


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if paramtext:
        htl_no = get_output(entschl_str70("do-it", paramtext.ptexte))

    resline1_obj_list = []
    for resline1, gast in db_session.query(Resline1, Gast).join(Gast,(Gast.gastnr == Resline1.gastnrmember) & (Gast.aufenthalte >= 2)).filter(
             (Resline1.active_flag == 2) & (Resline1.resstatus == 8) & (Resline1.abreise == ci_date)).order_by(Resline1.resnr, Resline1.reslinnr).all():
        if resline1._recid in resline1_obj_list:
            continue
        else:
            resline1_obj_list.append(resline1._recid)


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