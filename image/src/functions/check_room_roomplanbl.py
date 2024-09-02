from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.res_czinrbl import res_czinrbl
from models import Res_line, Zimmer, Zimkateg

def check_room_roomplanbl(pvilanguage:int, recid1:int, moved_room:str, ci_date:date):
    msg_str = ""
    lvcarea:str = "roomplan"
    res_line = zimmer = zimkateg = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, res_line, zimmer, zimkateg


        return {"msg_str": msg_str}

    def check_room():

        nonlocal msg_str, lvcarea, res_line, zimmer, zimkateg

        i:int = 1
        fdate:date = None
        error_code:int = 0
        rmcat:str = ""
        answer:bool = False

        res_line = db_session.query(Res_line).filter(
                (Res_line._recid == recid1)).first()

        zimmer = db_session.query(Zimmer).filter(
                (func.lower(Zimmer.zinr) == (moved_room).lower())).first()

        if (zimmer.zistatus != 0) and res_line.active_flag == 1:
            msg_str = msg_str + chr(2) + translateExtended ("Room assignment not possible.", lvcarea, "")
            i = 99

            return

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == zimmer.zikatnr)).first()

        if zimkateg:

            if res_line.active_flag == 1:
                fdate = ci_date
            else:
                fdate = res_line.ankunft
            rmcat = zimkateg.kurzbez
        rmcat, error_code, msg_str = get_output(res_czinrbl(pvilanguage, fdate, res_line.abreise, (res_line.resstatus == 11 or res_line.resstatus == 13), res_line.resnr, res_line.reslinnr, rmcat, zimmer.zinr))

        if error_code != 0:
            msg_str = msg_str + chr(2) + translateExtended ("Room assignment not possible.", lvcarea, "")
            i = 99

            return
        else:

            if zimmer.zikatnr != res_line.zikatnr:
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("Different Room Type Detected!", lvcarea, "") + chr(10) + translateExtended ("Please Go To Modify Reservation For Change Room.", lvcarea, "")

            return

    check_room()

    return generate_output()