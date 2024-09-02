from functions.additional_functions import *
import decimal
from models import Guest, Mc_guest

def ts_tbplan_btn_gcfbl(pvilanguage:int, gastno:int):
    resnr1 = 0
    gname = ""
    remark = ""
    lvcarea:str = "TS_tbplan"
    guest = mc_guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resnr1, gname, remark, lvcarea, guest, mc_guest


        return {"resnr1": resnr1, "gname": gname, "remark": remark}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastno)).first()
    resnr1 = guest.gastnr
    gname = guest.name + "," + guest.vorname1

    mc_guest = db_session.query(Mc_guest).filter(
            (Mc_guest.gastnr == guest.gastnr) &  (Mc_guest.activeflag)).first()

    if mc_guest:
        remark = translateExtended ("Membership No:", lvcarea, "") +\
                " " + mc_guest.cardnum + chr(10)

    return generate_output()