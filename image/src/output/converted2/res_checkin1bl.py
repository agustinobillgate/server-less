#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Guest, Reservation, Zimmer, Reslin_queasy, Nation, Htparam, Queasy

def res_checkin1bl(pvilanguage:int, resnr:int, reslinnr:int, silenzio:bool):

    prepare_cache ([Res_line, Guest, Reservation, Zimmer, Htparam])

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
    lvcarea:string = "res-checkin"
    res_line = guest = reservation = zimmer = reslin_queasy = nation = htparam = queasy = None

    res_member = res_sharer = res_line1 = buf_resline = gast = b_reservation = None

    Res_member = create_buffer("Res_member",Res_line)
    Res_sharer = create_buffer("Res_sharer",Res_line)
    Res_line1 = create_buffer("Res_line1",Res_line)
    Buf_resline = create_buffer("Buf_resline",Res_line)
    Gast = create_buffer("Gast",Guest)
    B_reservation = create_buffer("B_reservation",Reservation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal can_checkin, msg_str, msg_str1, msg_str2, msg_str3, msg_str4, err_number1, err_number2, err_number3, err_number4, fill_gcfemail, gast_gastnr, q_143, flag_report, warn_flag, lvcarea, res_line, guest, reservation, zimmer, reslin_queasy, nation, htparam, queasy
        nonlocal pvilanguage, resnr, reslinnr, silenzio
        nonlocal res_member, res_sharer, res_line1, buf_resline, gast, b_reservation


        nonlocal res_member, res_sharer, res_line1, buf_resline, gast, b_reservation

        return {"can_checkin": can_checkin, "msg_str": msg_str, "msg_str1": msg_str1, "msg_str2": msg_str2, "msg_str3": msg_str3, "msg_str4": msg_str4, "err_number1": err_number1, "err_number2": err_number2, "err_number3": err_number3, "err_number4": err_number4, "fill_gcfemail": fill_gcfemail, "gast_gastnr": gast_gastnr, "q_143": q_143, "flag_report": flag_report, "warn_flag": warn_flag}


    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if not res_line:

        return generate_output()

    if res_line.active_flag == 1:
        msg_str = translateExtended ("Guest already checked-in.", lvcarea, "")

        return generate_output()

    if res_line.zimmeranz > 1:
        msg_str = translateExtended ("Wrong room quantity.", lvcarea, "")

        return generate_output()

    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

    if (reservation.depositgef - reservation.depositbez - reservation.depositbez2) > 0:
        msg_str = translateExtended ("Deposit not yet settled, check-in not possible", lvcarea, "")

        return generate_output()

    gast = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

    if gast.karteityp != 0:
        msg_str = translateExtended ("Guest Type must be individual guest.", lvcarea, "")

        return generate_output()

    buf_resline = db_session.query(Buf_resline).filter(
             (Buf_resline.resnr == resnr) & (Buf_resline.reslinnr == reslinnr) & ((Buf_resline.resstatus == 6) | (Buf_resline.resstatus == 13))).first()

    if buf_resline:
        msg_str = translateExtended ("Guest already checkin by another user.", lvcarea, "")

        return generate_output()

    b_reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)],"gastnr": [(eq, res_line.gastnr)]})

    if not b_reservation:
        msg_str = translateExtended ("Guest number mismatch detected. Refresh the reservation records now?", lvcarea, "")

        return generate_output()

    res_line1 = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, res_line.zinr)],"_recid": [(ne, res_line._recid)]})

    if not res_line1:

        res_line1 = get_cache (Res_line, {"resstatus": [(eq, 13)],"zinr": [(eq, res_line.zinr)],"l_zuordnung[2]": [(eq, 0)],"_recid": [(ne, res_line._recid)]})

    if res_line1:

        if res_line1.resstatus == 6:

            if (res_line.resstatus <= 2) or (res_line.resstatus == 5) or (res_line.resstatus == 11 and (res_line.resnr != res_line1.resnr)):
                msg_str = translateExtended ("Room", lvcarea, "") + " " + res_line1.zinr + " " + translateExtended ("occupied by : ", lvcarea, "") + res_line1.name + chr_unicode(10) + translateExtended ("Check-out date:", lvcarea, "") + " " + to_string(res_line1.abreise)

                return generate_output()

        elif res_line1.resstatus == 13:

            if res_line.resnr != res_line1.resnr:
                msg_str = translateExtended ("Room", lvcarea, "") + " " + res_line1.zinr + " " + translateExtended ("occupied by : ", lvcarea, "") + res_line1.name + chr_unicode(10) + translateExtended ("Check-out date:", lvcarea, "") + " " + to_string(res_line1.abreise)

                return generate_output()

        if res_line.resstatus == 11 and res_line1.resstatus == 6 and res_line1.abreise < res_line.abreise:
            msg_str = translateExtended ("Room", lvcarea, "") + " " + res_line1.zinr + ": " + translateExtended ("Main guest will checkout earlier than room sharer", lvcarea, "") + chr_unicode(10) + "==> " + translateExtended ("Check-in of sharing guest not possible", lvcarea, "")

            return generate_output()

    if res_line.zinr != "":

        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

        if zimmer.zistatus == 1:
            msg_str = translateExtended ("Room ", lvcarea, "") + zimmer.zinr + " " + translateExtended ("Status: Clean not Checked", lvcarea, "") + chr_unicode(10) + translateExtended ("Check-in not possible - Contact House Keeping.", lvcarea, "")

            return generate_output()

        elif zimmer.zistatus == 2:
            msg_str = translateExtended ("Room", lvcarea, "") + " " + zimmer.zinr + " " + translateExtended ("Status: Vacant Dirty", lvcarea, "") + chr_unicode(10) + translateExtended ("Check-in not possible.", lvcarea, "")

            return generate_output()

        elif zimmer.zistatus == 6:
            msg_str = translateExtended ("Room", lvcarea, "") + " " + zimmer.zinr + " " + translateExtended ("Status = Out-Of-Order.", lvcarea, "") + chr_unicode(10) + translateExtended ("Checkin not possible.", lvcarea, "")

            return generate_output()

        if res_line.resstatus == 11:

            res_member = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"resstatus": [(le, 6)],"zinr": [(eq, res_line.zinr)]})

            if not res_member:
                msg_str = translateExtended ("Room", lvcarea, "") + " " + zimmer.zinr + ": " + translateExtended ("No main guest found.", lvcarea, "")

                return generate_output()

            elif res_member.resstatus != 6:
                warn_flag = True
                msg_str = "&W" + translateExtended ("Room", lvcarea, "") + " " + zimmer.zinr + chr_unicode(10) + translateExtended ("The main guest", lvcarea, "") + " " + res_member.name + " " + translateExtended ("not yet checked-in.", lvcarea, "")

    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"betriebsnr": [(eq, 0)]})
    flag_report = None != reslin_queasy

    nation = get_cache (Nation, {"kurzbez": [(eq, gast.land)]})

    if not nation:
        msg_str1 = translateExtended ("Guest COUNTRY not defined:", lvcarea, "") + " " + gast.land
        err_number1 = 1

    nation = get_cache (Nation, {"kurzbez": [(eq, gast.nation1)]})

    if not nation:
        msg_str2 = translateExtended ("Guest NATIONALITY not defined:", lvcarea, "") + " " + gast.nation1
        err_number2 = 1
    gast_gastnr = gast.gastnr

    if gast.email_adr == "":

        htparam = get_cache (Htparam, {"paramnr": [(eq, 249)]})

        if htparam.paramgruppe == 6 and htparam.flogical:
            fill_gcfemail = True

    if trim(gast.telefon) == "" and trim(gast.mobil_telefon) == "":

        htparam = get_cache (Htparam, {"paramnr": [(eq, 279)]})

        if htparam.paramgruppe == 6 and htparam.flogical:
            msg_str = msg_str + chr_unicode(3) + "YES"

    if not matches(res_line.zimmer_wunsch,r"*SEGM_PUR*"):
        msg_str3 = translateExtended ("Purpose of Stay not assigned.", lvcarea, "")

        queasy = get_cache (Queasy, {"key": [(eq, 143)]})

        if queasy:
            q_143 = True
        err_number3 = 1

    if res_line.zinr == "":
        msg_str4 = translateExtended ("Room number not assigned.", lvcarea, "")
        err_number4 = 1
    can_checkin = (err_number1 == 0 and err_number2 == 0 and err_number3 == 0 and err_number4 == 0)

    return generate_output()