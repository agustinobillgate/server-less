#using conversion tools version: 1.0.0.117

# =========================================
# Rulita, 23-10-2025 
# Issue : 
# - New compile program
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mc_guest, Guest, Res_line, Htparam, Interface

def nt_distmember():

    prepare_cache ([Mc_guest, Guest, Htparam, Interface])

    ci_date:date = None
    bdatestr:string = ""
    fdatestr:string = ""
    tdatestr:string = ""
    params:string = ""
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


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    ci_date = htparam.fdate

    mbership_obj_list = {}
    mbership = Mc_guest()
    gast = Guest()
    for mbership.fdate, mbership.tdate, mbership.cardnum, mbership.nr, mbership._recid, gast.geburtdatum1, gast.gastnr, gast.vorname1, gast.name, gast.nation1, gast._recid in db_session.query(Mbership.fdate, Mbership.tdate, Mbership.cardnum, Mbership.nr, Mbership._recid, Gast.geburtdatum1, Gast.gastnr, Gast.vorname1, Gast.name, Gast.nation1, Gast._recid).join(Gast,(Gast.gastnr == Mbership.gastnr) & (Gast.resflag != 2)).filter(
             (Mbership.created_date == ci_date) & (Mbership.activeflag)).order_by(Mbership._recid).all():
        if mbership_obj_list.get(mbership._recid):
            continue
        else:
            mbership_obj_list[mbership._recid] = True

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