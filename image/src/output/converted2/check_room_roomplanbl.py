#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.res_czinrbl import res_czinrbl
from models import Res_line, Zimmer, Zimkateg

def check_room_roomplanbl(pvilanguage:int, recid1:int, moved_room:string, ci_date:date):

    prepare_cache ([Res_line, Zimmer, Zimkateg])

    msg_str = ""
    lvcarea:string = "roomplan"
    res_line = zimmer = zimkateg = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, res_line, zimmer, zimkateg
        nonlocal pvilanguage, recid1, moved_room, ci_date

        return {"msg_str": msg_str}

    def check_room():

        nonlocal msg_str, lvcarea, res_line, zimmer, zimkateg
        nonlocal pvilanguage, recid1, moved_room, ci_date

        i:int = 1
        f_date:date = None
        error_code:int = 0
        rmcat:string = ""
        answer:bool = False

        res_line = get_cache (Res_line, {"_recid": [(eq, recid1)]})

        if not res_line:

            return

        zimmer = get_cache (Zimmer, {"zinr": [(eq, moved_room)]})

        if (zimmer.zistatus != 0) and res_line.active_flag == 1:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Room assignment not possible.", lvcarea, "")
            i = 99

            return

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

        if zimkateg:

            if res_line.active_flag == 1:
                f_date = ci_date
            else:
                f_date = res_line.ankunft
            rmcat = zimkateg.kurzbez
        rmcat, error_code, msg_str = get_output(res_czinrbl(pvilanguage, f_date, res_line.abreise, (res_line.resstatus == 11 or res_line.resstatus == 13), res_line.resnr, res_line.reslinnr, rmcat, zimmer.zinr))

        if error_code != 0:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Room assignment not possible.", lvcarea, "")
            i = 99

            return
        else:

            if zimmer.zikatnr != res_line.zikatnr:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Different Room Type Detected!", lvcarea, "") + chr_unicode(10) + translateExtended ("Please Go To Modify Reservation For Change Room.", lvcarea, "")

            return


    check_room()

    return generate_output()