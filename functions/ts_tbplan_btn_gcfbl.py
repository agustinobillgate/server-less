#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Mc_guest

def ts_tbplan_btn_gcfbl(pvilanguage:int, gastno:int):

    prepare_cache ([Guest])

    resnr1 = 0
    gname = ""
    remark = ""
    lvcarea:string = "TS-tbplan"
    guest = mc_guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resnr1, gname, remark, lvcarea, guest, mc_guest
        nonlocal pvilanguage, gastno

        return {"resnr1": resnr1, "gname": gname, "remark": remark}


    guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})
    resnr1 = guest.gastnr
    gname = guest.name + "," + guest.vorname1

    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)],"activeflag": [(eq, True)]})

    if mc_guest:
        remark = translateExtended ("Membership No:", lvcarea, "") +\
                " " + mc_guest.cardnum + chr_unicode(10)

    return generate_output()