from functions.additional_functions import *
import decimal
from sqlalchemy import func
import re
from models import Res_line, Guest, Reservation, Zimmer, Reslin_queasy, Nation, Htparam, Queasy

def res_checkin1bl(pvilanguage:int, resnr:int, reslinnr:int, silenzio:bool):
    can_checkin = False
    msg_str = ""
    msg_str1 = ""
    msg_str2 = ""
    msg_str3 = ""
    msg_str4 = ""
    err_number1 = 0
    err_number2 = 0
    err_number3 = 0
    err_number4 = 0
    fill_gcfemail = False
    gast_gastnr = 0
    q_143 = False
    flag_report = False
    warn_flag = False
    lvcarea:str = "res_checkin"
    res_line = guest = reservation = zimmer = reslin_queasy = nation = htparam = queasy = None

    res_member = res_sharer = res_line1 = gast = None

    Res_member = Res_line
    Res_sharer = Res_line
    Res_line1 = Res_line
    Gast = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal can_checkin, msg_str, msg_str1, msg_str2, msg_str3, msg_str4, err_number1, err_number2, err_number3, err_number4, fill_gcfemail, gast_gastnr, q_143, flag_report, warn_flag, lvcarea, res_line, guest, reservation, zimmer, reslin_queasy, nation, htparam, queasy
        nonlocal res_member, res_sharer, res_line1, gast


        nonlocal res_member, res_sharer, res_line1, gast
        return {"can_checkin": can_checkin, "msg_str": msg_str, "msg_str1": msg_str1, "msg_str2": msg_str2, "msg_str3": msg_str3, "msg_str4": msg_str4, "err_number1": err_number1, "err_number2": err_number2, "err_number3": err_number3, "err_number4": err_number4, "fill_gcfemail": fill_gcfemail, "gast_gastnr": gast_gastnr, "q_143": q_143, "flag_report": flag_report, "warn_flag": warn_flag}


    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if res_line.active_flag == 1:
        msg_str = translateExtended ("Guest already checked_in.", lvcarea, "")

        return generate_output()

    if res_line.zimmeranz > 1:
        msg_str = translateExtended ("Wrong room quantity.", lvcarea, "")

        return generate_output()

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == res_line.resnr)).first()

    if (reservation.depositgef - reservation.depositbez - reservation.depositbez2) > 0:
        msg_str = translateExtended ("Deposit not yet settled, check_in not possible", lvcarea, "")

        return generate_output()

    gast = db_session.query(Gast).filter(
            (Gast.gastnr == res_line.gastnrmember)).first()

    if gast.karteityp != 0:
        msg_str = translateExtended ("Guest Type must be individual guest.", lvcarea, "")

        return generate_output()

    res_line1 = db_session.query(Res_line1).filter(
            (Res_line1.resstatus == 6) &  (Res_line1.zinr == res_line.zinr) &  (Res_line1._recid != res_line._recid)).first()

    if not res_line1:

        res_line1 = db_session.query(Res_line1).filter(
                (Res_line1.resstatus == 13) &  (Res_line1.zinr == res_line.zinr) &  (Res_line1.l_zuordnung[2] == 0) &  (Res_line1._recid != res_line._recid)).first()

    if res_line1:

        if res_line1.resstatus == 6:

            if (res_line.resstatus <= 2) or (res_line.resstatus == 5) or (res_line.resstatus == 11 and (res_line.resnr != res_line1.resnr)):
                msg_str = translateExtended ("Room", lvcarea, "") + " " + res_line1.zinr + " " + translateExtended ("occupied by : ", lvcarea, "") + res_line1.name + chr(10) + translateExtended ("Check_out date:", lvcarea, "") + " " + to_string(res_line1.abreise)

                return generate_output()

        elif res_line1.resstatus == 13:

            if res_line.resnr != res_line1.resnr:
                msg_str = translateExtended ("Room", lvcarea, "") + " " + res_line1.zinr + " " + translateExtended ("occupied by : ", lvcarea, "") + res_line1.name + chr(10) + translateExtended ("Check_out date:", lvcarea, "") + " " + to_string(res_line1.abreise)

                return generate_output()

        if res_line.resstatus == 11 and res_line1.resstatus == 6 and res_line1.abreise < res_line.abreise:
            msg_str = translateExtended ("Room", lvcarea, "") + " " + res_line1.zinr + ": " + translateExtended ("Main guest will checkout earlier than room sharer", lvcarea, "") + chr(10) + "==> " + translateExtended ("Check_in of sharing guest not possible", lvcarea, "")

            return generate_output()

    if res_line.zinr != "":

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == res_line.zinr)).first()

        if zimmer.zistatus == 1:
            msg_str = translateExtended ("Room ", lvcarea, "") + zimmer.zinr + " " + translateExtended ("Status: Clean not Checked", lvcarea, "") + chr(10) + translateExtended ("Check_in not possible - Contact House Keeping.", lvcarea, "")

            return generate_output()

        elif zimmer.zistatus == 2:
            msg_str = translateExtended ("Room", lvcarea, "") + " " + zimmer.zinr + " " + translateExtended ("Status: Vacant Dirty", lvcarea, "") + chr(10) + translateExtended ("Check_in not possible.", lvcarea, "")

            return generate_output()

        elif zimmer.zistatus == 6:
            msg_str = translateExtended ("Room", lvcarea, "") + " " + zimmer.zinr + " " + translateExtended ("Status  ==  Out_Of_Order.", lvcarea, "") + chr(10) + translateExtended ("Checkin not possible.", lvcarea, "")

            return generate_output()

        if res_line.resstatus == 11:

            res_member = db_session.query(Res_member).filter(
                    (Res_member.resnr == res_line.resnr) &  (Res_member.resstatus <= 6) &  (Res_member.zinr == res_line.zinr)).first()

            if not res_member:
                msg_str = translateExtended ("Room", lvcarea, "") + " " + zimmer.zinr + ": " + translateExtended ("No main guest found.", lvcarea, "")

                return generate_output()

            elif res_member.resstatus != 6:
                warn_flag = True
                msg_str = "&W" + translateExtended ("Room", lvcarea, "") + " " + zimmer.zinr + chr(10) + translateExtended ("The main guest", lvcarea, "") + " " + res_member.name + " " + translateExtended ("not yet checked_in.", lvcarea, "")

    reslin_queasy = db_session.query(Reslin_queasy).filter(
            (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.betriebsnr == 0)).first()
    flag_report = None != reslin_queasy

    nation = db_session.query(Nation).filter(
            (Nation.kurzbez == gast.land)).first()

    if not nation:
        msg_str1 = translateExtended ("Guest COUNTRY not defined:", lvcarea, "") + " " + gast.land
        err_number1 = 1

    nation = db_session.query(Nation).filter(
            (Nation.kurzbez == gast.nation1)).first()

    if not nation:
        msg_str2 = translateExtended ("Guest NATIONALITY not defined:", lvcarea, "") + " " + gast.nation1
        err_number2 = 1
    gast_gastnr = gast.gastnr

    if gast.email_adr == "":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 249)).first()

        if htparam.paramgruppe == 6 and htparam.flogical:
            fill_gcfemail = True

    if trim(gast.telefon) == "" and trim(gast.mobil_telefon) == "":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 279)).first()

        if htparam.paramgruppe == 6 and htparam.flogical:
            msg_str = msg_str + chr(3) + "YES"

    if not re.match(".*SEGM__PUR.*",res_line.zimmer_wunsch):
        msg_str3 = translateExtended ("Purpose of Stay not assigned.", lvcarea, "")

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 143)).first()

        if queasy:
            q_143 = True
        err_number3 = 1

    if res_line.zinr == "":
        msg_str4 = translateExtended ("Room number not assigned.", lvcarea, "")
        err_number4 = 1
    can_checkin = (err_number1 == 0 and err_number2 == 0 and err_number3 == 0 and err_number4 == 0)

    return generate_output()