from functions.additional_functions import *
import decimal
from datetime import date
from models import Mc_guest, Guest, Res_line, Htparam, Interface

def nt_distmember():
    ci_date:date = None
    bdatestr:str = ""
    fdatestr:str = ""
    tdatestr:str = ""
    params:str = ""
    it_exists:bool = False
    mc_guest = guest = res_line = htparam = interface = None

    mbership = gast = resline1 = None

    Mbership = create_buffer("Mbership",Mc_guest)
    Gast = create_buffer("Gast",Guest)
    Resline1 = create_buffer("Resline1",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, bdatestr, fdatestr, tdatestr, params, it_exists, mc_guest, guest, res_line, htparam, interface
        nonlocal mbership, gast, resline1


        nonlocal mbership, gast, resline1

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    mbership_obj_list = []
    for mbership, gast in db_session.query(Mbership, Gast).join(Gast,(Gast.gastnr == Mbership.gastnr) & (Gast.resflag != 2)).filter(
             (Mbership.created_date == ci_date) & (Mbership.activeflag)).order_by(Mbership._recid).all():
        if mbership._recid in mbership_obj_list:
            continue
        else:
            mbership_obj_list.append(mbership._recid)

        if gast.geburtdatum1 == None:
            bdatestr = ""
        else:
            bdatestr = to_string(get_month(gast.geburtdatum1) , "99") + "/" + to_string(get_day(gast.geburtdatum1) , "99") + "/" + to_string(get_year(gast.geburtdatum1) , "9999")

        if mbership.fdate == None:
            fdatestr = ""
        else:
            fdatestr = to_string(get_month(mbership.fdate) , "99") + "/" + to_string(get_day(mbership.fdate) , "99") + "/" + to_string(get_year(mbership.fdate) , "9999")

        if mbership.tdate == None:
            tdatestr = ""
        else:
            tdatestr = to_string(get_month(mbership.tdate) , "99") + "/" + to_string(get_day(mbership.tdate) , "99") + "/" + to_string(get_year(mbership.tdate) , "9999")
        params = "_GASTNR:" + to_string(gast.gastnr) + "," + "_FIRSTNAME:" + gast.vorname1 + "," + "_FAMNAME:" + gast.name + "," + "_BDATE:" + bdatestr + "," + "_NAT:" + gast.nation1 + "," + "_CARDNUM:" + mbership.cardnum + "," + "_CARDTYPE:" + to_string(mbership.nr) + "," + "_CDFDATE:" + fdatestr + "," + "_CDTDATE:" + tdatestr
        interface = Interface()
        db_session.add(interface)

        interface.key = 14
        interface.int_time = 0
        interface.intdate = get_current_date()
        interface.parameters = params
        it_exists = True

    if it_exists:
        interface = Interface()
        db_session.add(interface)

        interface.key = 14
        interface.int_time = 0
        interface.intdate = get_current_date()
        interface.parameters = "_END"

    return generate_output()