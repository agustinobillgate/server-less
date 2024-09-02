from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Res_line

def ts_tbplan_return_gnamebl(t_gastnr:int, room:str):
    gname = ""
    resnr1 = 0
    hoga_resnr = 0
    resline = False
    guest = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, resnr1, hoga_resnr, resline, guest, res_line


        return {"gname": gname, "resnr1": resnr1, "hoga_resnr": hoga_resnr, "resline": resline}

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == t_gastnr)).first()
    gname = guest.name + "," + guest.vorname1

    if room != "":

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (func.lower(Res_line.zinr) == (room).lower()) &  (Res_line.gastnrmember == guest.gastnr)).first()

    if not res_line:
        resnr1 = guest.gastnr
        hoga_resnr = guest.gastnr


    else:
        resline = True

    return generate_output()