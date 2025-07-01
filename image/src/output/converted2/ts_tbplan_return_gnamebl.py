#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Res_line

def ts_tbplan_return_gnamebl(t_gastnr:int, room:string):

    prepare_cache ([Guest])

    gname = ""
    resnr1 = 0
    hoga_resnr = 0
    resline = False
    guest = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, resnr1, hoga_resnr, resline, guest, res_line
        nonlocal t_gastnr, room

        return {"gname": gname, "resnr1": resnr1, "hoga_resnr": hoga_resnr, "resline": resline}

    pass

    guest = get_cache (Guest, {"gastnr": [(eq, t_gastnr)]})
    gname = guest.name + "," + guest.vorname1

    if room != "":

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, room)],"gastnrmember": [(eq, guest.gastnr)]})

    if not res_line:
        resnr1 = guest.gastnr
        hoga_resnr = guest.gastnr


    else:
        resline = True

    return generate_output()