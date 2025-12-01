#using conversion tools version: 1.0.0.117
#--------------------------------------------
# Rd, 26/11/2025, with_for_update
#--------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
import random
from models import Guestbook, Queasy

def get_interface_info_iscanbl(usersession:string):
    scan_data = ""
    scan_image = ""
    finish_flag = None
    success_flag = None
    pointer:bytes = None
    guestnumber:int = 0
    recguestbook:int = 0
    logid:int = 0
    logstr:string = ""
    guestbook = queasy = None

    t_guestbook = bguestbook = None

    t_guestbook_data, T_guestbook = create_model_like(Guestbook, {"recidguestbook":int})

    Bguestbook = create_buffer("Bguestbook",Guestbook)


    db_session = local_storage.db_session
    usersession = usersession.strip()

    def generate_output():
        nonlocal scan_data, scan_image, finish_flag, success_flag, pointer, guestnumber, recguestbook, logid, logstr, guestbook, queasy
        nonlocal usersession
        nonlocal bguestbook


        nonlocal t_guestbook, bguestbook
        nonlocal t_guestbook_data

        return {"scan_data": scan_data, "scan_image": scan_image, "finish_flag": finish_flag, "success_flag": success_flag}

    if usersession == "":
        usersession = ""

    if usersession == None:
        usersession = ""
    logid = random.randint(1, 99999)
    logstr = "logid=" + to_string(logid) + "|SESSION=" + usersession + "|START"

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 999) & (Queasy.char1 == usersession)).order_by(Queasy._recid.desc()).with_for_update().first()

    if queasy:
        pass
        logstr = "logid=" + to_string(logid) + "|SESSION=" + usersession + "|FOUND QUEASY"
        finish_flag = queasy.logi1
        success_flag = queasy.logi2
        scan_data = queasy.char2
        guestnumber = queasy.number2

        for guestbook in db_session.query(Guestbook).filter(
                 (Guestbook.gastnr == guestnumber)).order_by(Guestbook._recid).all():
            t_guestbook = T_guestbook()
            t_guestbook_data.append(t_guestbook)

            buffer_copy(guestbook, t_guestbook)
            recidguestbook = guestbook._recid
        pass

        t_guestbook = query(t_guestbook_data, filters=(lambda t_guestbook: t_guestbook.orig_infostr == usersession), first=True)

        if t_guestbook:
            logstr = "logid=" + to_string(logid) + "|SESSION=" + usersession + "|FOUND GUESTBOOK"
            recguestbook = t_guestbook.recidguestbook
            pointer = t_guestbook.imagefile
            scan_image = base64_encode(pointer)

            if finish_flag:
                t_guestbook_data.remove(t_guestbook)
            pass

        if finish_flag:
            db_session.delete(queasy)

            bguestbook = db_session.query(Bguestbook).filter(
                     (Bguestbook._recid == recguestbook)).with_for_update().first()

            if bguestbook:
                db_session.delete(bguestbook)
        pass
    logstr = "logid=" + to_string(logid) + "|SESSION=" + usersession + "|END|FINIS=" + to_string(finish_flag)

    return generate_output()