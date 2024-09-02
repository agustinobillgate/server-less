from functions.additional_functions import *
import decimal
from datetime import date
from models import Reservation, Guest, Artikel, Debitor, Htparam, Res_line

def prepare_auto_checkinbl(pvilanguage:int, resnr:int):
    f_tittle = ""
    msg_str = ""
    msg_str1 = ""
    f_char = ""
    guest_gastnr = 0
    guest_kreditlimit = 0
    outstand = 0
    f_logical = False
    res_list_list = []
    lvcarea:str = "prepare_auto_checkin"
    ci_date:date = None
    reservation = guest = artikel = debitor = htparam = res_line = None

    res_list = None

    res_list_list, Res_list = create_model("Res_list", {"gastnr":int, "zinr":str, "name":str, "resnr":int, "reslinnr":int, "activeflag":int, "resstatus":int, "sysdate":date, "zeit":int, "selflag":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_tittle, msg_str, msg_str1, f_char, guest_gastnr, guest_kreditlimit, outstand, f_logical, res_list_list, lvcarea, ci_date, reservation, guest, artikel, debitor, htparam, res_line


        nonlocal res_list
        nonlocal res_list_list
        return {"f_tittle": f_tittle, "msg_str": msg_str, "msg_str1": msg_str1, "f_char": f_char, "guest_gastnr": guest_gastnr, "guest_kreditlimit": guest_kreditlimit, "outstand": outstand, "f_logical": f_logical, "res-list": res_list_list}

    def create_list():

        nonlocal f_tittle, msg_str, msg_str1, f_char, guest_gastnr, guest_kreditlimit, outstand, f_logical, res_list_list, lvcarea, ci_date, reservation, guest, artikel, debitor, htparam, res_line


        nonlocal res_list
        nonlocal res_list_list

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.active_flag == 0) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.ankunft == ci_date)).all():
            res_list = Res_list()
            res_list_list.append(res_list)

            res_list.gastnr = res_line.gastnr
            res_list.name = res_line.name
            res_list.zinr = res_line.zinr
            res_list.resnr = res_line.resnr
            res_list.reslinnr = res_line.reslinnr
            res_list.activeflag = res_line.active_flag
            res_list.resstatus = res_line.resstatus
            res_list.sysdate = get_current_date()
            res_list.zeit = get_current_time_in_seconds()

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    if (reservation.depositgef - reservation.depositbez - reservation.depositbez2) > 0:
        msg_str = msg_str + chr(2) + translateExtended ("Deposit not yet settled, check_in not possible", lvcarea, "")

        return generate_output()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == reservation.gastnr)).first()

    if guest.karteityp >= 1 and guest.kreditlimit > 0 and guest.zahlungsart > 0:
        outstand = 0

        debitor_obj_list = []
        for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0) &  (Artikel.artart == 2)).filter(
                (Debitor.gastnr == guest.gastnr) &  (Debitor.opart <= 1)).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            outstand = outstand + debitor.saldo

        if outstand > guest.kreditlimit:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 320)).first()

            if htparam.flogical:
                f_logical = True
                msg_str1 = msg_str1 + chr(2) + translateExtended ("Credit Limit overdrawn: ", lvcarea, "") + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 141)).first()
                f_char = htparam.fchar

                if htparam.fchar != "":
                    guest_gastnr = guest.gastnr
                    guest_kreditlimit = guest.kreditlimit

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()
    f_tittle = translateExtended ("Automatic Checkin for :", lvcarea, "") + reservation.name
    create_list()

    return generate_output()